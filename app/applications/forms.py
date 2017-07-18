from django import forms
from . import models
from django.forms import Select


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = models.Applicant
        fields = ['email', 'name', 'reason', 'story', 'achievement']


class CommentForm(forms.ModelForm):


    class Meta:
        model = models.Comment
        fields = ['comment']

