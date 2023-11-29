from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegistrationForm(UserCreationForm):
    user_type_choices = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
        ('alumni', 'Alumni')
    ]
    user_type = forms.ChoiceField(choices=user_type_choices, widget=forms.Select)


    class Meta:
        model=CustomUser
        fields = ['username', 'email', 'user_type', 'ID_no', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
