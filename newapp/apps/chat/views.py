from django.shortcuts import render
from  apps.home.models import User

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    myname=request.session["username"]
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'myname' : myname
    })