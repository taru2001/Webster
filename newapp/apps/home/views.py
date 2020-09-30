from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,'home/index.html')

def registerUser(request):
    if request.method=='POST':
        fname = request.POST.post['name']
        femail = request.POST.post['email']
        phone = request.POST.post['mobileno']
        passw = request.POST.post['password']
        confpass = request.POST.post['confirmpassword']

        if passw!=confpass:
            return return HttpResponse("passwords did not matched...!!");

        


    return render(request,'home/register.html')

def about(request):
    return HttpResponse("About page")

def loginUser(request):
    return render(request,'home/login.html')
