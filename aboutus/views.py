from django.shortcuts import render,HttpResponse,redirect
from course.models import*
from user_profile.models import*
# Create your views here.

def aboutus(request):
    
    course=course_detail.objects.all()
    crs={c.course_title for c in course}
    inst=instructor.objects.all()
    res={'crs':crs,'inst':inst}
    return  render(request,'aboutus1.html',res)

