from django.forms import ModelForm
from .models import Folder, File

class CreateFolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
        
        
class UploadFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']
        
        
class EditFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name']
        
        
class ShareFileForm(ModelForm):
    class Meta: 
        model = File
        fields = ['sharing_to']
        