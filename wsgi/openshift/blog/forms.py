# -*- coding: utf-8 -*-
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
