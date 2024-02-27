from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
def home(request):
    return render(request , 'home.html')

def contact(request):
    return render(request , "contact.html")

def events(request):
    return render(request,"events.html")

def registration(request):
    return render(request,"registration.html")