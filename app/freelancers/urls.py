from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
# https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
app_name = 'freelancers'
urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^update_profile/(?P<pk>[0-9]+)/$', views.update_profile, name='update_profile'),
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    url(r'^add_profile_skills/$', views.add_profile_skills, name='add_profile_skill'),
]
