# coding: utf-8

from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, redirect
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from userprofile.models import UserProfile, PrivateMessage
from userprofile.forms import UserForm, UserProfileForm

def user_loginsocial(request):
    return render_to_response('userprofile/loginsocial.html')

def user_login(request):
    if request.user.is_authenticated():
        return redirect('/')

    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if 'next' in request.POST:
            NEXT = request.POST['next']
        else:
            NEXT = '/'
               
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(NEXT)
            else:
                message = 'Your account is disabled.'
                title = 'Error!'
                return render_to_response(
                        'basesite/notification.html',
                        {'title':title, 'message':message},
                        context
                        )
        else:
            error = "Invalid login details supplied."
            return render_to_response(
                    'userprofile/login.html',
                    {'next':NEXT, 'error':error},
                    context
                    )
    else:
        if 'next' in request.GET:
            NEXT = request.GET['next']
        else:
            NEXT = None

        return render_to_response(
                'userprofile/login.html',
                {'next':NEXT},
                context
                )

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

def user_registration(request):
    if request.user.is_authenticated():
        return redirect('/')

    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
            registered = True
    else:
        user_form = UserForm()

    return render_to_response(
            'userprofile/registration.html',
            {
                'user_form': user_form,
                'registered': registered
            },
            context)
 
def user_profile(request, user_id):
    curr_user = get_object_or_404(User, pk=user_id)
    curr_user_profile = get_object_or_404(UserProfile, pk=user_id)
    context = RequestContext(request)
    return render_to_response(
            'userprofile/profile.html',
            {'curr_user':curr_user, 'curr_user_profile':curr_user_profile},
            context,
            )

@login_required
def user_profile_edit(request):
    context = RequestContext(request)

    if request.method == 'POST':
        pass
    else:
        return render_to_response('userprofile/edit_profile.html', {}, context) 

@login_required
def user_profile_delete(request, user_id):
    if not request.user.id == user_id:
        message = 'You can\'t delete not your account!'
        title = 'Error!'
        return render_to_response(
                'forum/notification.html',
                {'title':title, 'message':message},
                context
                )

    logout(request)
    message = 'Your account was deleted!'
    title = 'Ok!'
    return render_to_response(
            'forum/notification.html',
            {'title':title, 'message':message},
            context
            )
  
@login_required
@require_GET
def show_pm_form(request, to_user):
    user = get_object_or_404(User, pk=to_user)
    context = RequestContext(request, {})
    return render_to_response(
            'userprofile/send_pm.html',
            {'to_user':user,},
            context,
            ) 


@login_required
@require_POST
def send_pm(request):
    context = RequestContext(request)
    pm = PrivateMessage()
    title = 'Error!'

    if not 'to_user' in request.POST or not int(request.POST['to_user']):
        message = 'Wrong user!'
    elif not 'message' in request.POST or request.POST['message'] == '':
        message = 'Wrong message!'
    elif not 'title' in request.POST or request.POST['title'] == '':
        message = 'Wrong title!'
    else:
        pm.message = request.POST['message']
        pm.to_user_id = int(request.POST['to_user'])
        pm.title = request.POST['title']
        pm.from_user_id = request.user.id
        to_user = get_object_or_404(UserProfile, pk=pm.to_user_id)
        pm.save()
        to_user.increment_unread_pm()
        message = 'Your message have been sent!'
        title = 'Ok!'

    return render_to_response(
            'forum/notification.html',
            {'title':title, 'message':message},
            context
            )

@login_required
def show_pms(request):
#!!! add pagination
    #pms = get_list_or_404(PrivateMessage, to_user_id=request.user.id)
    context = RequestContext(request)
    pms = PrivateMessage.objects.filter(to_user_id=request.user.id)

    if not pms:
        message = 'You haven\'t any private messages!'
        return render_to_response(
                'forum/notification.html',
                {'message':message},
                context
                )

    return render_to_response(
            'userprofile/show_pms.html',
            {'pms':pms},
            context
            )

 
@login_required
def read_pm(request, pm_id):
    pm = get_object_or_404(PrivateMessage, pk=pm_id)
    context = RequestContext(request)

    if not pm.to_user.id == request.user.id:
        message = 'Error! You can\'t read this message!'
        title = 'Error!'
        return render_to_response(
                'forum/notification.html',
                {'title':title, 'message':message},
                context
                )

    if not pm.readed:
        pm.set_readed()
        pm.to_user.decrement_unread_pm()


    return render_to_response(
            'userprofile/read_pm.html',
            {'pm':pm},
            context
            )

@login_required
def delete_pm(request, pm_id):
    pm = get_object_or_404(PrivateMessage, pk=pm_id)

    if not pm.to_user.id == request.user.id:
        message = 'Error! You can\'t delete this message!' 
        title = 'Error!'
        context = RequestContext(request)
        return render_to_response(
                'forum/notification.html',
                {'title':title, 'message':message},
                context
                )

    pm.delete()
    pm.to_user.decrement_unread_pm()

    return redirect('userprofile:show_pms')
