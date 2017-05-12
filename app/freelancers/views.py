from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.db.models import Q
from django.http import HttpResponse
from django.views import generic
from django.views.generic.detail import DetailView

from .models import Profile, Project, Skill, Company
from .forms import ProfileForm, ProfileSkillForm, ExperienceForm, ProjectForm, CompanyForm, RegistrationForm

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


def index(request):
    profiles = Profile.objects.all()
    projects_list = Project.objects.all()
    return render(request, 'index.html', {'profiles': profiles, 'projects': projects_list})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


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
            return redirect('home_company')
    else:
        form = UserCreationForm()
        company_form = CompanyForm()
    return render(request, 'registration/signup_company.html', {'form': form, 'company_form': company_form})


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


@login_required
def home(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        company = None

    if company:
        company = Company.objects.get(user=request.user)
        profiles = Profile.objects.all()
        projects_list = Project.objects.all()
        return render(request, 'companies/home.html', {'company': company, 'profiles': profiles, 'projects': projects_list})
    else:
        profile = get_profile(user=request.user)
        profiles = get_profiles(profile)
        projects_list = Project.objects.all()
        return render(request, 'freelancers/home.html', {'profiles': profiles, 'profile': profile, 'projects': projects_list})


def projects(request):
    projects_all = Project.objects.all()
    return render(request, 'freelancers/projects.html', {'projects': projects_all})


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
            messages.success(request, 'Form submission successful')

    add_profile_form = ProfileForm()
    form_experience = ExperienceForm()

    return render(request, 'freelancers/add.html', {'form': add_profile_form, 'form_experience': form_experience,
                                                    'profile': profile})


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
def update_profile(request, pk):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        update_profile_form = ProfileForm(request.POST or None, instance=profile)

        if update_profile_form.is_valid():
            update_profile_form.save()
            messages.success(request, 'Form submission successful')

    else:
        a = Profile.objects.get(pk=pk)
        update_profile_form = ProfileForm(instance=a)

    return render(request, 'freelancers/update.html', {'form': update_profile_form, 'profile': profile})


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