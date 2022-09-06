from django.contrib import admin
from django.urls import path,include
from blog import views

urlpatterns = [

  path('blog/', views.blog, name='blog'),

  path('blog-detail/<slug:blogs>', views.single_blog, name='single-blog'),
  
  ]