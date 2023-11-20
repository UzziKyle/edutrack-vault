from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contribute.auth.urls')), 
    path('register/', views.register, name='register'),
]
