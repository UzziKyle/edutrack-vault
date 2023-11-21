from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'authentication/login.html')

def signup(request):
    return render(request, 'authentication/signup.html')

def home(request):
    return render(request, 'document_manager/index.html')