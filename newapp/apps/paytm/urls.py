from django.urls import path
from . import views

urlpatterns = [
    path('',views.paytm,name='paytm'),
    path('payment',views.payment,name='payment'),
    path('handlerequest/',views.handlerequest,name='paytmkaro'),
    path('offers/',views.offers,name='offers')
]