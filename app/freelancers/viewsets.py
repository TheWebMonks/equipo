from .serializers import serializers
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, renderers


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Skill.objects.all()
    serializer_class = serializers.SkillSerializer


class TypeOfContractViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TypeOfContract.objects.all()
    serializer_class = serializers.TypeOfContractSerializer


class SocialNetworkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SocialNetwork.objects.all()
    serializer_class = serializers.SocialNetworkSerializer


class SocialAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SocialAccount.objects.all()
    serializer_class = serializers.SocialAccountsSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    # renderer_classes = (TemplateHTMLRenderer,)


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Experience.objects.all()
    serializer_class = serializers.ExperienceSerializer
    # renderer_classes = (TemplateHTMLRenderer,)


class EducationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Education.objects.all()
    serializer_class = serializers.EducationSerializer
    # renderer_classes = (TemplateHTMLRenderer,)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
