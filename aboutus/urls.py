from django.contrib import admin
from django.urls import path,include
from aboutus import views

urlpatterns = [

  
  path('aboutus/', views.aboutus, name='aboutus'),


  ]