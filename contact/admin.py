from django.contrib import admin

from .models import*
# Register your models here.
@admin.register(contact_msg)

class contact_msg(admin.ModelAdmin):
    list_display=['id','user','name']
    list_display_links=('user','id')


@admin.register(operation_hours)

class operation_hours(admin.ModelAdmin):
    list_display=['id','day_start','day_end','time_start','time_end']
    list_display_links=('day_start','id')


@admin.register(contact_page_info)

class contact_page_info(admin.ModelAdmin):
    list_display=['id','user','gmail','mobile']
    list_display_links=('user','id')


