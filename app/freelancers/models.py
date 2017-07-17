from django.db import models
from django.contrib.auth.models import User
from .utils import Currency


# Create your models here.


class Skill(models.Model):
    """
    The skills a freelancer(User) possesses.
    """

    tag = models.CharField(max_length=20)
    description = models.TextField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.tag

    class Meta:
        ordering = ('tag',)


class ProfileType(models.Model):
    """
    The profile type of a user, eg. Developer, Designer, Manager, Network Engineer, ...
    """

    type = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ('type',)


class SocialNetwork(models.Model):
    """
    The different possible social networks.
    """

    name = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    """
    Profile of the freelancer(User).
    """

    user = models.OneToOneField(User)
    type = models.ForeignKey(ProfileType)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    skills = models.ManyToManyField(Skill)
    resume = models.CharField(max_length=100)
    personal_page = models.CharField(max_length=100, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True,
                             default='https://secure.gravatar.com/avatar/hash.jpg?size=150')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    """
    Social accounts of the freelancers(Users).
    """

    user = models.ForeignKey(User)
    web_address = models.CharField(max_length=255)
    name = models.ForeignKey(SocialNetwork)

    def __str__(self):  # __unicode__ on Python 2
        return self.web_address

    class Meta:
        ordering = ('name',)


def set_upload_to(self, path):
    return path


class Experience(models.Model):
    """
    Experiences of the freelancers(Users).
    """

    profile = models.ForeignKey(Profile)
    place = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    date = models.DateField()

    def __str__(self):  # __unicode__ on Python 2
        return self.role

    class Meta:
        ordering = ('role',)


class Education(models.Model):
    """
    The Education(s) a freelancer(User) completed.
    """

    profile = models.ForeignKey(Profile)
    university = models.CharField(max_length=100)
    degree = models.CharField(max_length=200)
    description = models.TextField(max_length=200, null=True)
    date = models.DateField()

    def __str__(self):  # __unicode__ on Python 2
        return self.university

    class Meta:
        ordering = ('university',)


class TypeOfContract(models.Model):
    """
    The type of contract decided between freelancer(User) and Company, eg. Hourly, Monthly, 1 time payment.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Company(models.Model):
    """
    The companies that are subscribed to Equipo.
    """

    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, null=True)
    web_page = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=200, null=True)
    logo = models.CharField(max_length=200, blank=True, null=True,
                            default='https://secure.gravatar.com/avatar/hash.jpg?size=150')

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    A project offered by a company on which users can participate.
    """

    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    description = models.TextField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    date = models.DateField()
    freelancers = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name


class Contract(models.Model):
    """
    A contract made between freelancer(User) and company is done per Project.
    The contract also saves the type and price agreement, eg. hourly and 14$.
    """

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    unit_type = models.ForeignKey(TypeOfContract)
    unit_price = models.FloatField(default=0.0)
    currency = models.CharField(
        max_length=3,
        choices=Currency.CURRENCY_CHOICES,
        default=Currency.EURO
    )

    def __str__(self):
        return 'Contract (' + str(self.user) + ' - ' + str(self.project) + ')'


class KindOfTask(models.Model):
    """
    The type of task on which time was expended, eg. Development, Design, Planning, ...
    """

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.name


class ExpendedTime(models.Model):
    """
    The time expended (per task) on a project.
    """

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    kind_of_task = models.ForeignKey(KindOfTask)
    notes = models.TextField(max_length=200, null=True)
    time = models.IntegerField(
        default=0,
        help_text='Time spent on the task in seconds. Time registered through start and stop time will be '
                  'automatically added to this field'
    )
    start_time = models.DateTimeField(
        null=True,
        help_text='Start time of the task.'
    )
    stop_time = models.DateTimeField(
        null=True,
        help_text="Stop time of the task. This time needs to be of a higher date then start_time. Setting this field "
                  "means the amount of time spent on the task will be added to the current 'time'."
    )

    def __str__(self):
        return str(self.project) + ' (' + str(self.time) + ')'


class Category(models.Model):
    """
    The category of the expense made, eg. Entertainment, Mileage, Lodging, Transportation, Meals, ...
    """

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Expense(models.Model):
    """
    A fixed cost made by a freelancer(User) on a project.
    """

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    category = models.ForeignKey(Category)
    notes = models.TextField(max_length=200, null=True)
    amount = models.FloatField(default=0.0)
    date = models.DateTimeField()
    currency = models.CharField(
        max_length=3,
        choices=Currency.CURRENCY_CHOICES,
        default=Currency.EURO
    )

    def __str__(self):
        return str(self.project) + ' ' + str(self.amount)


class Invoice(models.Model):
    """
    Invoices created for a project by a user.
    """

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    date_generated = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()

    def __str__(self):
        return str(self.project) + ' - ' + str(self.date_generated)
