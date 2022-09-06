
from django.shortcuts import render,HttpResponse,redirect

from shop.models import *
from .models import *
from datetime import date
from django.core.paginator import Paginator

from django.contrib import messages
# Create your views here.

def single_event(request,event):

    event=event_detail.objects.filter(slug=event)
    today=date.today()

    res={'event':event,'today':today}
    return  render(request,'single-event.html',res)

def events(request):
    event=event_detail.objects.all().order_by('id')

    paginator=Paginator(event,6)
    page_no=request.GET.get('page')
    page_obj=paginator.get_page(page_no)

    res={'event':page_obj}
    return render(request,'events.html',res)







