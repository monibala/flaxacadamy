from django.shortcuts import render,HttpResponse,redirect

# from blog.models import *
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib import messages
from django.db.models import Count
# Create your views here.


def commingsoon(request):
    return  render(request,'commingsoon.html')

def course_single(request,course):
    res={}
    crs=course_detail.objects.filter(slug=course)
    more_crs=course_detail.objects.all()
    if request.method=='POST':
        if request.user.is_authenticated:
            comment=request.POST['comment']
            rate=request.POST['rate']
            name=User.objects.get(id=request.user.id)
            crs=course_detail.objects.get(slug=course)
            rvw=crs_review(name=name,comment=comment,rate=rate,crs=crs)
            rvw.save()
            messages.success(request,'Review Posted Successfully.')
            return redirect(request.get_full_path())
        else:
            
            messages.warning(request,'Please! login or register.')
            return redirect ('loginregister')
    # rt_count=[]
    
    crs1=course_detail.objects.get(slug=course)
    rt=crs_review.objects.filter(crs=crs1).aggregate(Count('rate'))
    
    # rt['id']=crs1.id
    # rt_count.append(rt)
    cnt=crs_review.objects.filter(crs=crs1)
    cunt=0
    tot=0
    try:
        for i in cnt:
            cunt+=i.rate
        tot=cunt/len(cnt) 
    except ZeroDivisionError:
        pass 
    
    ct_1=crs_review.objects.filter(crs=crs1,rate=1).count()*1
    ct_2=crs_review.objects.filter(crs=crs1,rate=2).count()*2
    ct_3=crs_review.objects.filter(crs=crs1,rate=3).count()*3
    ct_4=crs_review.objects.filter(crs=crs1,rate=4).count()*4
    ct_5=crs_review.objects.filter(crs=crs1,rate=5).count()*5
    print(type(format(tot,'.0f')))
    res={'crs':crs,'more_crs':more_crs,'crss':crs_review.objects.filter(crs=crs1).order_by('-id'),
    # 'count':len(count),'crss':count,
    'total':format(tot,'.1f'),
    'tot':int(format(tot,'.0f')),
    'counts':len(cnt),
    'ct_1':ct_1/100,'ct_2':ct_2/100,'ct_3':ct_3/100,'ct_4':ct_4/100,'ct_5':ct_5/100}
    
    return  render(request,'course-single.html',res)

        
def courses(request):
    if request.method=='POST':
        search=request.POST['search']
        or_look=(Q(course_title__icontains=search)|Q(category__icontains=search)|Q(course_price__contains=search)|
        Q(slug__icontains=search)|Q(course_instructor__name__icontains=search))
        # Q(course_description__icontains=search)|Q(lession_no__icontains=search) 
        # |Q(student_no__icontains=search)|Q(course_certificate__icontains=search)|
        # Q(course_quiz__icontains=search) |Q(course_duration_in_weeks__icontains=search))
        crss=course_detail.objects.filter(or_look).order_by('id')
    
    elif request.GET.get('inst')!=None:
        ins=instructor.objects.get(slug=request.GET.get('inst'))
        crss=course_detail.objects.filter(course_instructor=ins).order_by('id')
    else:
        crss=course_detail.objects.all().order_by('id')
    if len(crss)==0:    
      return render(request,'searchnotfound.html')

        
    paginator=Paginator(crss,6)
    page_no=request.GET.get('page')
    crs=paginator.get_page(page_no)
       
    res={'crs':crs,'count':len(crss),'cnt':len(crs)}
    return  render(request,'courses.html',res)
