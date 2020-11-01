from django.contrib import admin

# Register your models here.

from .models import User,Post,Following,Followers,Notification,Comments,Replies,stream,tempUser

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Followers)
admin.site.register(Notification)
admin.site.register(Comments)
admin.site.register(Replies)
admin.site.register(stream)
admin.site.register(tempUser)
