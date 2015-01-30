from django.conf.urls import patterns, url
from udacity import views

urlpatterns = patterns(
    '',
    url(r'^hello/$', views.hello),
    url(r'^rot13/$', views.rot13, name='rot13'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^regok$', views.regok, name='regok'),
    )
