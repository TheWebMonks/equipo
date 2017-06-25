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


class ProfileType(models.Model):
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ('type',)


class SocialNetwork(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    user = models.OneToOneField(User)
    type = models.ForeignKey(ProfileType)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    skills = models.ManyToManyField(Skill)
    resume = models.CharField(max_length=100)
    personal_page = models.CharField(max_length=100, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True, default='https://secure.gravatar.com/avatar/hash.jpg?size=150')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    profile = models.ForeignKey(Profile)
    web_address = models.CharField(max_length=100)
    name = models.ForeignKey(SocialNetwork)

    def __str__(self):  # __unicode__ on Python 2
        return self.web_address

    class Meta:
        ordering = ('name',)


def set_upload_to(self, path):
    return path


class Experience(models.Model):
    profile = models.ForeignKey(Profile)
    place = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):  # __unicode__ on Python 2
        return self.role

    class Meta:
        ordering = ('role',)


class Education(models.Model):
    profile = models.ForeignKey(Profile)
    university = models.CharField(max_length=100)
    degree = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField()

    def __str__(self):  # __unicode__ on Python 2
        return self.university

    class Meta:
        ordering = ('university',)


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
    logo = models.CharField(max_length=200, blank=True, null=True,
                             default='https://secure.gravatar.com/avatar/hash.jpg?size=150')


class Project(models.Model):
    company = models.ForeignKey(Company)
    description = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    type_of_contract = models.ForeignKey(TypeOfContract)
    date = models.DateField()
    freelancers = models.ManyToManyField(Profile)