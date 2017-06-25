from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from rest_framework import routers
from . import viewsets
# https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html

import debug_toolbar

from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'groups', viewsets.GroupViewSet)
router.register(r'profiles', viewsets.ProfileViewSet)
router.register(r'skills', viewsets.SkillViewSet)
router.register(r'typeofcontract', viewsets.TypeOfContractViewSet)
router.register(r'company', viewsets.CompanyViewSet)
router.register(r'projects', viewsets.ProjectViewSet)
router.register(r'education', viewsets.EducationViewSet)
router.register(r'experience', viewsets.ExperienceViewSet)
router.register(r'socialnetworks', viewsets.SocialNetworkViewSet)
router.register(r'socialaccounts', viewsets.SocialAccountViewSet)

schema_view = get_swagger_view(title='Pastebin API')

app_name = 'freelancers'

urlpatterns = [
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^user_settings/$', views.user_settings, name='user_settings'),
    url(r'^user_settings/password/$', views.password, name='password'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^profile_update/$', views.profile_update, name='profile_update'),
    url(r'^apply_project/(?P<pk>[0-9]+)/$', views.apply_project, name='apply_project'),
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    url(r'^add_experience/(?P<pk>[0-9]+)/$', views.add_experience, name='add_experience'),
    url(r'^add_education/(?P<pk>[0-9]+)/$', views.add_education, name='add_education'),
    url(r'^add_profile_skills/$', views.add_profile_skills, name='add_profile_skill'),
    url(r'^browse_projects/$', views.browse_projects, name='browse_projects'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^view_project/(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='view_project'),
    url(r'^signup_company/$', views.signup_company, name='signup_company'),
    url(r'^view_profile/(?P<pk>[0-9]+)/$', views.view_profile, name='view_profile'),
    url(r'^my_projects/$', views.my_projects, name='my_projects'),
    url(r'^gravatar/$', views.gravatar, name='gravatar'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.project, name='project'),
    url(r'^company/home/$', views.company_home, name='company_home'),
    url(r'^cloudinary/$', views.cloudinary, name='cloudinary'),
    url(r'^cv/(?P<pk>[0-9]+)/$', views.cv, name='cv'),
    url(r'^cv_to_pdf/(?P<pk>[0-9]+)/$', views.cv_to_pdf, name='cv_to_pdf'),
    url(r'^django_fm/$', views.django_fm, name='django_fm'),
    url(r'^create_experience/$', views.ExperienceCreateView.as_view(), name='create_experience'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^docs/$', schema_view)
]

if settings.IS_WSGI:
    print("uWSGI mode, adding static file patterns")
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)