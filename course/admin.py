from statistics import median
from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

@admin.register(course_detail)
class course_detail(admin.ModelAdmin):

    list_display_links=('course_title','id')
    list_display=['id','course_title','course_instructor','course_price','category']

   

@admin.register(crs_review)
class crs_review(admin.ModelAdmin):
    list_display_links=('name','id')
    list_display=['id','name','comment'[:20]]

    
@admin.register( who_this_crs_for)
class  who_this_crs_for(admin.ModelAdmin):
    list_display_links=('crs','title','id')
    list_display=['id','crs'[:20],'title'[:20]]
