from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [

  path('', views.home, name='home'),
  
  path('search/', views.search, name='search'),
  path('page-not-found/', views.error, name='error'),
  path('faqs/', views.faqs, name='faqs'),

  path('gallery/', views.gallery, name='gallery'),

  path('term-condition/', views.term_condition, name='term-condition'),
  path('privacy-policy/', views.privacy, name='privacy-policy'),

  ]