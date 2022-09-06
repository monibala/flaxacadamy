from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(instructor)

class instructor(admin.ModelAdmin):
    list_display=['id','name','slug','expert']
    list_display_links=('name','slug')


@admin.register(student)

class student(admin.ModelAdmin):
    list_display=['id','name','slug']
    list_display_links=('name','slug')


@admin.register(chats)

class cht(admin.ModelAdmin):
    list_display=['msgby','msgto','msg','date']
    

