from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'document_manager/index.html')