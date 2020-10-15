from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from apps.home.models import User
import json 
from django.conf import settings 
from django.core.mail import send_mail
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum

import hashlib,string,random,base64

# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';

def paytm(request):   
    return render(request,'paytm/pay.html')

def payment(request):
    amount = request.POST.get('amount')
    order=request.POST.get('order')
    id = order
    param_dict={
                'MID':'WorldP64425807474247',
                'ORDER_ID':str(id),
                'TXN_AMOUNT':str(amount),
                'CUST_ID':'acfff@paytm.com',
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE':'WEBSTAGING',
                'CHANNEL_ID':'WEB',
	            'CALLBACK_URL':'http://127.0.0.1:8000/paytm/handlerequest/',
        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
    context = {
            'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
            'comany_name': settings.PAYTM_COMPANY_NAME,
            'param_dict': param_dict
        }
    return render(request,'paytm/paytm.html',context)

    # else:
    #     return redirect('offers')

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        
        if response_dict['RESPCODE'] == '01':
            
            print(response_dict["TXNAMOUNT"])
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paytm/paytmstatus.html', {'response': response_dict})

def offers(request):
    return render(request,'paytm/offers.html')



