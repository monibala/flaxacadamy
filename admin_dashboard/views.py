import collections
from email.mime import message
import imp
from os import abort
from wsgiref.util import request_uri
from django import http
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from admin_dashboard.form import * 
from login_register.models import *
from shop.models import *
from course.models import *
from django.contrib import messages as sms
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, JsonResponse
from admin_dashboard.templatetags.newfilter import *
# Create your views here.





def srch(request):
    
    res={}
    q= request.GET.get('q')
    blg=blog_detail.objects.filter(blog_title__contains=q)
    crs=course_detail.objects.filter(course_title__contains=q)
    event=event_detail.objects.filter(event_title__contains=q)
    prod=product_detail.objects.filter(product_title__contains=q)
    inst=instructor.objects.filter(name__contains=q)
    stud=student.objects.filter(name__contains=q)
    if crs:
        paginator=Paginator(crs,6)
        page_no=request.GET.get('page')
        res['crs']=paginator.get_page(page_no)
        res['tot']=len(crs)
        return render(request,'event.html',res)
    elif prod:
        paginator=Paginator(prod,6)
        page_no=request.GET.get('page')
        res['product']=paginator.get_page(page_no)
        res['tot']=len(prod)
        return render(request,'event.html',res)
    elif blg:
        paginator=Paginator(blg,6)
        page_no=request.GET.get('page')
        res['blogs']=paginator.get_page(page_no)
        res['tot']=len(blg)
        return render(request,'event.html',res)
    elif event:
        paginator=Paginator(event,6)
        page_no=request.GET.get('page')
        res['event']=paginator.get_page(page_no)
        res['tot']=len(event)
        return render(request,'event.html',res)
    elif inst:
        paginator=Paginator(inst,6)
        page_no=request.GET.get('page')
        res['inst']=paginator.get_page(page_no)
        res['tot']=len(inst)
        return render(request,'event.html',res)
    elif stud:
        paginator=Paginator(stud,6)
        page_no=request.GET.get('page')
        res['stud']=paginator.get_page(page_no)
        res['tot']=len(stud)
        return render(request,'event.html',res)

    return redirect('404')

def ad_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['totl_stud']=userType.objects.filter(type='2').count()
        res['totl_inst']=userType.objects.filter(type='1').count()
        res['totl_product']=product_detail.objects.all().count()
        res['totl_crs']=course_detail.objects.all().count()
        res['inst']=instructor.objects.all().order_by('-id')
        res['stud']=student.objects.all().order_by('-id')
        
        # crs=course_detail.objects.values('course_instructor__name').all()
        # print(crs,'ll')
        # ret=collections.defaultdict(int)
        li=[]
        for c in instructor.objects.all():
            inst_crs=course_detail.objects.filter(course_instructor=c).count()     
            li.append({'id':c.id,'crs_cunt':inst_crs})
        res['crs_count']=li
        return render(request,'admin-index.html',res)
    else:
        return redirect('ad_login')
