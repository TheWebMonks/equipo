from django.db import models
from django.contrib.auth.models import User

class Applicant(models.Model):
    """
    Freelancers who want to join the network
    """

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    reason = models.TextField(max_length=255, null=True)
    story = models.TextField(max_length=511, null=True)
    achievement = models.TextField(max_length=511, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    Admins can comment on applications by applicants
    """

    applicant = models.ForeignKey(Applicant)
    admin = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=255)

    def __str__(self):
        return str(self.admin) + ' commented on ' + str(self.applicant) + ' at ' + str(self.date)
