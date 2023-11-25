from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from .forms import FolderForm, UploadFileForm, EditFileForm


# Create your views here.
@login_required
def home(request):
    context = {}
    ordering = request.GET.get('ordering', "")
    folders = Folder.objects.filter(parent=None, owner=request.user)
        
    if ordering:
        folders = folders.order_by(ordering)
    
    context['folders'] = folders 
    context['form'] = FolderForm()
        
    if request.method == 'POST':
        form = FolderForm(request.POST)
        
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            messages.success(request, f'{folder.name} was created successfully.')
            redirect('home')
            
        else:
            context['form'] = form
            messages.error(request, 'Folder name is required')
            return render(request, 'document_manager/home.html', context)

    return render(request, 'document_manager/home.html', context)


@login_required   
def edit_folder(request, id):
    context = {}
    folder = get_object_or_404(Folder, id=id)
    
    if request.method == 'GET':
        context['form'] = FolderForm(instance=folder)
        context['id'] = folder
        
        return render(request, 'document_manager/home.html', context)
    
    elif request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'{folder.name} has been updated successfully!')
            return redirect('home')
        
        else:
            context['form'] = form
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'document_manager/home.html', context)
        

@login_required  
def delete_folder(request, id):
    context = {}
    folder = get_object_or_404(Folder, pk=id)
    context['folder'] = folder
    
    if request.method == 'GET':        
        return render(request, 'document_manager/delete_folder.html', context)
    
    elif request.method == 'POST':
        folder_name = folder.name
        folder.delete()
        messages.success(request, f'{folder_name} has been deleted successfully.')
        return redirect('home')
    

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
    context['folderform'] = FolderForm()
    
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
                redirect(f'folder/open/{folder.id}/')

            else:
                context['form'] = form
                messages.error(request, 'Please correct the following erros.')
                return render(request, 'document_manager/open_folder.html', context)
            
        if 'folderform' in request.POST:
            form = FolderForm(request.POST)
        
            if form.is_valid():
                subfolder = form.save(commit=False)
                subfolder.owner = request.user
                subfolder.parent = folder
                subfolder.save()
                messages.success(request, f'{subfolder.name} has been updated successfully!')
                redirect(f'folder/open/{subfolder.parent.id}/')
            
            else:
                context['form'] = form
                messages.error(request, 'Please correct the following errors:')
                return render(request, 'document_manager/open_folder.html', context)

    return render(request, 'document_manager/open_folder.html', context)


@login_required   
def edit_file(request, id):
    context = {}
    file = get_object_or_404(File, id=id)
    
    if request.method == 'GET':
        context['form'] = EditFileForm(instance=file)
        context['id'] = file
        
        return render(request, 'document_manager/home.html', context)
    
    elif request.method == 'POST':
        form = EditFileForm(request.POST, instance=file)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'{file.name} has been updated successfully!')
            return redirect('home')
        
        else:
            context['form'] = form
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'document_manager/home.html', context)
        
        
@login_required
def delete_file(request, id):
    context = {}
    file = get_object_or_404(File, pk=id)
    context['file'] = file    
    
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
