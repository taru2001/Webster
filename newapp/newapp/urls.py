
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',include('apps.home.urls')),
    path('',views.index,name="site_index")
]
