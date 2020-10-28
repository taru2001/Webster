from django.db import models
from apps.home.models import User

# Create your models here.
class Room(models.Model):
    admin = models.ForeignKey(User,on_delete=models.CASCADE)
    roomName = models.CharField(max_length=20,default="")
    password = models.CharField(max_length=20,default="")
    limit = models.IntegerField(default=0)
    members = models.ManyToManyField(User,related_name="members_of_room")
    time = models.DateTimeField(auto_now_add=True)
    which = models.CharField(default="private",max_length=20)
    blocked = models.ManyToManyField(User,related_name="blocked_users")

    class Meta:
        ordering=['-time']


    def __str__(self):
        return self.roomName




class Chats(models.Model):
    by_whom = models.ForeignKey(User,related_name="by_whom",on_delete=models.CASCADE)
    room = models.ForeignKey(Room , on_delete=models.CASCADE,related_name="which_room")
    message = models.CharField(max_length=100,default="")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.by_whom.username +" : "+ self.room.roomName

