# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from userprofile.models import UserProfile, PrivateMessage


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'username',
                   'placeholder': 'Username'}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholedr': 'Password',
                }
            ),
        )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Email',
                }
            ),
        )


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'username',
                'placeholder': 'Username',
                }
            ),
        required=True
        )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholedr': 'Password',
                }
            ),
        required=True
        )


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about_me', 'website')
        exclude = ('EditUser',)

    check_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'check_password',
                'placeholedr': 'Your password (required)',
                }
        ),
        required=True
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'new_password',
                'placeholedr': 'New password',
                }
        ),
        required=False
    )

    about_me = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'about_me',
                'placeholder': 'Write something about you',
                }
            ),
        required=False,
        )

    website = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'id': 'website',
                'placeholder': 'Your website',
                }
            ),
        required=False,
        )

    new_avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'id': 'avatar',
                }
            ),
        required=False,
        )


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ('title', 'message',)

    title = forms.CharField(
        max_length=25,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'title',
                'placeholder': 'Title',
                }
            ),
        required=True,
        )

    message = forms.CharField(
        max_length=300,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'about_me',
                'placeholder': 'Write your message',
                }
            ),
        required=True,
        )
