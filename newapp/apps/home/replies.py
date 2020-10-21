from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Post, Following, Followers, Notification, Comments, Replies
import json
from django.conf import settings
from django.core.mail import send_mail

def replies(request):
    # currently checks if current user is a valid user or not
    #Basic Reply Implementation
    if 'username' in request.session:
        msg=request.GET.get('msg')
        commentid=request.GET.get('commentid')
        commentuser=Comments.objects.get(pk=commentid).user.username
        user=request.session['username']
        replyid = Replies.add_reply(commentid,msg,request.session['username'])    #add reply takes comment id msg,user that is replied and adds in database
        rep={'msg':"success",'commentuser':commentuser,'user':user , 'replyid':replyid}
        print(replyid)
        response=json.dumps(rep)
        return HttpResponse(response,content_type="application/json")
    return HttpResponse("Login Pehle karo fir hoga reply")


def delete_reply(request,*args):
    if "username" in request.session:
        replyid = request.GET.get('replyid')
        Replies.delete_reply(replyid)
        print(replyid)

        rep={}
        response=json.dumps(rep)
        return HttpResponse(response,content_type="application/json")

    return HttpResponse('login')

