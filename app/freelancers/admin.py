from django.contrib import admin

# Register your models here.
from .models import Profile, Skill, TypeOfContract, Project, Company, ProfileType, SocialNetwork, SocialAccount, \
    Experience, Education, Contract, Invoice,ExpendedTime, KindOfTask, Expense, Category

"""
 Profile
"""
class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('skills',)
    fieldsets = (
        ('User', {
            'fields': ('photo', ('user', 'type'), ('name', 'last_name'), 'birthday'),
        }),
        ('Profile', {
            'fields': ('personal_page', 'skills', 'resume'),
        }),
        ('Contact', {
            'classes': ('collapse',),
            'fields': ('email', ('country', 'city'), 'telephone'),
        }),
    )

admin.site.register(Profile, ProfileAdmin)


"""
 The rest
"""
admin.site.register(Skill)
admin.site.register(TypeOfContract)
admin.site.register(Project)
admin.site.register(Company)
admin.site.register(ProfileType)
admin.site.register(SocialNetwork)
admin.site.register(SocialAccount)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Contract)
admin.site.register(Invoice)
admin.site.register(ExpendedTime)
admin.site.register(KindOfTask)
admin.site.register(Expense)
admin.site.register(Category)
