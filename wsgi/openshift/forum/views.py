from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from forum.models import Branch, Theme, Post
from userprofile.forms import UserForm, UserProfileForm
from userprofile.models import UserProfile
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.utils.decorators import method_decorator
from django.views.generic import ListView

class PostList(ListView):

    model = Post

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PostList, self).dispatch(request, *args, **kwargs)

class ThemesList(ListView):
    model = Theme

    template_name = 'forum/index.html'
    context_object_name = 'themes'
    paginate_by = 5

    def get_queryset(self):
        qs = Theme.objects.order_by('id')
        return qs

def list_of_themes(request):
    #!!! add pagination
    themes = Theme.objects.order_by('id')
    return render(
            request,
            'forum/index.html',
            {'themes': themes}
            )

@login_required
def create_theme(request):
    if request.method == 'POST' and 'theme_name' in request.POST and 'first_post' in request.POST:
        new_theme = Theme()
        new_theme.author_id = request.user.id
        new_theme.name = request.POST['theme_name']
        new_theme.count_posts = 1
        #!!!add branches!!!
        new_theme.branch_id = 1
        new_theme.save()

        new_post = Post()
        new_post.theme_id = new_theme.id
        new_post.post = request.POST['first_post']
        new_post.user_id = request.user.id
        UserProfile.objects.filter(pk=request.user.id).update(count_messages=F('count_messages')+1)
        #new_post.save()
        #return HttpResponseRedirect(reverse('forum:theme' 
        #url = reverse('forum:theme', args=[theme.id, paginator.num_pages])
        return HttpResponse(str(new_theme.id))
     
    else:
        #show creation form
        return render(
                request,
                'forum/create_theme.html',
                {}
                )

def view_theme(request, theme_id, page=1):
    posts_list = get_list_or_404(Post, theme_id=theme_id)
    paginator = Paginator(posts_list, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    theme = get_object_or_404(Theme, pk=theme_id)

    return render(
            request,
            'forum/theme.html', 
            {'posts': posts, 'theme': theme}
            )

@require_POST
@login_required
def add_post(request):
    if not 'post' in request.POST or not request.POST['post'].strip():
        return redirect(reverse('blog:list_of_posts'))

    theme = get_object_or_404(Theme, pk=request.POST['theme_id']) 
    new_post = Post()
    new_post.theme_id = theme.id
    new_post.post = request.POST['post']
    new_post.user_id = request.user.id
    UserProfile.objects.filter(pk=request.user.id).update(count_messages=F('count_messages')+1)
    new_post.save()
    theme.increment_count_posts()

    #redirection to the last page
    posts_list = get_list_or_404(Post, theme_id=theme.id)
    paginator = Paginator(posts_list, 5)
    url = reverse('forum:theme', args=[theme.id, paginator.num_pages])

    return HttpResponseRedirect(url)

@require_GET
@login_required
def delete_post(request, post_id):
    context = RequestContext(request)
    post = get_object_or_404(Post, pk=post_id)
    theme_id = post.theme.id
    last_post = Post.objects.filter(theme=theme_id).order_by('-id')[:1][0]

    if not post.id == last_post.id:
        message = 'Error! Your post is not the last!'
        title = 'Error!'
        return render_to_response(
                'forum/notification.html',
                {'title':title, 'message':message},
                context
                )

    theme = get_object_or_404(Theme, pk=theme_id)
    
    if not post.user_id == request.user.id:
        message = 'Error! You can delete only your messages!'
        title = 'Error!'
        return render_to_response(
                'forum/notification.html',
                {'title':title, 'message':message},
                context
                )

    Post.objects.filter(pk=post_id).delete()
    UserProfile.objects.filter(pk=request.user.id).update(count_messages=F('count_messages')-1)
    theme.decrement_count_posts()

    #redirection to the last page
    posts_list = get_list_or_404(Post, theme_id=theme_id)
    paginator = Paginator(posts_list, 5)
    url = reverse('forum:theme', args=[theme_id, paginator.num_pages])

    return HttpResponseRedirect(url)
