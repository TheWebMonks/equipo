from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Skill(models.Model):
    tag = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.tag

    class Meta:
        ordering = ('tag',)


class Experience(models.Model):
    role = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):  # __unicode__ on Python 2
        return self.role

    class Meta:
        ordering = ('role',)


class SocialAccounts(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    web_address = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    skills = models.ManyToManyField(Skill)
    experiences = models.ManyToManyField(Experience)
    personal_page = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class TypeOfContract(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Company(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50, null=True)
    web_page = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)
    social_accounts = models.ManyToManyField(SocialAccounts)


class Project(models.Model):
    company = models.ForeignKey(Company)
    description = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    type_of_contract = models.ForeignKey(TypeOfContract)
    date = models.DateField()
    freelancers = models.ManyToManyField(Profile)

