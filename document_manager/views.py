from django.shortcuts import render
from users.models import CustomUser
from users.forms import UserProfileForm

def home(request):
    return render(request, 'document_manager/index.html')

def profile_view(request):
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
        
    
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'document_manager/profile.html', {'form': form, 'profile': profile})

