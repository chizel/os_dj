from django.conf.urls import patterns, url
from forum import views
from forum.views import ThemesList

urlpatterns = patterns('',
    url(r'^$', ThemesList.as_view(), name='list_of_themes'),
    #url(r'^$', views.list_of_themes, name='list_of_themes'),
    url(r'^(?P<theme_id>\d+)/$', views.view_theme, name='theme'),
    url(r'^(?P<theme_id>\d+)/(?P<page>\d+)/$', views.view_theme, name='theme'),
    url(r'^create_theme/$', views.create_theme, name='create_theme'),
    #posts
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
    )
