from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
# https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
if settings.DEBUG:
    import debug_toolbar

app_name = 'freelancers'

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^update_profile/(?P<pk>[0-9]+)/$', views.update_profile, name='update_profile'),
    url(r'^apply_project/(?P<pk>[0-9]+)/$', views.apply_project, name='apply_project'),
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    url(r'^add_experience/$', views.add_experience, name='add_experience'),
    url(r'^add_profile_skills/$', views.add_profile_skills, name='add_profile_skill'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^view_project/(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='view_project'),
    url(r'^signup_company/$', views.signup_company, name='signup_company'),
    url(r'^view_profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='view_profile'),

]
