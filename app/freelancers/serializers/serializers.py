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
    skills = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='tag'
    )

    class Meta:
        model = Profile
        fields = ('user', 'name', 'last_name', 'email', 'birthday', 'skills', 'personal_page')


class SocialNetworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('name',)


class SocialAccountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('user', 'name', 'web_address')


class TypeOfContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeOfContract
        fields = ('name', 'description')


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('user', 'name', 'email', 'web_page', 'description')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    required_skills = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='tag'
    )
    freelancers = ProfileSerializer(many=True)

    class Meta:
        model = Project
        fields = ('name', 'company', 'description', 'required_skills', 'date', 'freelancers')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')


class KindOfTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KindOfTask
        fields = ('name', 'description')


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Expense
        fields = ('user', 'project', 'category', 'notes', 'amount', 'date')


class ExpendedTimeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpendedTime
        fields = ('user', 'project', 'kind_of_task', 'notes', 'time', 'start_time', 'stop_time')


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='project-detail'
    )
    unit_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Contract
        fields = ('user', 'project', 'unit_type', 'unit_price', 'currency')


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Invoice
        fields = ('user', 'project', 'date_generated', 'start_time', 'stop_time')
