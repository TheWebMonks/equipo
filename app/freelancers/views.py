from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

from django.http import HttpResponse
from .models import Profile
from django.template import loader
from django.urls import reverse
from django.views import generic
from .forms import ProfileForm
from .forms import SkillForm
from .forms import ProfileSkillForm


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'freelancers/home.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Profile.objects.order_by('id')


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


@login_required
def home(request):
    return render(request, 'freelancers/home.html')


@login_required
def settings(request):
    user = request.user

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

    return render(request, 'freelancers/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
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
    return render(request, 'freelancers/password.html', {'form': form})

def add_profile(request):
    if request.method == 'POST':
        add_profile_form = ProfileForm(request.POST)

        if add_profile_form.is_valid():
            new_profile = add_profile_form.save();
            return HttpResponse("<h3>Thanks<h3> <li><a href='/'>Return to index</a></li>")
    else:
        add_profile_form = ProfileForm()

    return render(request, 'freelancers/add.html', {'add_profile_form': add_profile_form})

@login_required
def update_profile(request, pk):
    if request.method == 'POST':
        instance = get_object_or_404(Profile, pk=pk)
        update_profile_form = ProfileForm(request.POST or None, instance=instance)
        if update_profile_form.is_valid():
            update_profile_form.save();
            return HttpResponse("<h3>Thanks<h3> <li><a href='/'>Return to index</a></li>")
    else:
        a = Profile.objects.get(pk=pk)
        update_profile_form = ProfileForm(instance=a)

    return render(request, 'freelancers/update.html', {'form': update_profile_form, 'id': pk})


def add_profile_skills(request):
    if request.method == 'POST':
        form = ProfileSkillForm(request.POST)

        if form.is_valid():
            new_skill = form.save();
            return HttpResponse("<h3>Thanks<h3> <li><a href='/'>Return to index</a></li>")

    else:
        form = ProfileSkillForm()

    return render(request, 'freelancers/add_profile_skills.html', {'form': form})