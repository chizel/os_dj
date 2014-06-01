from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.list_of_posts, name='list_of_posts'),
    url(r'^(?P<page>\d+)/$', views.list_of_posts, name='list_of_posts'),
    url(r'^user/((?P<page>\d+)/)?$', views.view_user_blogposts, name='user_bps'),
    url(r'^tag/(?P<tag>[A-Za-z0-9 -_]+)/$', views.show_tag, name='show_tag'),
    url(r'^tag/(?P<tag>[A-Za-z0-9 -_]+)/(?P<page>\d+)/$', views.show_tag, name='show_tag'),

    url(r'^post/(?P<post_id>\d+)/$', views.show_post, name='show_post'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^add_comment/(?P<blogpost_id>\d+)/$', views.add_comment, name='add_comment'),
   )
