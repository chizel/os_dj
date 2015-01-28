from django.conf.urls import patterns, url
from udacity import views

urlpatterns = patterns(
    '',
    url(r'^hello/$', views.hello),
    url(r'^rot13/$', views.rot13, name='rot13'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^regok$', views.regok, name='regok'),
    )
