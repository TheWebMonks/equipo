from django.conf.urls import url
from . import views

app_name = 'freelancers'
urlpatterns = [
     # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.update_profile, name='update_profile'),
    # ex: /
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<pk>[0-9]+)/vote/$', views.vote, name='vote'),
]