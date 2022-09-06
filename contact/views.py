
from email import message
import pytz
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import*
import datetime
import pytz

from django.contrib import messages

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
import os
def contact(request):
    res={}
    if request.method=='POST':
        if request.user.is_authenticated:
            name=request.POST['name']
            email=request.POST['email']
            subject=request.POST['subject']
            msg=request.POST['msg']
            user=User.objects.get(id=request.user.id)
            cont=contact_msg(user=user,name=name,email=email,subject=subject,Msg=msg)
            cont.save()  
            msg1=(f'\n\n\n Name :  {name} \n Email :  {email} \n Message :  {msg}')
            send_mail(subject,msg1,email,[settings.EMAIL_HOST_USER],fail_silently=False)
            messages.success(request,'Your Message Send Successfully.')
            return redirect(request.get_full_path())
        else:
            messages.warning(request,'Please! Login Or Register.')
            return redirect('loginregister')
    if len(User.objects.filter(username='admin'))>0:
        usr=User.objects.get(username='admin')
        cont=contact_page_info.objects.filter(user=usr)
        res={'cont':cont}
    return  render(request,'contact.html',res)
