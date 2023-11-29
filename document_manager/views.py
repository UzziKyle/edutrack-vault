from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from .forms import CreateFolderForm, UploadFileForm, EditFileForm, ShareFileForm


@login_required
def home(request):
    context = {}
    
    try:
        files = File.objects.filter(owner=request.user).order_by('-date')[:5][::-1]
        files = reversed(files)
        
    except:
        files = None
        
    user = request.user
    
    context['files'] = files
    context['user'] = user
    context['title'] = 'Home'
    
    return render(request, 'document_manager/home.html', context)
    

@login_required
def directory(request):
    context = {}
    ordering = request.GET.get('ordering', "")
    folders = Folder.objects.filter(parent=None, owner=request.user)
        
    if ordering:
        folders = folders.order_by(ordering)
    
    context['folders'] = folders 
    context['form'] = CreateFolderForm()
    context['title'] = 'My Directory'
        
    if request.method == 'POST':
        form = CreateFolderForm(request.POST)
        
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            messages.success(request, f'{folder.name} was created successfully.')
            redirect('directory')
            
        else:
            context['form'] = form
            messages.error(request, 'Folder name is required.')
            return render(request, 'document_manager/directory.html', context)

    return render(request, 'document_manager/directory.html', context)


@login_required   
def edit_folder(request, id):
    context = {}
    folder = get_object_or_404(Folder, id=id)
    
    if request.method == 'GET':
        context['form'] = CreateFolderForm(instance=folder)
        context['folder'] = folder
        context['title'] = f'Edit {folder.name}'
        
        return render(request, 'document_manager/edit_folder.html', context)
    
    elif request.method == 'POST':
        form = CreateFolderForm(request.POST, instance=folder)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'{folder.name} has been updated successfully!')
            
            if folder.parent:
                return redirect('folder-open', folder.parent.id)
                
            return redirect('directory')
        
        else:
            context['form'] = form
            messages.error(request, 'Please correct the following errors.')
            return render(request, 'document_manager/edit_folder.html', context)
        

@login_required  
def delete_folder(request, id):
    context = {}
    folder = get_object_or_404(Folder, pk=id)
    context['folder'] = folder
    context['title'] = f'Delete {folder.name}'
    
    if request.method == 'GET':        
        return render(request, 'document_manager/delete_folder.html', context)
    
    elif request.method == 'POST':
        folder_name = folder.name
        parent = folder.parent
        folder.delete()
        messages.success(request, f'{folder_name} has been deleted successfully.')
        
        if parent:
            return redirect('folder-open', parent.id)
        
        return redirect('directory')
    

@login_required   
def open_folder(request, id):
    context = {}
    ordering = request.GET.get('ordering', "")
    folder = get_object_or_404(Folder, id=id)
    subfolders = Folder.objects.filter(parent=folder, owner=request.user)
    files = File.objects.filter(folder=folder, owner=request.user)
    
    if ordering:
        subfolders = subfolders.order_by(ordering)
        files = files.order_by(ordering)
    
    context['folder'] = folder
    context['subfolders'] = subfolders
    context['files'] = files
    context['fileform'] = UploadFileForm()
    context['folderform'] = CreateFolderForm()
    context['title'] = folder.name
    
    if request.method == 'GET':        
        return render(request, 'document_manager/open_folder.html', context)
        
    if request.method == 'POST':
        if 'fileform' in request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            
            if form.is_valid():
                file = form.save(commit=False)
                file.owner = request.user
                file.folder = folder
                file.save()
                messages.success(request, f'{file.name} was uploaded successfully.')
                redirect (f'folder/open/{folder.id}/')

            else:
                context['form'] = form
                messages.error(request, 'Please correct the following errors.')
                return render(request, 'document_manager/open_folder.html', context)
            
        if 'folderform' in request.POST:
            form = CreateFolderForm(request.POST)
            print(form)
        
            if form.is_valid():
                subfolder = form.save(commit=False)
                subfolder.owner = request.user
                subfolder.parent = folder
                subfolder.save()
                messages.success(request, f'{subfolder.name} was created successfully.')
                redirect(f'folder/open/{subfolder.parent.id}/')
            
            else:
                context['form'] = form
                messages.error(request, 'Please correct the following errors.')
                return render(request, 'document_manager/open_folder.html', context)

    return render(request, 'document_manager/open_folder.html', context)


@login_required
def open_shared_to_you(request):
    context = {}
    files = request.user.receiver.all()
    ordering = request.GET.get('ordering', "")
    
    if ordering:
        files = files.order_by(ordering)
        
    context['files'] = files
    context['title'] = 'Shared to You'

    if request.method == 'GET':        
        return render(request, 'document_manager/open_shared_files.html', context)
    

@login_required   
def edit_file(request, id):
    context = {}
    file = get_object_or_404(File, id=id)
    
    if request.method == 'GET':
        context['form'] = EditFileForm(instance=file)
        context['file'] = file
        
        return render(request, 'document_manager/edit_file.html', context)
    
    elif request.method == 'POST':
        form = EditFileForm(request.POST, instance=file)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'{file.name} has been updated successfully!')
            return redirect('folder-open', file.folder.id)
        
        else:
            context['form'] = form
            messages.error(request, 'Please correct the following errors.')
            return render(request, 'document_manager/edit_file.html', context)
        
        
@login_required
def delete_file(request, id):
    context = {}
    file = get_object_or_404(File, pk=id)
    context['file'] = file    
    context['title'] = f'Delete {file.name}'
    
    if request.method == 'GET':        
        return render(request, 'document_manager/delete_file.html', context)
    
    elif request.method == 'POST':
        folder_id = file.folder.id
        file_name = file.name
        file.delete()
        messages.success(request, f'{file_name} has been deleted successfully.')
        return redirect('folder-open', folder_id)
    
    
@login_required
def download_file(request, id):
    file = File.objects.get(id=id)
    filename = file.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


@login_required   
def share_file(request, id):
    context = {}
    file = get_object_or_404(File, id=id)
    context['title'] = f'Share {file.name}'
    
    if request.method == 'GET':
        context['form'] = ShareFileForm(current_user=request.user, instance=file)
        context['file'] = file
        
        return render(request, 'document_manager/share_file.html', context)
    
    elif request.method == 'POST':
        form = ShareFileForm(current_user=request.user, data=request.POST, instance=file)
        print(file.folder.id)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'{file.name} has been shared successfully!')
            return redirect('folder-open', file.folder.id)
                    
        else:
            context['form'] = form
            messages.error(request, 'Please correct the following errors.')
            return render(request, 'document_manager/share_file.html', context)
        
        
@login_required
def uploads(request):
    context = {}
    files = File.objects.filter(owner=request.user)
    
    context['files'] = files
    context['title'] = 'My Uploads'
    
    return render(request, 'document_manager/uploads.html', context)


@login_required
def myactions(request):
    return render(request, 'document_manager/myactions.html', {'title': 'My Actions'})


@login_required
def notifications(request):
    return render(request, 'document_manager/notifications.html', {'title': 'Notifications'})


@login_required
def settings(request):
    return render(request, 'document_manager/settings.html', {'title': 'Settings'})


@login_required
def inbox(request): 
    return render(request, 'document_manager/inbox.html', {'title': 'Messages'})


@login_required
def conversation(request):
    return render(request, 'document_manager/conversation.html', {'title': 'Message'})
