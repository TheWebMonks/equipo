from django import forms
from . import models


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = models.Applicant
        fields = ['email', 'name', 'reason', 'story', 'achievement']


class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['comment']


class ApplicantForm(forms.ModelForm):

    class Meta:
        model = models.Applicant
        fields = ['email', 'name', 'reason', 'story', 'achievement']
