from django.forms import ModelForm
from django import forms

from . import models


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['name', 'last_name', 'email', 'birthday', 'skills']


class SkillForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = ['tag', 'description']


class ProfileSkillForm(ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=models.Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.Skill
        fields = ['tag', 'description']
