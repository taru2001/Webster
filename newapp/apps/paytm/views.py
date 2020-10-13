from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from .models import User, Post, Following, Followers, Notification, Comments
import json 
from django.conf import settings 
from django.core.mail import send_mail
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum

# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def paytm(request):
    return render(request,'paytm/pay.html')

def payment(request):
    amount = request.POST.get('amount')
    param_dict={
            'MID':'WorldP64425807474247',
            'ORDER_ID':'1',
            'TXN_AMOUNT':'1',
            'CUST_ID':'coderboytg@gmail.com',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/paytm/handlerequest/',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request,'paytm/paytm.html',{'param_dict': param_dict})

@csrf_exempt
def handlerequest(request):
    return HttpResponse("done")