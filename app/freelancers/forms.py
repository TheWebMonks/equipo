from django.forms import ModelForm
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from . import models
import datetime


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
            raise forms.ValidationError('Username is already taken.')

        raise forms.ValidationError('Passwords do not match.')


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['name', 'last_name', 'email', 'birthday', 'skills', 'personal_page']
        widgets = {
            'birthday': DateInput(),
        }


class SkillForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = ['tag', 'description']


class ExperienceForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = ['role', 'description', 'date']


class TypeOfContractForm(ModelForm):
    class Meta:
        model = models.TypeOfContract
        fields = ['name', 'description']


class ProfileSkillForm(ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=models.Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.Skill
        fields = ['tag', 'description']


class ProjectContractForm(ModelForm):
    type_of_contract = forms.ModelMultipleChoiceField(
        queryset=models.TypeOfContract.objects.all(),
        widget=forms.Select)

    class Meta:
        model = models.TypeOfContract
        fields = ['name', 'description']


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ['description', 'type_of_contract', 'required_skills']


class CompanyForm(ModelForm):
    class Meta:
        model = models.Company
        fields = ['name']