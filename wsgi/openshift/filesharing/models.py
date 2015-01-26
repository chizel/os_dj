from django.db import models

from userprofile.models import UserProfile


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    files_amount = models.IntegerField(default=0)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, related_name='_section')
    # hash 32 + dot 1 + extension 1-7
    name = models.CharField(max_length=40)
    display_name = models.CharField(max_length=120)
    description = models.CharField(max_length=3000)
    user = models.ForeignKey(UserProfile, related_name='_file_author')
    added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    # size = models.
