from django.shortcuts import render,redirect
from django.http import HttpResponse
from apps.home.models import User
from .models import Room,Chats
import json

# Create your views here.

def chatindex(request):
    if "username" in request.session:
        return render(request,'chat/chat-index.html')    

    return redirect('login')


def create_room(request):
    if "username" in request.session:

        if request.method=='POST':
            admin_name = request.session["username"]
            user_obj = User.objects.get(username=admin_name)
            password = request.POST.get('password')
            room_name = request.POST.get('roomName')
            limit  = request.POST.get('limit')
            which = request.POST.get('which')

            currUser = User.objects.get(username=request.session["username"])

            newroom = Room(admin=user_obj,roomName=room_name,limit=limit,password=password,which=which)
            Room.save(newroom)
            newroom.members.add(currUser)
            newroom.save()
            return redirect('chatindex')

        return render(request,'chat/create-room.html',{'username':request.session["username"]})

    return redirect('login')



def join_room(request):
    if "username" in request.session:
        all_public_rooms = Room.objects.filter(which="public")
        print(all_public_rooms)
        return render(request,'chat/join-room.html',{'rooms':all_public_rooms})

    return render(request,'chat/join-room.html')



def handle_join_room(request):
    if "username" in request.session and request.method=='POST':
        room_name = request.POST.get('roomName')
        password = request.POST.get('password')

        currUser_obj = User.objects.get(username=request.session["username"])    

        all_rooms = Room.objects.all()

        found = 0
        currRoom = None

        for room in all_rooms:
            if room.roomName==room_name:
                currRoom = room
                found = 1
                break

        if found:
            if currRoom.password==password:
                
                is_member = currRoom.members.filter(username=currUser_obj.username)

                # Main chat html rendering............!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if not is_member:
                    
                    if currRoom.members.count()==currRoom.limit:
                        return HttpResponse("<h1>Sorry the room is full</h1>")

                    else:
                        currRoom.members.add(currUser_obj)
                        currRoom.save()

                      
                room_chats = Chats.objects.filter(room=currRoom)

                return render(request,'chat/chat-room.html',{'currRoom':currRoom , 'room_chats':room_chats ,
                                                                 'currUser':currUser_obj.username})


            else:
                return HttpResponse("<h1>Wrong Password</h1>")


        else:
            return HttpResponse("<h1>No such room exists</h1>")

        return redirect('chatindex')

    elif "username" in request.session:
        return redirect('chatindex')

    else:
        return redirect('login')




def get_chats(request,room_id):
    if "username" in request.session:
        room_obj = Room.objects.filter(id=room_id)

        if not room_obj:
            resp = {
            'check':"no room",
            'chats':"",
            'users':""
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

        room_obj=room_obj[0]

        currUser_obj = User.objects.get(username = request.session["username"])

        member = room_obj.members.filter(username=currUser_obj.username)
        if member:
            room_chats = Chats.objects.filter(room=room_obj)
            chats=[]
            users = []

            for msg in room_chats:
                chats.append(msg.message)
                users.append(msg.by_whom.username)

            resp = {
                'check':"ok",
            'chats':chats,
            'users':users
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")


        else:
            redirect('chatindex')

    return redirect('login')




def handlemsg(request,*args):
    if "username" in request.session:
        roomid = request.GET.get('roomid')
        room_obj = Room.objects.get(id=roomid)

        if not room_obj:
            resp = {
            'check':"room not there or u r not member of it",
            'msg':""
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")
        
        currUser_obj = User.objects.get(username = request.session["username"])

        member = room_obj.members.filter(username=currUser_obj.username) 

        if member:
            msg = request.GET.get('msg')
            newmsg = Chats(room=room_obj,by_whom=currUser_obj,message=msg)
            Chats.save(newmsg)

            resp = {
            'check':"ok",
            'msg':msg
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")


        else:
            resp = {
            'check':"room does not exist or u r not member of it",
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")

    return redirect('login')



def handleleave(request,*args):
    if "username" in request.session:
        print("yes")
        username = request.session["username"]
        roomid = request.GET.get('roomid')
        room_obj = Room.objects.filter(id=roomid)

        if not room_obj:
            return redirect('chatindex')

        room_obj=room_obj[0]

        is_member = room_obj.members.filter(username=username)

        if is_member:
            is_admin = True if room_obj.admin.username == username else False

            if is_admin:
                room_obj.delete()
                all_chats=Chats.objects.filter(room=room_obj)
                all_chats.delete()

            else:
                room_obj.members.remove(is_member[0])
                all_chats = Chats.objects.filter(by_whom=is_member[0],room=room_obj)
                all_chats.delete()
                room_obj.save()

        
        return redirect('chatindex')


    return redirect('login')