def payments(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
    # crs_order=courses_purchase_order.objects.values('user','amount')
    # ret=collections.defaultdict(int)
    # for c in crs_order:
    #     ret[c['user']]+=int(c['amount'])
    #     crs=[{'usr':us,'amount':am} for us,am in ret.items()]
    # prod_order=products_purchase_order.objects.values('user','amount')
    # ret=collections.defaultdict(int)
    # for p in prod_order:
    #     ret[p['user']]+=int(p['amount'])
    #     prod=[{'usr':us,'amount':am} for us,am in ret.items()]
    # ret=collections.defaultdict(int)
    # for u in crs+prod:
    #     ret[u['usr']]+=int(u['amount'])
    #     rs=[{'usr':us,'amount':am} for us,am in ret.items()]
    # li=[]
    # for r in rs:
    #     inst=instructor.objects.filter(user__id=r['usr'])
    #     if inst:
    #         li.append([inst,r])
    #     stud=student.objects.filter(user__id=r['usr'])
    #     if stud:
    #         li.append([stud,r])
    # res['usrs']=li
        # crs=courses_purchase_order.objects.all()
        # prod=products_purchase_order.objects.all()
        # from itertools import chain
        # pymnt_all = list(chain(crs,prod))
        # tot=0
        # for i in pymnt_all:
        #     tot+=i.amount
        #     res['amnt']={'amount':tot}
        # res['crs']=crs.count()
        # res['prod']=prod.count()
        # res['inst']=instructor.objects.all()
        # res['stud']=student.objects.all()
        # paginator=Paginator(pymnt_all,10)
        # page_no=request.GET.get('page')
        # res['pymnts_all']=paginator.get_page(page_no)
        # res['tot']=len(pymnt_all)
        # res['typ']=userType.objects.all()
        trans=PaytmTransaction.objects.all()
        paginator=Paginator(trans,10)
        page_no=request.GET.get('page')
        res['trans']=paginator.get_page(page_no)
        return render(request,'payment-trans.html',res)
    else:
        return redirect('ad_login')
# def ad_register(request):

#         if request.method == "POST":
#                     name = request.POST['name']
#                     email = request.POST['email']
#                     password = request.POST['password']
#                     confirm=request.POST['confirm']
#                     usermail = User.objects.filter(email=email)
#                     if len(usermail) !=1 :
#                             if confirm==password: 
#                                 user =User.objects.create_superuser(username=name, email=email, password=password)
#                                 user.save()
#                                 frgpwd=frgt_pwd(user=user,frg_token=str(uuid.uuid4()))
#                                 frgpwd.save()
#                                 pro=admin_profile(user=user,email=email,name=name)
#                                 pro.save()
#                                 sms.success(request,'Registered Successfully.')
#                                 return redirect('ad_login')
#         return render(request,'create-account.html')
def ad_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('ad_dash')
    else:
        res={}
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            USER = authenticate(request,username=username, password=password)
            if USER is not None:
                login(request, USER)
                if request.user.is_superuser:
                    sms.success(request,'Login Success.')
                    return redirect('ad_dash')
                else:
                    
                    sms.error(request,'wrong username or password!')
                    return redirect('ad_login')
            
            else:
                sms.error(request,'Invalid Username or Password!')
                return redirect('ad_login')
                
        return render(request,'logn.html',res)
def ad_logout(request):
    if request.user.is_authenticated and request.user.is_superuser:
   
        try:
            logout(request)
            sms.success(request,'Logout Successfully.')
            return redirect('ad_login')
        except Exception as e:
            sms.warning(request,'something went wrong !')
            return redirect('ad_login')
    else:
        return redirect('ad_login')
    # return redirect('home')
def ad_forgot_pwd(request):
    if request.user.is_authenticated!=True:
        
        if request.method=='POST':
            try:
                email=request.POST['email']
                useremail=User.objects.get(email=email)
                frgtoken=frgt_pwd.objects.get(user=useremail)
                ftoken=frgtoken.frg_token
                emails=useremail.email   
                mail_msg=f'Your reset password link is http://127.0.0.1:8000/dashboard/password-change/{ftoken}.'
                # mail_msg=f'Set Password \n Your reset password link is https://cyberacdamy.herokuapp.com/dashboard/password-change/{ftoken}.'
                send_mail('For reset password', mail_msg,settings.EMAIL_HOST_USER, [emails],fail_silently=False)
                sms.success(request, "Mail Send Successfully.\n Please Check Your Email.")
                return redirect('ad_forgot_pwd')
            except Exception as e:
                sms.error(request,'Invalid Email!')
        return render(request,'admin-forgot-password.html')

    else:
        return redirect('error')  
def pwd_reset_change(request,id):
    if request.user.is_authenticated!=True:
        if request.method=='POST':
            try:
                pass1=request.POST['pass1']
                confirm=request.POST['pass2']
                if pass1==confirm:
                    frgpwd=frgt_pwd.objects.get(frg_token=id)
                    user=User.objects.get(username=frgpwd)
                    user.set_password(pass1)
                    user.save()
                    sms.success(request, "Password Change Successfully.\n +Please login. ")
                    return redirect('ad_login')
                else:
                    sms.error(request,'Password Not Match.Enter Same Password.')
            except Exception as e:
                print(e)
        return render(request,'pwd_change.html')
    else:
        return redirect('error')

def ad_event(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['events']=event_detail.objects.all()
        paginator=Paginator(res['events'],6)
        page_no=request.GET.get('page')
        res['event']=paginator.get_page(page_no)
        res['tot']=len(res['events'])
        nxt=request.get_full_path()
        if request.method=='POST':
            
            if request.POST.get('evid')!=None: # for delete
                evid=request.POST['evid']
                evnt=event_detail.objects.filter(id=evid)
                evnt.delete()
                sms.success(request,'Event Deleted SuccessFully.')
                return redirect(nxt)
            elif request.POST.get('eid')!=None: # for edit
                title=request.POST['title']
                desc=request.POST['desc'] 
                endtime=request.POST['endtime']
                starttime=request.POST['starttime']
                about=request.POST['about'] 
                img=request.POST['img']
                slot=request.POST['slot']
                cost=request.POST['cost']
                date=request.POST['date']
                state=request.POST['state']
                country=request.POST['country']
                enddate=request.POST['enddate']
                startdate=request.POST['startdate']
                ev= event_detail.objects.filter(id=request.POST['eid'])
                if len(ev)>0:
                    ob=ev[0]
                    if len(title)>0:
                        ob.event_title=title
                    if len(img)>0:
                        ob.event_img=img
                    if len(slot)>0:
                        ob.event_total_slot=slot
                    if len(cost)>0:
                        ob.event_cost=cost
                    if len(desc)>0:
                        ob.where_event=desc
                    if len(country)>0:
                        ob.country=country
                    if len(state)>0:
                        ob.state=state
                    if len(startdate)>0:
                        ob.event_start_date=startdate
                    if len(enddate)>0:
                        ob.event_end_date=enddate
                    if len(starttime)>0:
                        ob.event_start_time=starttime
                    if len(endtime)>0:
                        ob.event_end_time=endtime
                    if len(about)>0:
                        ob.about_event=about
                    if len(date)>0:
                        ob.date=date
                    ob.save()
                    sms.success(request,'Event Updated.')
                    return redirect(nxt)    
          
        return render(request,'event.html',res)
    else:
        return redirect('ad_login')
def ad_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['products']=product_detail.objects.all()
        paginator=Paginator(res['products'],6)
        page_no=request.GET.get('page')
        res['product']=paginator.get_page(page_no)
        res['tot']=len(res['products'])
        nxt=request.get_full_path()
        if request.method=='POST':
            if request.POST.get('prid')!=None: # for delete
                prid=request.POST['prid']
                prod=product_detail.objects.filter(id=prid)
                prod.delete()
                sms.success(request,'Product Deleted SuccessFully.')
                return redirect(nxt)
            elif request.POST.get('pid')!=None: # for edit
                title=request.POST['title']
                desc=request.POST['desc'] 
                price=request.POST['price']
                cat=request.POST['cat']
                about=request.POST['about'] 
                img=request.POST['img']
                tag=request.POST['tag']
                sku=request.POST['sku']
                dis=request.POST['dis']
                qunt=request.POST['qunt']
                pr= product_detail.objects.filter(id=request.POST['pid'])
                if len(pr)>0:
                    ob=pr[0]
                    if len(title)>0:
                        ob.product_title=title
                    if len(img)>0:
                        ob.product_img=img
                    if len(cat)>0:
                        ob.category=cat
                    if len(price)>0:
                        ob.product_price=price
                    if len(desc)>0:
                        ob.product_description=desc
                    if len(tag)>0:
                        ob.product_tag=tag
                    if len(qunt)>0:
                        ob.quntity=qunt
                    if len(sku)>0:
                        ob.product_sku=sku
                        
                    if len(about)>0:
                        ob.about_product=about
                    if len(dis)>0:
                        ob.discount=dis
                    ob.save()
                    sms.success(request,'Product Updated.')
                    return redirect(nxt)    
           
        return render(request,'event.html',res)
    else:
        return redirect('ad_login')
def ad_crs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['inst']=instructor.objects.all()
        res['who']=who_this_crs_for.objects.all()
        res['crss']=course_detail.objects.all()
        paginator=Paginator(res['crss'],6)
        page_no=request.GET.get('page')
        res['crs']=paginator.get_page(page_no)
        res['tot']=len(res['crss'])
        nxt=request.get_full_path()
        if request.method=='POST':
            if request.POST.get('crid')!=None: # for delete
            
                crid=request.POST['crid']
                crs=course_detail.objects.filter(id=crid)
                crs.delete()
                sms.success(request,'Course Deleted SuccessFully.')
                return redirect(nxt)
            elif request.POST.get('cid')!=None: # for edit
                title=request.POST['title']
                desc=request.POST['desc'] 
                price=request.POST['price']
                
                crti=request.POST['certificate']
                if request.POST.get('inst')!=None:
                    inst=instructor.objects.filter(id=request.POST.get('inst'))
                cat=request.POST['cat']
                img=request.POST['img']
                crs= course_detail.objects.filter(id=request.POST['cid'])
                if len(crs)>0:
                    ob=crs[0]
                    
                    if len(crti)>0:
                        ob.course_certificate=crti
                   
                    if len(title)>0:
                        ob.course_title=title
                    if len(img)>0:
                        ob.course_img=img
                    if request.POST.get('inst')!=None and len(inst)>0:
                        ob.course_instructor=instructor.objects.get(id=request.POST.get('inst'))
                    if len(cat)>0:
                        ob.blog_category=cat
                    if len(price)>0:
                        ob.course_price=price
                    if len(desc)>0:
                        ob.course_description=desc
                    ob.save()
                    sms.success(request,'Course Updated.')
                    return redirect(nxt)    
           
        return render(request,'event.html',res)
    else:
        return redirect('ad_login')
def ad_blogs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['inst']=instructor.objects.all()
        
        res['blog']=blog_detail.objects.all()
        paginator=Paginator(res['blog'],6)
        page_no=request.GET.get('page')
        res['blogs']=paginator.get_page(page_no)
        res['tot']=len(res['blog'])
        nxt=request.get_full_path()
        if request.method=='POST':
            if request.POST.get('blid')!=None:# for delete
                blid=request.POST['blid']
                blg=blog_detail.objects.filter(id=blid)
                blg.delete()
                sms.success(request,'Blog Deleted SuccessFully.')
                return redirect(nxt)
            
            elif request.POST.get('bid')!=None: # for edit
                title=request.POST['title']
                desc=request.POST['desc'] 
                tag=request.POST['tag']
                if request.POST.get('inst')!=None:
                    inst=instructor.objects.filter(id=request.POST.get('inst'))
                cat=request.POST['cat']
                head2=request.POST['about'] 
                img=request.POST['img']
                blg= blog_detail.objects.filter(id=request.POST['bid'])
                if len(blg)>0:
                    ob=blg[0]
                    
                    if len(title)>0:
                        ob.blog_title=title
                    if len(img)>0:
                        ob.blog_img=img
                    if request.POST.get('inst')!=None and len(inst)>0:
                        ob.blog_instructor=instructor.objects.get(id=request.POST.get('inst'))
                    if len(cat)>0:
                        ob.blog_category=cat
                    if len(head2)>0:
                        ob.head2=head2
                    if len(tag)>0:
                        ob.tags=tag
                    if len(desc)>0:
                        ob.blog_description=desc
                    ob.save()
                    sms.success(request,'Blog Updated.')
                    return redirect(nxt)    
           



        return render(request,'event.html',res)
    else:
        return redirect('ad_login')
def add_event(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        if request.method=='POST' :
            title=request.POST['title']
            desc=request.POST['desc'] 
            event_end_time=request.POST['endtime']
            state=request.POST['state']
            event_end_date=request.POST['enddate']
            event_start_time=request.POST['starttime'] 
            img=request.POST['img']
            country=request.POST['country']
            date=request.POST['date']  
            about=request.POST['about'] 
            event_cost=request.POST['cost']
            event_total_slot=request.POST['slot']
            event_start_date=request.POST['startdate']
        
            try:
                event= event_detail(event_img=img,event_title=title,state=state,country=country,date=date,event_cost=event_cost,
                event_total_slot=event_total_slot,event_start_date=event_start_date,event_end_date=event_end_date,
                event_start_time=event_start_time,event_end_time=event_end_time,about_event=about, where_event=desc)
                event.save()
                sms.success(request,'Event Added.')
                return redirect('ad_event')
            except Exception as p:
                sms.warning(request,'All Field Are Required !')
                return redirect('add_event')

    
        return render(request,'add-event.html',res)
    else:
        return redirect('ad_login')
def add_blog(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['inst']=instructor.objects.all()
        # res['imgs']=blogdetail_img.objects.all()
        res['elem']=blogdetail_element.objects.all()

        if request.method=='POST'  :
            title=request.POST['title']
            desc=request.POST['desc'] 
            tag=request.POST['tag']
            inst=instructor.objects.get(id=request.POST['inst'])
            cat=request.POST['cat']
            head1=request.POST['quote']
            head2=request.POST['about'] 
            img=request.FILES.get('img')
            elements=request.POST.getlist('element') 
            settings=request.POST['setting']
            need=request.POST['need']
            try:
                blg= blog_detail(blog_title=title,blog_instructor=inst,blog_category=cat,blog_img=img,
                blog_description=desc,tags=tag,head1=head1,head2=head2,setting=settings,why_need=need)
                blg.save()
                for i in elements:
                    blg.element.add(blogdetail_element.objects.get(id=i))
                
                
                sms.success(request,'Blog Added.')
                return redirect('ad_blog')
            except Exception as p:
                sms.warning(request,'All Field Are Required !')
                return redirect('add_blog')

        return render(request,'add-blog.html',res)
    else:
        return redirect('ad_login')
def add_crs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['inst']=instructor.objects.all()
        
        res['who']=who_this_crs_for.objects.all()
        if request.method=='POST'  :
            # doc = request.FILES
            title=request.POST['title']
            desc=request.POST['desc'] 
            price=request.POST['price']
            inst=instructor.objects.get(id=request.POST['inst'])
            cat=request.POST['cat']
            about=request.POST['about'] 
            img=request.FILES.get('img')
            crti=request.FILES.get('certificate')
            week=request.POST['week'] 
            who=request.POST.getlist('who')
            lession=request.POST['lession']
            try:    
                crs= course_detail(
                    course_instructor=inst,course_price=price,course_img=img,course_title=title,
                    short_course_description=about,course_description=desc,lession_no=int(lession),
                    course_duration_in_weeks=week,category=cat,course_certificate=crti)
                crs.save()
                for i in who:
                        crs.title.add(who_this_crs_for.objects.get(id=i))
                    
                sms.success(request,'Course Added.')
                return redirect('ad_course')
            except Exception as p:
                sms.warning(request,'All Field Are Required !')
                return redirect('add_crs')
        return render(request,'add-course.html',res)
    else:
        return redirect('ad_login')
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['inst']=instructor.objects.all()
        
        if request.method=='POST'  :
                
                title=request.POST['title']
                desc=request.POST['desc'] 
                price=request.POST['price']
                cat=request.POST['cat']
                about=request.POST['about'] 
                img=request.FILES.get('img')
                tag=request.POST['tag'] 
                sku=request.POST['sku']
                dis=request.POST['discount']
                quntity=request.POST['qunt']
                try:
                    prod= product_detail(
                        product_img=img,product_title=title,product_price=price,about_product=about,product_description=desc,
                        product_tag=tag,quntity=quntity,product_sku=sku,category=cat,discount=dis)
                    prod.save()
                    sms.success(request,'Product Added.')
                    return redirect('ad_product')
                except Exception as p:
                    sms.warning(request,'All Field Are Required !')
                    return redirect('add_product')
    
        return render(request,'add-product.html',res)
    else:
        return redirect('ad_login')

def stud(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        nxt=request.get_full_path()
        res['studs']=student.objects.all()
        paginator=Paginator(res['studs'],6)
        page_no=request.GET.get('page')
        res['stud']=paginator.get_page(page_no)
        res['tot']=len( student.objects.all() )
        if request.method=='POST':
                if request.POST.get('sdid')!=None: # for delete
                    sdid=request.POST['sdid']
                    prod=student.objects.filter(id=sdid)
                    # prod.delete()
                    ur=User.objects.filter(id=student.objects.get(id=sdid).user.id).delete()
                    sms.success(request,'Student Deleted SuccessFully.')
                    return redirect(nxt)
            
        return render(request,'instrut.html',res)
    else:
        return redirect('ad_login')

def inst(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        nxt=request.get_full_path()
        res['insts']=instructor.objects.all()
        paginator=Paginator(res['insts'],6)
        page_no=request.GET.get('page')
        res['inst']=paginator.get_page(page_no)
        res['tot']=len( instructor.objects.all() )
        if request.method=='POST':
                if request.POST.get('idid')!=None: # for delete
                    idid=request.POST['idid']
                    prod=instructor.objects.filter(id=idid)
                    # prod.delete()
                    ur=User.objects.filter(id=instructor.objects.get(id=idid).user.id).delete()
                    sms.success(request,'Instructor Deleted SuccessFully.')
                    return redirect(nxt)
            

        
        return render(request,'instrut.html',res)
    else:
        return redirect('ad_login')


def ad_profile(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['profile']=admin_profile.objects.filter(user=User.objects.get(id=request.user.id))
        if request.method=='POST':
            if request.POST.get('usr')!=None:
                email=request.POST['email']
                name=request.POST['name']
                img=request.POST['img']
                dob=request.POST['dob']
                address=request.POST['address']
                about=request.POST['about'] 
                phone=request.POST['phone']
                
                pro= admin_profile.objects.filter(user=User.objects.get(id=request.POST['usr']))
                if len(pro)>0:
                    ob=pro[0]
                    ob.user=User.objects.get(id=request.user.id)
                    if len(name)>0:
                        ob.name=name
                    if len(img)>0:
                        ob.img=img
                    if len(email)>0:
                        ob.email=email
                    if len(dob)>0:
                        ob.dob=dob
                    if len(phone)>0:
                        ob.mobile=phone
                    if len(about)>0:
                        ob.about=about
                    if len(address)>0:
                        ob.address=address
                    ob.save()
                    sms.success(request,'Profile Updated.')
                    return redirect('ad_profile')
                else:
                    try:
                        admin_profile(user=User.objects.get(id=request.user.id),name=name,img=img,email=email,dob=dob
                        ,mobile=phone,about=about,address=address).save()
                        sms.success(request,'Profile Updated.')
                        return redirect('ad_profile')
                    except Exception as e:
                        res['error']='All Field Required !'
                        return render(request,'profiles.html',res)
            
            elif request.POST.get('uss')!=None: 
                logo=request.POST['logo']
                favicon=request.POST['fav']
                title=request.POST['title']
                if favicon!='' and title!='' and logo!='':   
                    setting.objects.all().delete()
                    setting(title=title,logo=logo,favicon=favicon).save()
                    sms.success(request,'Profile Setting Updated.')
                    return redirect('ad_profile')
                elif favicon!='':
                    sett=setting.objects.all()
                    if len(sett)>0:
                        ob=sett[0]
                        ob.favicon=favicon
                        ob.save()
                        sms.success(request,'Profile Setting Updated.')
                        return redirect('ad_profile')
                elif logo!='':
                    sett=setting.objects.all()
                    if len(sett)>0:
                        ob=sett[0]
                        ob.logo=logo
                        ob.save()
                        sms.success(request,'Profile Setting Updated.')
                        return redirect('ad_profile')
                elif title!='':
                    sett=setting.objects.all()
                    if len(sett)>0:
                        ob=sett[0]
                        ob.title=title
                        ob.save()
                        sms.success(request,'Profile Setting Updated.')
                        return redirect('ad_profile')
            
        return render(request,'profiles.html',res)
    else:
        return redirect('ad_login')
def inst_detail(request,inst):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['inst']=instructor.objects.filter(slug=inst)
        res['crss']=course_detail.objects.filter(course_instructor=instructor.objects.get(slug=inst)).order_by('-id')
        res['odrprod']=products_purchase_order.objects.filter(user=instructor.objects.get(slug=inst).user.id).order_by('-id')

        print(res['odrprod'],'[[[[[[[[')
        paginator=Paginator(res['crss'],10)
        page_no=request.GET.get('page')
        res['crs']=paginator.get_page(page_no)
        res['tot']=len( res['crss'])
        nxt=request.get_full_path()
        if request.method=='POST':
                email=request.POST['email']
                name=request.POST['name']
                img=request.POST['img']
                expert=request.POST['expert']
                about=request.POST['about']
                if request.POST.get('inst')!=None:
                    pro= instructor.objects.filter(id=request.POST['inst'])
                    if len(pro)>0:
                        ob=pro[0]
                        ob.user=User.objects.get(id=request.user.id)
                        if len(name)>0:
                            ob.name=name
                        if len(img)>0:
                            ob.img=img
                        if len(email)>0:
                            ob.email=email
                        if len(expert)>0:
                            ob.expert=expert
                        if len(about)>0:
                            ob.about=about
                        ob.save()
                        sms.success(request,'Profile Updated.')
                        return redirect(nxt)    
            
        
        return render(request,'inst-stud-profile.html',res)
    else:
        return redirect('ad_login')


import itertools 
from itertools import chain
def stud_detail(request,stud):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['stud']=student.objects.filter(slug=stud)
        res['odrcrs']=courses_purchase_order.objects.filter(user=student.objects.get(slug=stud).user.id).order_by('-id')
        res['odrprod']=products_purchase_order.objects.filter(user=student.objects.get(slug=stud).user.id).order_by('-id')

        
        # for i in chn:
        #     print(i.order_date,'////////')
        # paginator=Paginator(res['chn'],10)
        # page_no=request.GET.get('page')
        # res['ordr']=paginator.get_page(page_no)
        # res['tots']=len( res['chn'])
        nxt=request.get_full_path()
        if request.method=='POST':
                email=request.POST['email']
                name=request.POST['name']
                img=request.POST['img']
                expert=request.POST['expert']
                about=request.POST['about']
                if request.POST.get('stud')!=None:
                    pro= student.objects.filter(id=request.POST['stud'])
                    if len(pro)>0:
                        ob=pro[0]
                        ob.user=User.objects.get(id=request.user.id)
                        if len(name)>0:
                            ob.name=name
                        if len(img)>0:
                            ob.img=img
                        if len(email)>0:
                            ob.email=email
                        if len(expert)>0:
                            ob.expert=expert
                        if len(about)>0:
                            ob.about=about
                        ob.save() 
                        sms.success(request,'Profile Updated.')
                        return redirect(nxt)
        return render(request,'inst-stud-profile.html',res)
    else:
        return redirect('ad_login')



def who_this(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['whos']=who_this_crs_for.objects.all().order_by('-id')
        paginator=Paginator(res['whos'],10)
        page_no=request.GET.get('page')
        res['who']=paginator.get_page(page_no)
        res['tot']=len(who_this_crs_for.objects.all())
        if request.method=='POST':
            
            if request.POST.get('crs')!=None:
                crs=request.POST['crs']
                title=request.POST['title']
                pro= who_this_crs_for(crs=crs,title=title)
                pro.save() 
                sms.success(request,'Element Added.')
                return redirect('who')
                
            elif request.POST.get('eid')!=None:
                        pro= who_this_crs_for.objects.filter(id=request.POST.get('eid'))
                        crs=request.POST['crss']
                        title=request.POST['title']
                        if len(pro)>0:
                            ob=pro[0]
                            if len(title)>0:
                                ob.title=title
                            if len(crs)>0:
                                ob.crs=crs
                            ob.save()
                            sms.success(request,'Updated successfully.')
                            return redirect('who')
            
            elif request.POST.get('did')!=None:
                        pro= who_this_crs_for(id=request.POST.get('did')).delete()
                        sms.success(request,'Deleted Successfully.')
                        return redirect('who')

        return render(request,'whothiscrs.html',res)
    else:
        return redirect('ad_login')


def blgele(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['blg']=blogdetail_element.objects.all().order_by('-id')
        paginator=Paginator(res['blg'],10)
        page_no=request.GET.get('page')
        res['blg']=paginator.get_page(page_no)
        res['tot']=len(blogdetail_element.objects.all())
        if request.method=='POST':
            
            if request.POST.get('eles')!=None:
                ele=request.POST['eles']
                pro= blogdetail_element(element=ele)
                pro.save() 
                sms.success(request,'Element Added.')
                return redirect('blgele')
                
            elif request.POST.get('bid')!=None:
                        pro= blogdetail_element.objects.filter(id=request.POST.get('bid'))
                        ele=request.POST['ele']
                        if len(pro)>0:
                            ob=pro[0]
                            if len(ele)>0:
                                ob.element=ele
                            ob.save()
                            sms.success(request,'Updated successfully.')
                            return redirect('blgele')
            
            elif request.POST.get('deid')!=None:
                        pro= blogdetail_element(id=request.POST.get('deid')).delete()
                        sms.success(request,'Deleted Successfully.')
                        return redirect('blgele')

        return render(request,'whothiscrs.html',res)
    else:
        return redirect('ad_login')




def add_coupon(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=='POST':
                code=request.POST['code']
                valid_date=request.POST['date']
                discount=request.POST['dis']
                pro= coupon_code(code=code,valid_date=valid_date,discount=discount)
                pro.save() 
                sms.success(request,'Coupon Added.')
                return redirect('coupons')
        return render(request,'addcoupon.html')
    else:
        return redirect('ad_login')


def coupons(request):
    if request.user.is_authenticated and request.user.is_superuser:
        res={}
        res['cop']=coupon_code.objects.all()
        nxt=request.get_full_path()
        if request.method=='POST':
            
                if request.POST.get('cid')!=None:
                    code=request.POST['code']
                    valid_date=request.POST['date']
                    discount=request.POST['dis']

                    pro= coupon_code.objects.filter(id=request.POST['cid'])
                    if len(pro)>0:
                        ob=pro[0]
                        if len(valid_date)>0:
                            ob.valid_date=valid_date
                        if len(discount)>0:
                            ob.discount=discount
                        if len(code)>0:
                            ob.code=code
                        ob.save()
                        sms.success(request,'Coupon Updated.')
                        return redirect(nxt)
                elif request.POST.get('did')!=None:
                    pro= coupon_code.objects.filter(id=request.POST['did'])
                    pro.delete()   
                    sms.success(request,'Coupon Deleted.')
                    return redirect(nxt)           

        return render(request,'coupons.html',res)
    else:
        return redirect('ad_login')

def error404(request):
    return render(request,'pages/404.html')

