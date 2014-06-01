from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404
from annoying.functions import get_object_or_None
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.template import RequestContext

from userprofile.models import UserProfile
from models import BlogPost, BlogPostComment, Tag

def list_of_posts(request, page=1):
    posts_list = get_list_or_404(BlogPost)
    paginator = Paginator(posts_list, 5)
    context = RequestContext(request)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render_to_response(
                'blog/list_of_posts.html',
                {
                    'posts':posts,
                    'title': 'Posts',
                },
                context
                )

@login_required
def add_post(request):
    context = RequestContext(request)

    #show form for add post
    if not request.method == 'POST':
        return render_to_response(
                'blog/add_post.html',
                {},
                context
                )

    if not request.POST['title'] or not request.POST['post']:
        return redirect('blog:add_post')

    new_post = BlogPost()
    new_post.title = request.POST['title']
    new_post.body= request.POST['post']
    new_post.user_id= request.user.id
    new_post.save()

#!!! tags may contain only A-Za-z0-9 -
    if request.POST['tags']:
        tags = request.POST['tags'].split(',')

        if len(tags) > 10:
            return HttpResponse('Amount of tags can\'t be more than 10!')

        tags = [tag.strip() for tag in tags]

        #delete repetitions
        tags = list(set(tags))
        res = ''
        for tag in tags:
            new_tag = get_object_or_None(Tag, name=tag)

            if not new_tag:
                new_tag = Tag(name=tag)
                new_tag.save()
            new_post.tag.add(new_tag)

    #??? may be add to user's profile count of blog's post???
    #UserProfile.objects.filter(pk=request.user.id).update(count_blog_posts=F('count_blog_posts')+1)
    return redirect('blog:list_of_posts')

   
def show_post(request, post_id):
    context = RequestContext(request)
    post = get_object_or_404(BlogPost, pk=post_id)
    comments = BlogPostComment.objects.all().filter(post_id=post_id)

    return render_to_response(
            'blog/show_post.html',
            {
                'post':post,
                'comments':comments,
            },
            context
            )

@login_required
def add_comment(request):
    return HttpResponse()

def create_tag(requst, tag):
    tag = tag.trip(tag)

    if not tag:
        return

    tag_exist = Tag.objects.get(name=tag)

    if not tag_exist:
        new_tag = Tag(name=tag)
        new_tag.save()

def show_tag(request, tag, page=1):
    #show all posts that contains current tag
    search_tag = get_object_or_404(Tag, name=tag)
    context = RequestContext(request)
    posts_list = BlogPost.objects.all().filter(tag=search_tag.id)
    paginator = Paginator(posts_list, 5)

    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render_to_response(
            'blog/list_of_posts.html',
            {
                'posts':posts,
                'tag':search_tag,
                'title': 'Posts by "%s" tag' % search_tag.name,
            },
            context
            )

@login_required
def view_user_blogposts(request, user_id, page=1):
    context = RequestContext(request)
    user = get_object_or_404(UserProfile, pk=user_id)
#!!! add if user haven't any posts - show message
#not 404 page !!!
    posts_list = get_list_or_404(BlogPost, user_id = user_id)
    paginator = Paginator(posts_list, 5)

    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render_to_response(
            'blog/list_of_posts.html',
            {
                'posts':posts,
                'title': '%s\'s posts' %user.user.username,
            },
            context
            )

@login_required
def add_comment(request, blogpost_id, parent_comment=0):
    if not 'comment' in request.POST or not request.POST['comment'].strip():
        return redirect(reverse('blog:show_post', args=[blogpost_id]))

    context = RequestContext(request)
    post = get_object_or_404(BlogPost, pk=blogpost_id)
    new_comment = BlogPostComment()
    new_comment.user_id = request.user.id
    new_comment.post_id = blogpost_id
    new_comment.parent_comment = parent_comment
    new_comment.comment = request.POST['comment']
    new_comment.save()
    post.increment_count_comments()

    return redirect(reverse('blog:show_post', args=[blogpost_id]))
