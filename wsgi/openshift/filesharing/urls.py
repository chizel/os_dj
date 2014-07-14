# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from filesharing.views import SectionsList, FilesList, FileDetail

urlpatterns = patterns(
    '',
    url(r'^$', SectionsList.as_view(), name='files_sections'),
    url(r'^(?P<section_id>\d+)/$', FilesList.as_view(), name='files_list'),
    url(r'^file/(?P<file_id>\d+)/$', FileDetail.as_view(), name='view_file'),
    )
