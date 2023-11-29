from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('directory/', views.directory, name='directory'),
    path('folder/edit/<int:id>/', views.edit_folder, name='folder-edit'),
    path('folder/delete/<int:id>/', views.delete_folder, name='folder-delete'),
    path('folder/open/<int:id>/', views.open_folder, name='folder-open'),
    path('folder/open/shared-to-you/', views.open_shared_to_you, name='folder-shared-to-you'),
    path('file/edit/<int:id>/', views.edit_file, name='file-edit'),
    path('file/delete/<int:id>/', views.delete_file, name='file-delete'),
    path('file/download/<int:id>', views.download_file, name='file-download'),
    path('file/share/<int:id>', views.share_file, name='file-share'),
    path('uploads/', views.uploads, name='uploads'),
    path('myactions/', views.myactions, name='myactions'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings, name='settings'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/conversation', views.conversation, name='conversation'),
]
