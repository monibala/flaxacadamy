from django.contrib import admin
from django.urls import path,include
from user_profile import views

urlpatterns = [
  
  path('profile/<slug:profile>', views.profile, name='profile'),
  
  path('profile-certificates/<slug:certificate>', views.profile_certificates, name='profile-certificates'),

  path('private-message/<slug:msg>', views.private_message, name='private-message'),

  path('setting-genralinfo/<slug:genralinfo>', views.setting_genralinfo, name='setting-genralinfo'),

  path('settings-avatar/<slug:avatar>', views.settings_avatar, name='settings-avatar'),

  path('settings-privacy/<slug:privacy>', views.settings_privacy, name='settings-privacy'),

  path('success-story/', views.success_story, name='success-story'),

  path('instructors/', views.instructors, name='instructors'),
  
  path('orders/<slug:order>', views.orders, name='orders'),
  
  path('change-password/<slug:pwd>', views.change_pwd, name='change-password'),

  path('quzess/<slug:quize>', views.quzess, name='quzess'),
      
  ]