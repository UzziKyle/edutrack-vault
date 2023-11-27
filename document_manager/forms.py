from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Folder, File
from django.contrib.auth import get_user_model


User = get_user_model()


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
        
    def __init__(self, current_user, *args, **kwargs):
        super(ShareFileForm, self).__init__(*args, **kwargs)
        self.fields['sharing_to'].queryset = User.objects.exclude(id=current_user.id)
        
    sharing_to = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple,
        label='Share with:',
        required=False
    )
        