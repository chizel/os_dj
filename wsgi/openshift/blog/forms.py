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
        required=True,
        help_text='Blogpost\'s title',
        )

    body = forms.CharField(
        max_length=3000,
        required=True,
        help_text='Blogpost\'s title',
        )

    tags = forms.CharField(
        max_length=120,
        required=False,
        help_text='Blogpost\'s tags',
        )

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        
        if not tags:
            return

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
        help_text='Blogpost\'s comment',
        )
