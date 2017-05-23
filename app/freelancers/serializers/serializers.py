from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ..models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.save()
        return instance


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ('tag', 'description')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'last_name', 'email', 'birthday', 'experiences', 'skills', 'personal_page')

        # user = serializers.OneToOneField(User)
        # name = serializers.CharField(max_length=200)
        # last_name = serializers.CharField(max_length=200)
        # email = serializers.CharField(max_length=50)
        # birthday = serializers.DateField()
        skills = SkillSerializer(many=True)  # A nested
        # experiences = serializers.ManyToManyField(Experience)


class SocialAccountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialAccounts
        fields = ('name', 'description', 'web_address')


class TypeOfContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeOfContract
        fields = ('name', 'description')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('user', 'name', 'email', 'web_page', 'description', 'social_accounts')

        social_accounts = SocialAccountsSerializer(many=True)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('company', 'description', 'required_skills', 'type_of_contract', 'date', 'freelancers')

        required_skills = SkillSerializer(many=True)  # A nested
        type_of_contract = TypeOfContractSerializer()
        freelancers = ProfileSerializer(many=True)