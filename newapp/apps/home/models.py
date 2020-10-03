from django.db import models

# Create your models here.

class User(models.Model):
    name_id=models.AutoField
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    mobile=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=25)
    description = models.CharField(max_length=25,default="")
    stats = models.CharField(max_length=25,default="")
    country = models.CharField(max_length=25,default="")
    state = models.CharField(max_length=25,default="")
    games = models.CharField(max_length=100,default="")
    profileImage = models.ImageField(upload_to = "home/userProfiles",blank=True)
    

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


class Following(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    followed = models.ManyToManyField(User,related_name="followed")

    @classmethod
    def follow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(user=currUser)
        obj.followed.add(to_follow)
        

    @classmethod
    def unfollow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(user=currUser)
        obj.followed.remove(to_follow)

    def __str__(self):
        return self.user.username


class Followers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follower = models.ManyToManyField(User,related_name="follower")

    @classmethod
    def follow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(user=to_follow)
        obj.follower.add(currUser)
        

    @classmethod
    def unfollow(cls,currUser,to_follow):
        obj, create = cls.objects.get_or_create(user=to_follow)
        obj.follower.remove(currUser)

    def __str__(self):
        return self.user.username



