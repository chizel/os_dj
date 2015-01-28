from django.conf.urls import patterns, url
from udacity import views

urlpatterns = patterns(
    '',
    url(r'^hello/$', views.hello),
    url(r'^rot13/$', views.rot13, name='rot13'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^regok$', views.regok, name='regok'),
    #url(r'^regok/(?P<username>[a-zA-Z0-9_-]{3,20})$', views.regok, name='regok'),
   # ThemesList.as_view(), name='list_of_themes'),
    #url(r'^(?P<page>\d+)/$', ThemesList.as_view(), name='list_of_themes'),

    ## themes
    #url(r'^theme/(?P<theme_id>\d+)/(?P<page>\d+)/$',
        #PostsList.as_view(), name='theme'),
    #url(r'^theme/(?P<theme_id>\d+)/$', PostsList.as_view(), name='theme'),

    ## create theme
    #url(r'^create_theme/$', views.add_theme, name='create_theme'),

    ## posts
    #url(r'^add_post/(?P<theme_id>\d+)/$', views.add_post, name='add_post'),
    #url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post,
   #     name='delete_post'),
    )
