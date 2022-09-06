from django.contrib import admin

# Register your models here.
from .models import *
@admin.register(userType)


class userType(admin.ModelAdmin):
    list_display=['id','user','type']
    list_display_links=('user','id')

    
@admin.register(frgt_pwd)

class frgt_pwd(admin.ModelAdmin):
    list_display=['id','user']
    list_display_links=('user','id')

    