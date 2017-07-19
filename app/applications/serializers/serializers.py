from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ..models import *


class ApplicantSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Applicant
        fields = ('email', 'name', 'reason', 'story', 'achievement')


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = ('applicant', 'admin', 'date', 'comment')

