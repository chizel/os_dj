# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from userprofile.models import UserProfile, PrivateMessage

#hidden_form = forms.CharField(widget=forms.HiddenInput())
#field_that_not_required = forms.BooleanField(required=False)

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'username',
            'placeholder':'Username',
            }
        ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'password',
            'placeholedr':'Password',
            }
        ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'id':'email',
            'placeholder':'Email',
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

#class PrivateMessageForm(forms.ModelForm):
    #message = forms.TextInput()

    #class Meta:
        #model = PrivateMessage
#        fields = ('message',)
