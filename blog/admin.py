from django.contrib import admin
from .models import *

from django.utils.html import format_html
# Register your models here.
@admin.register(blog_detail)

class blog_detail(admin.ModelAdmin):
    list_display=['id','blog_instructor','blog_title','slug']
    list_display_links=('blog_instructor','id')


# @admin.register(blogdetail_img)
# class blogdetail_img(admin.ModelAdmin):
#     list_display_links=('imgs','id')
#     list_display=['id','imgs']

@admin.register(blogdetail_element)
    
class blogdetail_element(admin.ModelAdmin):
    list_display_links=('element',)
    list_display=['id','element']
    
    
@admin.register(blog_review)
    
class blog_review(admin.ModelAdmin):
    list_display_links=('user','id')
    list_display=['id','user','blog_id','comment']

    
    
