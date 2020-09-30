from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,'home/index.html')

def registerUser(request):
    return HttpResponse("Register page")

def about(request):
    return HttpResponse("About page")

def loginUser(request):
    return render(request,'home/login.html')
