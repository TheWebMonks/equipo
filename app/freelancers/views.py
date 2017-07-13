from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import ProfileForm, ProfileSkillForm, ExperienceForm, ProjectForm, CompanyForm, EducationForm, \
    CategoryForm, KindOfTaskForm, ExpendedTimeForm, ExpenseForm,ContractForm, InvoiceForm
from django.views import generic
from social_django.models import UserSocialAuth
from django.db.models import Q

from cloudinary.uploader import upload
from django_gravatar.helpers import get_gravatar_url, has_gravatar, get_gravatar_profile_url, calculate_gravatar_hash
from urllib.request import urlopen

# from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import JsonResponse
from weasyprint import default_url_fetcher, HTML, CSS
from django.template.loader import get_template
from django.template import RequestContext
from django.conf import settings
from fm.views import AjaxCreateView
import json


class ProjectView(generic.DetailView):
    model = Project

    template_name = 'companies/project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs,)
        context['required_skills'] = Skill.objects.all()
        return context


class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'companies/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs, )
        return context


def view_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    education = Education.objects.filter(profile=profile)
    experience = Experience.objects.filter(profile=profile)

    return render(request, 'companies/profile.html', {'profile': profile, 'studies': education,
                                                      'experiences': experience})


@login_required
def add_project(request):
    profile = get_profile(request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.user = request.user
            new_project.date = datetime.now()
            new_project.company = Company.objects.get(user=request.user)
            new_project.save()
            form.save_m2m()
            messages.success(request, 'Form submission successful')
    else:
        form = ProjectForm()

    return render(request, 'companies/add_project.html', {'form': form, 'profile': profile})


def project(request, pk):
    this_project = Project.objects.get(pk=pk)
    if request.user.is_authenticated():
        profile = get_profile(user= request.user)
    else:
        profile = None
    return render(request, 'freelancers/project.html', {'project': this_project, 'profile': profile})


def browse_projects(request):
    projects_all = Project.objects.all()
    return render(request, 'freelancers/projects.html', {'projects': projects_all})


def my_projects(request):
    company = Company.objects.get(user=request.user)
    projects = Project.objects.filter(company=company)
    return render(request, 'companies/projects.html', {'projects': projects})


@login_required
def apply_project(request, pk):
    '''
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        company = None

    if company:
        messages.error(request, 'You must create a profile as freelance')
        return redirect('/view_project/' + pk)
    '''
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        profile = get_profile(user=request.user)

        if profile:
            #if profile in profile.project_set.all:
            #    return JsonResponse({"success": False, "message": "You are already in"})
            project.freelancers.add(profile)
            project.save()
            return JsonResponse({"success": True, "message": "OK"})
        else:
            return JsonResponse({"success": False, "message": "Error on application"})


@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, 'Form submission successful')

    else:
        form = CompanyForm()
    return render(request, 'companies/add_company.html', {'form': form})

