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


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experience
        fields = ('profile', 'role', 'description', 'date')


class EducationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Education
        fields = ('profile', 'university', 'degree', 'date')



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'last_name', 'email', 'birthday', 'skills', 'personal_page')

        skills = SkillSerializer(many=True)  # A nested


class SocialNetworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('name',)


class SocialAccountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('profile','name', 'web_address')


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