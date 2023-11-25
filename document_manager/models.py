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
    name = models.CharField(max_length=100, blank=False, unique=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name = "folder"
        verbose_name_plural = "folders"

    def __str__(self) -> str:
        return self.name
        

class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=160, blank=False, unique=True)
    date_uploaded = models.DateTimeField(default=timezone.now, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path, blank=False)
    