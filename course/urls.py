from django.contrib import admin
from django.urls import path,include
from course import views

urlpatterns = [

  
        path('courses/', views.courses, name='courses'),

        path('commingsoon/', views.commingsoon, name='commingsoon'),
            
        path('course/<slug:course>', views.course_single, name='course-single'),
      #   path('course/<int:id>', views.course_single, name='course-single'),



  ]