import re
import hashlib

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

from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_user(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        login(request, user)
        url = reverse('udacity:regok')
        response = HttpResponseRedirect(url)
        response['Set-Cookie'] = 'user_id=24; Path=/;'
        return response
    return render_to_response('udacity/login.html',
                              context) 


@csrf_exempt
def signup(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

        if not USER_RE.match(username):
            return render_to_response('udacity/signup.html',
                                      {'username_error': 'Username invalid!'},
                                      context)

        email = request.POST.get('email', '')
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

        if email and not EMAIL_RE.match(email):
            return render_to_response('udacity/signup.html',
                                      {'email_error': 'Email invalid!'},
                                      context)

        password = request.POST.get('password', '')

        if len(password) < 3 or len(password) > 20:
            return render_to_response(
                'udacity/signup.html',
                {'password_error':
                 'Password length must be more 3 and less 20 characters!'},
                context)

        verify = request.POST['verify']

        if not verify == password:
            return render_to_response('udacity/signup.html',
                                      {'verify_error':
                                          'Passwords aren\'t match!'},
                                      context)

        if User.objects.filter(username=username).count():
            return render_to_response('udacity/signup.html',
                                      {'username_error':
                                          'Username exist!'},
                                      context)
 
        user = User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(request, user)

        url = reverse('udacity:regok')
        response = HttpResponseRedirect(url)
        #response = HttpResponse()
        #response.set_cookie( 'user_id', 2981)
        response['Set-Cookie'] = 'user_id=%s; Path=/;' % hashlib.sha256(username).hexdigest()
        return response
    return render_to_response('udacity/signup.html',
                              context)


@require_GET
def regok(request):
    if request.user.is_authenticated():
        username = request.user.username

        if not request.COOKIES.get('user_id') == hashlib.sha256(username).hexdigest():
            url = reverse('udacity:signup')
            return HttpResponseRedirect(url)

    response = HttpResponse('Hello, %s!' % username)
    #response['Set-Cookie'] = 'user_id=24; Path=/;'
    return response


@csrf_exempt
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


def hello(request):
    return HttpResponse('Hello, Udacity!')
