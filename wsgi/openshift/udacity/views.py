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
from django.views.generic import ListView



def hello(request):
    return HttpResponse('Hello, Udacity!')

@require_GET
def show(request):
    context = RequestContext(request)
    return render_to_response('udacity/show.html',
                                  {'form': form},
                                  context)


