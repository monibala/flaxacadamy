from django.contrib import admin

# Register your models here.
from .models import*

@admin.register(Newsletter_subscriber)
class Newsletter_subscriber(admin.ModelAdmin):
    list_display=['id','suscriber_email']
    list_display_links=('suscriber_email','id')


@admin.register(New_Course)
class AdminNew_Course(admin.ModelAdmin):
    list_display= ['id','c_price','c_image','c_name','c_description']
  