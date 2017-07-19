from .serializers import serializers
from .models import *
from rest_framework import viewsets


class ApplicantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Applicant.objects.all()
    serializer_class = serializers.ApplicantSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
