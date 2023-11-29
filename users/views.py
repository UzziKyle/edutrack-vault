from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm, UserProfileForm
from .models import CustomUser


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('home')
            
        messages.error(request, f'Invalid username or password.')
        return render(request, 'users/login.html', {'form': form})
  
    
def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


def sign_up(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully!')
            login(request, user)
            return redirect('home')
        
        else:
            return render(request, 'users/register.html', {'form': form})


@login_required
def view_profile(request):
    context = {}
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None
    context['user'] = user
    context['profile'] = profile
    context['title'] = 'Profile'

    return render(request, 'users/profile.html', context)


@login_required   
def edit_profile(request):
    context = {}
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None
    context['title'] = 'Edit Profile'
    
    if request.method == 'GET':
        context['form'] = UserProfileForm(instance=profile)
        context['profile'] = profile
        
        return render(request, 'users/edit_profile.html', context)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            
            return redirect('profile')

        else:
            context['form'] = form
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'edit_profile.html', context)
        