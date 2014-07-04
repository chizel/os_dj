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

from forum.models import Branch, Theme, Post
from forum.forms import CreateThemeForm, PostForm
from userprofile.models import UserProfile


class ThemesList(ListView):
    model = Theme
    template_name = 'forum/index.html'
    context_object_name = 'themes'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(ThemesList, self).get_context_data(**kwargs)
        return context


    def get_queryset(self):
        return get_list_or_404(Theme)


class PostsList(ListView):
    model = Post
    template_name = 'forum/theme.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(PostsList, self).get_context_data(**kwargs)
        context['theme'] = get_object_or_404(
            Theme,
            pk=self.kwargs.get("theme_id")
            )
        return context

    def get_queryset(self):
        return get_list_or_404(Post, theme_id=self.kwargs.get("theme_id"))


@login_required
def create_theme(request):
    if request.method == 'POST':

        form = CreateThemeForm(request.POST)
        new_theme = form.save(commit=False)
        new_theme.user_id = request.user.id
        new_theme.last_user_id = request.user.id
        new_theme.branch_id = 1
        new_theme.save()

        new_post = Post()
        new_post.theme_id = new_theme.id
        new_post.post = form.cleaned_data['first_post']
        new_post.user_id = request.user.id
        UserProfile.objects.filter(pk=request.user.id).update(
            count_messages=F('count_messages')+1)
        new_post.save()
        return HttpResponseRedirect(reverse('forum:theme',
                                    args=[new_theme.id]))
    else:
        form = CreateThemeForm()
        context = RequestContext(request)
        return render_to_response('forum/create_theme.html',
                                  {'form': form},
                                  context)


@require_POST
@login_required
def add_post(request):
    if 'post' not in request.POST or not request.POST['post'].strip():
        return redirect(reverse('blog:list_of_posts'))

    theme = get_object_or_404(Theme, pk=request.POST['theme_id'])
    new_post = Post()
    new_post.theme_id = theme.id
    new_post.post = request.POST['post']
    new_post.user_id = request.user.id
    UserProfile.objects.filter(pk=request.user.id).update(
        count_messages=F('count_messages')+1)
    new_post.save()
    theme.increment_count_posts()

    # redirection to the last page
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
            {'title': title, 'message': message},
            context
            )

    theme = get_object_or_404(Theme, pk=theme_id)

    if not post.user_id == request.user.id:
        message = 'Error! You can delete only your messages!'
        title = 'Error!'
        return render_to_response(
            'forum/notification.html',
            {'title': title, 'message': message},
            context
            )

    Post.objects.filter(pk=post_id).delete()
    UserProfile.objects.filter(pk=request.user.id).update(
        count_messages=F('count_messages')-1)
    theme.decrement_count_posts()

    # redirection to the last page
    posts_list = get_list_or_404(Post, theme_id=theme_id)
    paginator = Paginator(posts_list, 5)
    url = reverse('forum:theme', args=[theme_id, paginator.num_pages])

    return HttpResponseRedirect(url)
