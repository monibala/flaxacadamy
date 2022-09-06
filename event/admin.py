from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(event_detail)



class event_detail(admin.ModelAdmin):
    list_display_links=('event_title','id')
    list_display=['id','event_title','slug','state','country']