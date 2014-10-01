from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns(
    '',
    # list of blogposts
    url(r'^$', views.BlogPostList.as_view(), name='list_of_posts'),
    url(r'^(?P<page>\d+)/$', views.BlogPostList.as_view(),
        name='list_of_posts'),

    # list of posts by tag
    url(r'^tag/(?P<tag>[A-Za-z0-9 -_]+)/(?P<page>\d+)/$',
        views.BlogTagList.as_view(), name='show_tag'),
    url(r'^tag/(?P<tag>[A-Za-z0-9 -_]+)/$',
        views.BlogTagList.as_view(), name='show_tag'),

    # list of user's posts
    url(r'^user/(?P<uid>\d+)/(?P<page>\d+)/$',
        views.UserBlogPostList.as_view(), name='user_bps'),
    url(r'^user/(?P<uid>\d+)/$',
        views.UserBlogPostList.as_view(), name='user_bps'),

    # show post
    url(r'^post/(?P<pk>\d+)/$', views.ShowPost.as_view(), name='show_post'),

    # add post
    url(r'^add_post/$', views.add_post, name='add_post'),

    # add comment
    url(r'^add_comment/(?P<blogpost_id>\d+)/$',
        views.add_comment, name='add_comment'),

    # show comment
    url(r'^comment/(?P<pk>\d+)/$', views.ShowComment.as_view(),
        name='show_comment'),
)
