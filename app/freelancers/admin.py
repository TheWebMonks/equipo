from django.contrib import admin

# Register your models here.
from .models import Profile, Skill, TypeOfContract, Project, Company, ProfileType, SocialNetwork, Contract, Invoice,\
    ExpendedTime, KindOfTask, Expense, Category

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(TypeOfContract)
admin.site.register(Project)
admin.site.register(Company)
admin.site.register(ProfileType)
admin.site.register(SocialNetwork)
admin.site.register(Contract)
admin.site.register(Invoice)
admin.site.register(ExpendedTime)
admin.site.register(KindOfTask)
admin.site.register(Expense)
admin.site.register(Category)