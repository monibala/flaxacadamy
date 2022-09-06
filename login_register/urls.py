from django.contrib import admin
from django.urls import path,include
from login_register import views

urlpatterns = [


  path('login-register/', views.loginregister, name='loginregister'),
  path('register/',views.register,name='register'),
  path('login/', views.loged_in, name='login'),
  path('logout/', views.loged_out, name='logout'),
  path('lost-password/', views.lost_password, name='lost-password'),
  
  path('password-confirm/<str:id>/',views.pwd_reset_cnfrm,name='pwd_cnfrm'),
    

  ]