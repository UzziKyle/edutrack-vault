from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/edit', views.edit_profile, name='profile-edit'),
]
