# -*- coding: utf-8 -*-
import re

from django import forms
from django.contrib.auth.models import User

from blog.models import BlogPost, BlogPostComment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'body')

    title = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'title',
                'placeholder': 'Post title',
                }
            ),
        required=True,
        )

    body = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'body',
                'placeholder': 'Write your post',
                }
            ),
        required=True,
        )

    tags = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Tags (comma-separated)',
                }
            ),
        required=False,
        )

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        r = re.compile('^[\w ,]+$')

        if r.match(tags):
            return tags
        else:
            raise forms.ValidationError(
                ('Invalid value! Tags must contain "A-Za-z0-9_" " "(space)\
                        and "," for separation!'), code='invalid')


class BlogPostCommentForm(forms.ModelForm):
    class Meta:
        model = BlogPostComment
        fields = ('comment', )

    comment = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'comment',
                'placeholder': 'Write your comment',
                }
            ),
        required=True,
        )
