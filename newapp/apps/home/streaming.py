from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Post, Following, Followers, Notification, Comments, Replies,stream
import json 
from django.conf import settings 
from django.core.mail import send_mail
import os




def check(request,*args):
    uri = request.GET.get('pic')

    all_streams = stream.objects.all()

    total = 0

    if len(all_streams)<=30:
        pass
    else:
        total = len(all_streams)-30
        for i in all_streams:
            if total==0:
                break
            else:
                total-=1
                i.delete()


    
    newurl = stream(ss=uri)
    stream.save(newurl)
    
    resp={}
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


def renders(request):  
    return render(request,'home/render.html')


def getstream(request):
    latesturl = stream.objects.all()
    
    resp={'url':latesturl[0].ss}
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")
