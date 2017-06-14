from django.forms import ModelForm
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.utils.safestring import mark_safe
from string import Template
import  django.template.loader
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


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


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs={ 'width':'150', 'height':'150'}):
        html = Template("""<img src="$link"/>""")

        return mark_safe(html.substitute(link=value))


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['type','name', 'last_name', 'email', 'birthday', 'skills', 'personal_page', 'photo']
        widgets = {
            'birthday': DateInput(),
            'photo': PictureWidget(),
        }


class SkillForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = ['tag', 'description']


class SocialNetworkForm(ModelForm):
    class Meta:
        model = models.SocialNetwork
        fields = ['name']


class SocialAccount(ModelForm):
    class Meta:
        model = models.SocialAccount
        fields = ['web_address','profile', 'name']


class ExperienceForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = ['role', 'description', 'date']
        widgets = {
            'date': DateInput(),
        }


class EducationForm(ModelForm):
    class Meta:
        model = models.Education
        fields = ['university', 'degree', 'date']
        widgets = {
            'date': DateInput(),
        }


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
        fields = ['name', 'email', 'web_page', 'description', 'logo']
        widgets = {
            'logo': PictureWidget(),
        }