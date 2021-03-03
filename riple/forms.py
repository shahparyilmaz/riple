from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
'''        
class LogInForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1']
'''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age','profile_pic']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption','pic']