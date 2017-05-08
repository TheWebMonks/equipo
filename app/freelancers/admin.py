from django.contrib import admin

# Register your models here.
from .models import Profile, Skill, TypeOfContract, Project, Company

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(TypeOfContract)
admin.site.register(Project)
admin.site.register(Company)