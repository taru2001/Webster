from django.contrib import admin

# Register your models here.

from .models import User,Post,Following,Followers,Notification

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Followers)
admin.site.register(Notification)
