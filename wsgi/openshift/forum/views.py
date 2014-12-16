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
        context['pag_url'] = reverse('forum:list_of_themes')
        return context

    def get_queryset(self):
        return get_list_or_404(Theme)


class PostsList(ListView):
    model = Post
    template_name = 'forum/theme.html'
    context_object_name = 'posts'
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.theme_id = self.kwargs.get('theme_id')
        return super(PostsList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PostsList, self).get_context_data(**kwargs)
        context['form'] = PostForm()

        # data for pagination
        context['pag_url'] = reverse('forum:theme',
                                     kwargs={'theme_id': self.theme_id})
        context['theme'] = get_object_or_404(Theme, pk=self.theme_id)
        return context

    def get_queryset(self):
        return get_list_or_404(Post, theme_id=self.theme_id)


def create_post(theme_id, post_body, user_id):
    theme = get_object_or_404(Theme, pk=int(theme_id))
    user_id = int(user_id)
    post = Post()
    post.theme_id = theme.id
    post.post = post_body
    post.user_id = user_id
    post.save()

    # increment count of posts in author's profile
    UserProfile.objects.filter(pk=user_id).update(
        count_messages=F('count_messages')+1)
    theme.increment_count_posts()
    return True


@require_POST
@login_required
def add_post(request, theme_id):
    form = PostForm(request.POST)

    if form.is_valid():
        create_post(
            theme_id,
            form.cleaned_data['post'],
            request.user.id)

    # redirecting to the last page
    posts_list = get_list_or_404(Post, theme_id=theme_id)
    paginator = Paginator(posts_list, 5)

    url = reverse('forum:theme', args=[theme_id, paginator.num_pages])
    return HttpResponseRedirect(url)


def create_theme(theme_name, first_post, user_id):
    theme = Theme()
    theme.user_id = user_id
    theme.last_user_id = user_id
    theme.branch_id = 1
    theme.name = theme_name
    theme.save()

    # create first post in new theme
    create_post(theme.id, first_post, user_id)
    return theme.id


@login_required
def add_theme(request):
    form = CreateThemeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        theme_id = create_theme(
            form.cleaned_data['name'],
            form.cleaned_data['first_post'],
            request.user.id)

        return HttpResponseRedirect(reverse('forum:theme',
                                    args=[theme_id]))
    else:
        context = RequestContext(request)
        return render_to_response('forum/create_theme.html',
                                  {'form': form},
                                  context)


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

    # redirect to the last page
    posts_list = get_list_or_404(Post, theme_id=theme_id)
    paginator = Paginator(posts_list, 5)
    url = reverse('forum:theme', args=[theme_id, paginator.num_pages])

    return HttpResponseRedirect(url)
