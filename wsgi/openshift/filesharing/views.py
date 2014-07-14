from django.shortcuts import redirect, render_to_response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from filesharing.models import Section, File


class SectionsList(ListView):
    model = Section
    context_object_name = 'sections'
    paginate_by = 5

class FilesList(ListView):
    model = File
    context_object_name = 'files'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(FilesList, self).get_context_data(**kwargs)
        return context


    def get_queryset(self):
        return get_list_or_404(File, section=self.kwargs.get('section_id'))


class FileDetail(DetailView):
    model = File
