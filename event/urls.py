from django.contrib import admin
from django.urls import path,include
from event import views

urlpatterns = [

  path('events/', views.events, name='events'),

  path('event-detail/<slug:event>/', views.single_event, name='single-event'),


  ]