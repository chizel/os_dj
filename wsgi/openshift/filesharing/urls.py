# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from filesharing.views import SectionsList, FilesList, FileDetail

urlpatterns = patterns(
    '',
    url(r'^$', SectionsList.as_view(), name='files_sections'),
    url(r'^(?P<section_name>[A-Za-z0-9_- ]+)/$', FilesList.as_view(), name='files_list'),
    url(r'^(?P<section_name>[A-Za-z0-9_- ]+)/(?P<file_id>\d+)/$', FilesList.as_view(), name='files_list'),
    )
