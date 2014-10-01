from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from annoying.functions import get_object_or_None
from django.http import HttpResponse
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from userprofile.models import UserProfile
from models import BlogPost, BlogPostComment, Tag
from forms import BlogPostForm, BlogPostCommentForm


@login_required
def search_posts(request):
    q = request.GET['q']
    return


class BlogPostList(ListView):
    '''Show list of blogposts'''
    model = BlogPost
    template_name = 'blog/list_of_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostList, self).get_context_data(**kwargs)
        context['title'] = 'Blog posts'
        context['pag_url'] = reverse('blog:list_of_posts')
        return context


class BlogTagList(BlogPostList):
    '''Show list of blogposts by tag'''
    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(Tag, name=self.kwargs.get('tag'))
        return super(BlogTagList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostList, self).get_context_data(**kwargs)
        context['title'] = self.tag.name
        context['pag_url'] = reverse('blog:show_tag',
                                     kwargs={'tag': self.tag.name})
        return context

    def get_queryset(self):
        return get_list_or_404(BlogPost, tag=self.tag)


class UserBlogPostList(BlogPostList):
    '''Show list of user's blogposts'''
    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(UserProfile,
                                      pk=self.kwargs.get('uid'))
        return super(BlogPostList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BlogPostList, self).get_context_data(**kwargs)
        context['title'] = str(self.user.user.username) + '\'s posts by tag'
        context['pag_url'] = reverse('blog:user_bps',
                                     kwargs={'uid': self.user.id})
        context['user'] = self.user
        return context

    def get_queryset(self):
        return get_list_or_404(BlogPost, user=self.user)


class ShowPost(DetailView):
    ''''Show post'''
    model = BlogPost

    def get_context_data(self, *args, **kwargs):
        context = super(ShowPost, self).get_context_data(**kwargs)
        context['form'] = BlogPostCommentForm()
        context['comments'] = BlogPostComment.objects.filter(
            post_id=self.kwargs.get('pk'))
        return context


class ShowComment(DetailView):
    '''Show blogpost's comment with child comments'''
    model = BlogPostComment

    def get_context_data(self, *args, **kwargs):
        context = super(ShowComment, self).get_context_data(**kwargs)
        #context['form'] = BlogPostCommentForm()
        context['comments'] = BlogPostComment.objects.filter(
            parent_comment=self.kwargs.get('pk'))
        return context


@login_required
def add_post(request):
    '''Add new blogpost'''
    form = BlogPostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_post = form.save(commit=False)
        new_post.user_id = request.user.id
        new_post.save()

        if form.cleaned_data['tags']:
            list_tags = request.POST['tags'].split(',')
            list_tags = [tag.strip() for tag in list_tags]
            list_tags = set(list_tags)

            if len(list_tags) > 10:
                return HttpResponse('Amount of tags can\'t be more than 10!')

            for tag in list_tags:
                if tag:
                    new_tag, created = Tag.objects.get_or_create(name=tag)
                    new_post.tag.add(new_tag.id)

        # ??? may be add to user's profile count of blog's post???
        # UserProfile.objects.filter(pk=request.user.id).update(count_blog_posts=F('count_blog_posts')+1)
        return redirect('blog:list_of_posts')
    else:
        context = RequestContext(request)
        return render_to_response('blog/add_post.html',
                                  {'form': form}, context)


@login_required
@require_POST
def add_comment(request, blogpost_id, pid=0):
    ''' add comment to blogpost
    pid=0 means that comment haven't any parents comment
    '''
    form = BlogPostCommentForm(request.POST)

    if form.is_valid():
        post = get_object_or_404(BlogPost, pk=blogpost_id)
        new_comment = form.save(commit=False)
        new_comment.user_id = request.user.id
        new_comment.post_id = blogpost_id
        new_comment.parent_comment = pid
        new_comment.save()
        post.increment_count_comments()

    return redirect(reverse('blog:show_post', args=[blogpost_id]))
