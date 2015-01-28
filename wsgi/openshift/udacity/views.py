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


def rot13(request):
    in_text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    out_text = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
    answer = ''

    if request.method == 'POST':
        text = request.POST['text']

        for i in text:
            pos = in_text.find(i)
            if pos >= 0:
                answer = answer + out_text[pos]
            else:
                answer = answer + i

    context = RequestContext(request)
    return render_to_response('udacity/rot13.html',
                                  {'answer': answer},
                                  context)


@require_GET
def show(request):
    context = RequestContext(request)
    return render_to_response('udacity/show.html',
                                  {'form': form},
                                  context)


