from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from rest_framework import routers
from . import viewsets
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static

router = routers.SimpleRouter()

router.register(r'applicants', viewsets.ApplicantViewSet)
router.register(r'comments', viewsets.CommentViewSet)

app_name = 'applications'

urlpatterns = [
    url(r'^apply/', views.apply, name='apply'),
    url(r'^all/', views.get_all, name='all-applications'),
    url(r'^applicant/(?P<pk>[0-9]+)/create-comment', views.create_comment, name='create-comment'),
    url(r'^applicant/(?P<pk>[0-9]+)/$', views.applicant, name='applicant'),
    url(r'^comment/edit/(?P<pk>[0-9]+)/$', views.edit_comment, name='edit-comment'),
]