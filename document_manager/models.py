from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def user_directory_path(instance, filename): 
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    
    return f'uploads/{instance.owner.id}/{instance.folder.name}/{filename}'


# Create your models here.
class Folder(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "folder"
        verbose_name_plural = "folders"

    def __str__(self) -> str:
        return self.name
        

class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=160, blank=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE)
    sharing_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='receiver', blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path, blank=False)
    
    def __str__(self) -> str:
        return self.name
    