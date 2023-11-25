from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('folder/edit/<int:id>/', views.edit_folder, name='folder-edit'),
    path('folder/delete/<int:id>/', views.delete_folder, name='folder-delete'),
    path('folder/open/<int:id>/', views.open_folder, name='folder-open'),
    path('file/edit/<int:id>/', views.edit_file, name='file-edit'),
    path('file/delete/<int:id>/', views.delete_file, name='file-delete'),
    path('file/download<int:id>', views.download_file, name='file-download'),
    ]