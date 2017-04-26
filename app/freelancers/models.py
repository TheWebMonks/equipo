from django.db import models


# Create your models here.

class Skill(models.Model):
    tag = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.tag

    class Meta:
        ordering = ('tag',)


class Profile(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name
