# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from forum.models import Branch, Theme, Post


class CreateThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ('name',)

    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Themename',
                }
            ),
        required=True,
        )

    first_post = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'first_post',
                'placeholder': 'Write your post',
                }
            ),
        required=True,
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

    post = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'post',
                'placeholder': 'Write your post',
                }
            ),
        required=True,
        )
