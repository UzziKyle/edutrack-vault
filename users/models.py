from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    user_type_choices = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
        ('alumni', 'Alumni')
    ]
    user_type = models.CharField(max_length=20, choices=user_type_choices, default='student')

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=_('groups'))
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True, verbose_name=_('user permissions'))


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.username}\n{self.user.user_type}"
