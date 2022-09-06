
from email import message
from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator
from .models import*

from django.contrib import messages
from django.db.models import Q
# Create your views here.


def blog(request):
    if request.method=='POST':
        search=request.POST['search']
        look=(Q(blog_category__icontains=search)|Q(blog_title__icontains=search)
        |Q(slug__icontains=search)|Q(tags__icontains=search))
        blogs=blog_detail.objects.filter(look).order_by('id')  
    else:
      cat=request.GET.get('category')
      tg=request.GET.get('tags')
      if cat != None:
          blogs=blog_detail.objects.filter(blog_category=cat).order_by('id')
      elif tg != None:
          blogs=blog_detail.objects.filter(tags=tg).order_by('id')
      else:
        blogs=blog_detail.objects.all().order_by('id')
    if len(blogs)==0:    
      return render(request,'searchnotfound.html')

    li=[]
    cats=blog_detail.objects.values('blog_category')
    x={cat['blog_category'] for cat in cats}
    for i in x:
      cat=blog_detail.objects.filter(blog_category=i).count()
      li.append([i,cat])

    tag=blog_detail.objects.values('tags')
    tags={t['tags'] for t in tag}
    
    paginator=Paginator(blogs,6)
    page_no=request.GET.get('page')
    page_obj=paginator.get_page(page_no)
    res={'blog':page_obj,'cat':li,'tag':tags}
    return  render(request,'blog.html',res)

def single_blog(request,blogs):
  
    blgs=blog_detail.objects.filter(slug=blogs)

    blog_rcnt=blog_detail.objects.all() 
    li=[]
    cats=blog_detail.objects.values('blog_category')
    x={cat['blog_category'] for cat in cats}
    for i in x:
      cat=blog_detail.objects.filter(blog_category=i).count()
      li.append([i,cat])

    
    tag=blog_detail.objects.values('tags')
    tags={t['tags'] for t in tag}
    # stud=student.objects.all()
    rvw=blog_review.objects.filter(blog_id=blog_detail.objects.get(slug=blogs)).order_by('-id')
    if request.method=='POST':
        if request.user.is_authenticated :
          if request.user.userType.type =='2' :

            comment=request.POST['comment']
            user=student.objects.get(user=User.objects.get(id=request.user.id))
            bg=blog_detail.objects.get(slug=blogs)
            rvw=blog_review(user=user,blog_id=bg,comment=comment)
            rvw.save()
            messages.success(request,'Review Posted Successfully.')
            return redirect(request.get_full_path())
          else:
             messages.error(request,'You are not student.')
             return redirect(request.get_full_path())
        else:
          
          messages.warning(request,'Please login or register !')
          return redirect('loginregister')
    com=blog_review.objects.filter(blog_id=blog_detail.objects.get(slug=blogs)).count()
    res={'blog':blgs,'rcnt':blog_rcnt,'cat':li,'tag':tags,'comment_count':com,'rvw':rvw}
    return  render(request,'single-blog.html',res)


    