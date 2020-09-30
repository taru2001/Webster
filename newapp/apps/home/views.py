from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,'home/index.html')

def registerUser(request):
    return render(request,'home/register.html')

def about(request):
    return HttpResponse("About page")

def loginUser(request):
    return HttpResponse("Login page")
