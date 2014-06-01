# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #user's data
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    #about_me = models.CharField(max_lenght=300, blank=True)

    #system fields
    count_messages = models.PositiveSmallIntegerField(default=0)
    unread_pm = models.PositiveSmallIntegerField(default=0)

    def increment_count_messages(self):
        self.count_messages += 1
        self.save()

    def decrement_count_messages(self):
        if self.count_messages > 0:
            self.count_messages -= 1
        else:
            self.count_messages = 0
        self.save()

    def increment_unread_pm(self):
        self.unread_pm += 1
        self.save()

    def decrement_unread_pm(self):
        if self.unread_pm > 0:
            self.unread_pm -= 1
        else:
            self.unread_pm = 0
        self.save()

    def get_absolute_url(self):
        return '/user/%i/' % self.user.id

    def __unicode__(self):
        return self.user.username

class PrivateMessage(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=300)
    sent = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)
    to_user = models.ForeignKey(UserProfile, related_name='_to_user')
    from_user = models.ForeignKey(UserProfile, related_name='_from_user')
    title = models.CharField(max_length=25)

    def set_readed(self):
        self.readed = True
        self.save()

    def __unicode__(self):
        return self.message

    def __repr__(self):
        return '<PrivateMessage %r>' % (self.message)
