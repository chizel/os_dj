# coding: utf-8

from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
    url(r'^login/$', views.user_login, name='login'),
    url(r'^login/social/$', views.user_loginsocial, name='loginsocial'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^registration/$', views.user_registration, name='registration'),

    #profile
    url(r'^(?P<user_id>\d+)/$', views.user_profile, name='profile'),
    url(r'^edit/$', views.user_profile_edit, name='edit_profile'),
    url(r'^delete/$', views.user_profile_delete, name='delete_profile'),

    #private messages
    url(
        r'^send_private_message/(?P<to_user>\d+)/$',
        views.show_pm_form, name='show_pm_form'
        ),
    url(r'^send_private_message/$', views.send_pm, name='send_pm'),
    url(r'^private_messages/$', views.show_pms, name='show_pms'),
    url(r'^read_private_message/(?P<pm_id>\d+)/$', views.read_pm, name='read_pm'),
    url(r'^delete_pm/(?P<pm_id>\d+)/$', views.delete_pm, name='delete_pm'),
    )
