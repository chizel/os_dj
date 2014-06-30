from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from userprofile.models import UserProfile


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    count_themes = models.IntegerField(default=0)

    def delete_branch(self, id):
        pass

    def __unicode__(self):
        return self.name


class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, related_name='_branch')
    name = models.CharField(max_length=120)
    user = models.ForeignKey(UserProfile, related_name='_author')
    created = models.DateTimeField(auto_now_add=True)
    last_post = models.DateTimeField(auto_now_add=True)
    last_user = models.ForeignKey(UserProfile, related_name='_last_author')
    count_posts = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)

    def increment_count_posts(self):
        self.count_posts += 1
        self.save()

    def decrement_count_posts(self):
        if self.count_posts < 1:
            self.count_posts = 0
        else:
            self.count_posts -= 1
        self.save()

    def delete_theme(self, id):
        clear_theme(id)

    def clear_theme(self, id):
        posts = Post.objects.all(theme_id=self.id)

        for i in range(1, len(posts)):
            post[i].user.decrement_count_messages()

        self.last_author = posts[0].user.id
        self.last_post = posts[0].created
        self.count_posts = 1

    def close_theme(self, id):
        self.closed = True
        self.save()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.ForeignKey(Theme, related_name='_theme_id')
    post = models.CharField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile, related_name='_user_id')

    def delete_post(self, id):
        # decrement number of messages post's user and theme
        self.user.decrement_count_messages()
        # self.delete()
        pass

    def edit_post(self, id):
        # if post.user_id == user.id:
        pass

    def __unicode__(self):
        return self.post

    def __repr__(self):
        return '<Post %r>' % (self.post)
