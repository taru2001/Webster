
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',include('apps.home.urls')),
    path('',views.index,name="site_index"),
    path('chat/',include('apps.chat.urls')),
    path('paytm/',include('apps.paytm.urls'))
] + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
