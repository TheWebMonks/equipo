from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import ProfileForm, ProfileSkillForm, ExperienceForm, ProjectForm, CompanyForm, RegistrationForm
from django.views import generic
from social_django.models import UserSocialAuth
from django.db.models import Q
# Create your views here.


class ProjectView(generic.DetailView):
    model = Project

    template_name = 'freelancers/project.html'

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


@login_required
def add_project(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

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
    return render(request, 'companies/project.html', {'project': this_project})

def browse_projects(request):
    projects_all = Project.objects.all()
    return render(request, 'freelancers/projects.html', {'projects': projects_all})

def my_projects(request):
    company = Company.objects.get(user=request.user)
    projects = Project.objects.filter(company=company)
    return render(request, 'companies/projects.html', {'projects': projects})

@login_required
def apply_project(request, pk):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        company = None

    if company:
        messages.error(request, 'You must create a profile as freelance')
        return redirect('/view_project/' + pk)

    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

        if profile:
            project.freelancers.add(profile)
            project.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'You must create a profile')

        return redirect('/view_project/' + pk)


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
def update_profile(self, pk):
    try:
        profile = Profile.objects.get(user=self.user)
    except Profile.DoesNotExist:
        profile = None

    if self.method == 'POST':
        update_profile_form = ProfileForm(self.POST or None, instance=profile)

        if update_profile_form.is_valid():
            update_profile_form.save()
            messages.success(self, 'Form submission successful')

    else:
        a = Profile.objects.get(pk=pk)
        update_profile_form = ProfileForm(instance=a)

    return render(self, 'freelancers/update.html', {'form': update_profile_form, 'profile': profile})

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
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        add_profile_form = ProfileForm(request.POST)

        if add_profile_form.is_valid():
            new_profile = add_profile_form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            add_profile_form.save_m2m()
            messages.success(request, 'Form submission successful')

    add_profile_form = ProfileForm()
    form_experience = ExperienceForm()

    return render(request, 'freelancers/add.html', {'form': add_profile_form, 'form_experience': form_experience,
                                                    'profile': profile})

@login_required
def add_experience(request):
    if request.method == 'POST':
        add_experience_form = ExperienceForm(request.POST)

        if add_experience_form.is_valid():
            new_experience = add_experience_form.save()
            messages.success(request, 'Form submission successful')
    else:
        add_experience_form = ProfileForm()

    return render(request, 'freelancers/add.html', {'form': add_experience_form})



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
def settings(request):
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

    return render(request, 'registration/settings.html', {
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