from django.db import models

# Create your models here.

class User(models.Model):
    name_id=models.AutoField
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    mobile=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=25)

    def __str__(self):
       return self.name 


class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    tagline = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to = "home/images",blank=True)
    posttype = models.CharField(max_length=10,default="video")

    def __str__(self):
        return self.user.username