@login_required
def company_home(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        company = None

    profiles = Profile.objects.all()
    projects = Project.objects.filter(company=company)
    return render(request, 'companies/home.html',
                  {'company': company, 'profiles': profiles, 'projects': projects})


def signup_company(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        company_form = CompanyForm(request.POST)
        if form.is_valid() and company_form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            new_company = company_form.save(commit=False)
            new_company.user = user
            new_company.save()
            login(request, user)
            return redirect('company_home')
    else:
        form = UserCreationForm()
        company_form = CompanyForm()
    return render(request, 'registration/signup_company.html', {'form': form, 'company_form': company_form})


@login_required
def profile_update(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        update_profile_form = ProfileForm(request.POST, request.FILES)

        if update_profile_form.is_valid():
            profile = update_profile_form.save(commit=False)
            if "gravatar" in request.POST:
                user_email = update_profile_form.cleaned_data['email']
                gravatar_url  = get_gravatar_url(user_email, size=150)
                profile.photo = gravatar_url
            else:
                img = request.FILES['new_photo']
                uploaded_file = upload(img, api_key='981758619657849', api_secret='MxjoWH06DMotcKyJXaF3VMtVKxc',
                                   cloud_name='ddodjetvf')

                profile.photo = uploaded_file['secure_url']

            profile.save()
            update_profile_form.save_m2m()
            return JsonResponse({"success": True, "message": "update success"})
        else:
            return JsonResponse({"success": False, 'errors': update_profile_form.errors.as_json()})

    profile = get_profile(request.user)
    update_profile_form = ProfileForm(instance=profile)

    return render(request, 'freelancers/update.html', {'form': update_profile_form, 'profile': profile})


def add_experience(request, pk):
    profile = get_profile(request.user)
    if request.method == 'POST':
        experience_form = ExperienceForm(request.POST or None, instance=profile)
        if experience_form.is_valid():
            experience_form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission error')

    a = Profile.objects.get(pk=pk)
    experience_form = ExperienceForm(instance=a)
    return render(request, 'freelancers/experience.html', {'form': experience_form, 'profile': profile})


def add_education(request, pk):
    profile = get_profile(request.user)
    if request.method == 'POST':
        education_form = EducationForm(request.POST or None, instance=profile)
        if education_form.is_valid():
            education_form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission error')

    a = Profile.objects.get(pk=pk)
    education_form = EducationForm(instance=a)
    return render(request, 'freelancers/education.html', {'form': education_form, 'profile': profile})


@login_required
def add_profile_skills(request):
    if request.method == 'POST':
        form = ProfileSkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')

    else:
        form = ProfileSkillForm()

    return render(request, 'freelancers/add_profile_skills.html', {'form': form})


@login_required
def add_profile(request):
    profile = get_profile(request.user)

    if request.method == 'POST':
        add_profile_form = ProfileForm(request.POST, request.FILES)
        experience_form = ExperienceForm(request.POST)

        if add_profile_form.is_valid():
            new_profile = add_profile_form.save(commit=False)
            new_profile.user = request.user

            if "gravatar" in request.POST:
                user_email = add_profile_form.cleaned_data['email']
                gravatar_url  = get_gravatar_url(user_email, size=150)
                new_profile.photo = gravatar_url
            else:
                img = request.FILES['photo']
                uploaded_file = upload(img, api_key='981758619657849', api_secret='MxjoWH06DMotcKyJXaF3VMtVKxc',
                                   cloud_name='ddodjetvf')
                new_profile.photo = uploaded_file['secure_url']

            new_profile.save()
            add_profile_form.save_m2m()
            add_profile_form = ProfileForm(instance=new_profile)
            experience_form = ExperienceForm()
            messages.success(request, 'Form submission successful')
            return JsonResponse({"success": True})
        else:
            messages.error(request, 'Form submission error')
            return JsonResponse({"success": False})
    else:
        add_profile_form = ProfileForm()
        experience_form = ExperienceForm()

    if request.is_ajax():
        return JsonResponse({"is ajax": True})
    else:
        return render(request, 'freelancers/add.html', {'form': add_profile_form, 'form_experience': experience_form,
                                                    'profile': profile})


def cloudinary(request):
    img = upload("http://e.snmc.io/lk/f/l/0a8c67d6c371be990b798182d04a5dbd/1243875.jpg", api_key = '981758619657849',
                 api_secret='MxjoWH06DMotcKyJXaF3VMtVKxc', cloud_name='ddodjetvf')
    return render(request, 'freelancers/cloudinary.html', {'img': img})


def gravatar(request):
    g_url = get_gravatar_url('isaacmiliani@gmail.com', size=150)
    image_stream = urlopen(g_url)
    user = request.user
    profile = get_profile(user)
    profile.photo = g_url

    profile.save()
    gravatar_exists = has_gravatar('isaacmiliani@gmail.com')
    profile_url = get_gravatar_profile_url('isaacmiliani@gmail.com')
    email_hash = calculate_gravatar_hash('isaacmiliani@gmail.com')

    return render(request, 'freelancers/gravatar.html',{'url':g_url, 'gravatar_exists':gravatar_exists,
                                                       'profile_url':profile_url, 'email_hash':email_hash } )


def get_profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    return profile


def get_profiles(profile):
    if profile:
        profiles = Profile.objects.filter(~Q(pk=profile.id))
    else:
        profiles = Profile.objects.all()

    return profiles


def home(request):
    template_name = 'freelancers/home.html'
    user = request.user
    profile = get_profile(user)
    profiles = get_profiles(profile)
    projects = Project.objects.all()
    data = {'profiles': profiles, 'profile': profile, 'projects': projects}
    return render(request, template_name, data)


@login_required
def user_settings(request):
    user = request.user
    profile = get_profile(user)
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'freelancers/home.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect,
        'profile': profile
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})


def get_company(user):
    try:
        company = Company.objects.get(user = user)
    except Company.DoesNotExist:
        company = None

    return company


def index(request):
    user = request.user
    if user.is_authenticated():
        company = get_company(user)
        if company:
            return redirect('company_home')
        else:
            return redirect('home')
    else:
        profiles = Profile.objects.all()
        projects = Project.objects.all()
        data = {'profiles': profiles, 'projects': projects, 'profile': None}
        return render(request, 'index.html', data)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def my_fetcher(url):
    if url.startswith('assets://'):
        url = url[len('assets://'):]
        url = "file://" + safe_join(settings.ASSETS_ROOT, url)
    else:
        return default_url_fetcher(url)


def django_fm(request):
    return render(request, 'freelancers/django_fm.html')


class ExperienceCreateView(AjaxCreateView):
    form_class = ExperienceForm

class EducationCreateView(AjaxCreateView):
    form_class = EducationForm

class ContractCreateView(AjaxCreateView):
    form_class = ContractForm

class KindOfTaskCreateView(AjaxCreateView):
    form_class = KindOfTaskForm

class ExpendedTimeCreateView(AjaxCreateView):
    form_class = ExpendedTimeForm

class CategoryCreateView(AjaxCreateView):
    form_class = CategoryForm

class InvoiceCreateView(AjaxCreateView):
    form_class = InvoiceForm

class ExpenseCreateView(AjaxCreateView):
    form_class = ExpenseForm

def cv(request, pk):
    profile = Profile.objects.get(pk=pk)
    education = Education.objects.filter(profile=profile)
    experience = Experience.objects.filter(profile=profile)

    return render(request, 'freelancers/cv.html', {'profile': profile, 'studies': education, 'experiences': experience})


def cv_to_pdf(request, pk):
    profile = Profile.objects.get(pk=pk)
    education = Education.objects.filter(profile=profile)
    experience = Experience.objects.filter(profile=profile)

    html_template = get_template('freelancers/cv_to_pdf.html')

    rendered_html = html_template.render(RequestContext(request, {'profile': profile, 'studies': education, 'experiences': experience})).encode(encoding="UTF-8")
    pdf_file = HTML(string=rendered_html,base_url=request.build_absolute_uri(), url_fetcher=my_fetcher).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + 'css/cv.css'), CSS(settings.STATIC_ROOT + 'css/reset.css'), CSS(settings.STATIC_ROOT + 'css/print.css')])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="cv.pdf"'

    return http_response