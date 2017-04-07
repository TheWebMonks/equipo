from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
    	return self.name
