from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# The skills a freelancer(User) possesses.
class Skill(models.Model):
    tag = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.tag

    class Meta:
        ordering = ('tag',)


# The profile type of a user, eg. Developer, Designer, Manager, Network Engineer, ...
class ProfileType(models.Model):
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ('type',)


# The different possible social networks.
class SocialNetwork(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)


# Profile of the freelancer(User)
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


# Social accounts of the freelancers(Users)
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


# Experiences of the freelancers(Users)
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


# The Education(s) a freelancer(User) completed.
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


# The type of contract decided between freelancer(User) and Company, eg. Hourly, Monthly, 1 time payment.
class TypeOfContract(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


#The companies that are subscribed to Equipo
class Company(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, null=True)
    web_page = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=200, null=True)
    logo = models.CharField(max_length=200, blank=True, null=True,
                             default='https://secure.gravatar.com/avatar/hash.jpg?size=150')


# A project offered by a company on which users can participate.
class Project(models.Model):
    company = models.ForeignKey(Company)
    description = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    # TODO: delete ToC? Now saved in 'Contract'.
    type_of_contract = models.ForeignKey(TypeOfContract)
    date = models.DateField()
    freelancers = models.ManyToManyField(Profile)


# A contract made between freelancer(User) and company is done per Project.
# The contract also saves the type and price agreement, eg. hourly and 14$.
class Contract(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    type_of_contract = models.ForeignKey(TypeOfContract)
    price = models.FloatField(default=0.0)


# The type of task on which time was expended, eg. Development, Design, Planning, ...
class KindOfTask(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)


# The time expended (per task) on a project.
# TODO: add foreign key to user if multiple users per project are possible.
class ExpendedTime(models.Model):
    project = models.ForeignKey(Project)
    kind_of_task = models.ForeignKey(KindOfTask)
    notes = models.CharField(max_length=200, null=True)
    time = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True)
    stop_time = models.DateTimeField(null=True)


# The category of the expense made, eg. Entertainment, Mileage, Lodging, Transportation, Meals, ...
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


# A fixed cost made by a freelancer(User) on a project.
# TODO: add foreign key to user if multiple users per project are possible.
class Expense(models.Model):
    category = models.ForeignKey(Category)
    notes = models.CharField(max_length=200, null=True)
    amount = models.FloatField(default=0.0)


# Invoices created for a project
# TODO: add foreign key to user if multiple users per project are possible.
class Invoice(models.Model):
    project = models.ForeignKey(Project)
    date_generated = models.DateTimeField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()


