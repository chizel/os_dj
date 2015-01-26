from django.shortcuts import redirect, render_to_response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_get, require_post
from django.contrib.auth.decorators import login_required
from django.http import httpresponse, httpresponseredirect
from django.contrib.auth import authenticate, login, logout
from django.template import requestcontext
from django.contrib.auth.models import user
from django.db.models import f
from django.core.paginator import paginator, emptypage, pagenotaninteger
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import listview


def h(request):
    return HttpResponse('Hello, Udacity!')

@require_GET
def show(request):
    context = RequestContext(request)
    return render_to_response('udacity/show.html',
                                  {'form': form},
                                  context)


