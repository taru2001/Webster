from django.urls import path
from . import views

urlpatterns = [
    path('',views.chatindex,name="chatindex"),
    path('create-room/',views.create_room,name="createRoom"),
    path('join-room/',views.join_room,name="joinRoom"),
    path('handle_join_room/',views.handle_join_room,name="handleJoin"),
    path('getChats/<int:room_id>/',views.get_chats,name="getchats"),
    path('handlemsg/',views.handlemsg,name="handlemsg"),
    path('handleleave/',views.handleleave,name="handleleave"),
    path('handlekick/',views.handlekick,name="handlekick"),
    path('handleban/',views.handleban,name="handleban")
   
]