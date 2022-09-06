import re

from django.shortcuts import render,HttpResponse,redirect

from django.contrib.auth.models import User
from course.models import course_detail
from shop.models import *
from user_profile.models import instructor, student

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
def pro(usr):
    li1=[]
    li=[]
    cht1=chats.objects.filter(msgto=usr).last()
    cht2=chats.objects.filter(msgby=usr).last()
    lis=list([cht1,cht2])
    for i in lis:
        li1.append(i.date)
    li1.sort(reverse=True)

    ins=instructor.objects.filter(slug=usr)
    stu=student.objects.filter(slug=usr)
    if ins:
       li.append({'cht':chats.objects.filter(date=li1[0]),'usr':ins})
    elif stu:
        li.append({'cht':chats.objects.filter(date=li1[0]),'usr':stu})
    
    return li



@login_required(login_url='loginregister')
def private_message(request,msg):
    res={}
    res['cht']=chats.objects.all()
    if request.user.userType.type=='2':
        st_crs=courses_purchase_order.objects.filter(user=User.objects.get(id=request.user.id),status='Success').values('course')
        inst={ course_detail.objects.get(id=i['course']).course_instructor  for i in st_crs}
        print(inst,'00000000')
        x1=[pro(i.slug) for i in inst]
        res['profil']=x1
        res['inst']=inst
        if request.GET.get('instructor')!=None:
            usr=request.GET.get('instructor')
        
        else:
            usre= list(inst)[0]
            usr=instructor.objects.get(name=usre).slug
        
        res['prof']=instructor.objects.filter(slug=usr)
        
        if request.method=='POST':
            msgs=request.POST['msg']
            chats(msg=msgs,msgto=usr,msgby=msg).save()
            return redirect(request.get_full_path())
        chat1=list(chats.objects.filter(msgby=msg,msgto=usr))
        chat2=list(chats.objects.filter(msgto=msg,msgby=usr))
        li=chat1+chat2
        lis=[]
        cht=[]
        for i in li:
            lis.append(i.date.strftime("%d-%b-%y,%H:%M:%S"))
        lis.sort() 
        for i in lis:
            for x in li:
                if x.date.strftime("%d-%b-%y,%H:%M:%S")==i:
                    cht.append(x)
        res['chat']=cht
    elif request.user.userType.type=='1':
        st_crs=courses_purchase_order.objects.filter(course__course_instructor__user=User.objects.get(id=request.user.id),status='Success').values('user')
        # res_list = [i for n, i in enumerate(list(st_crs)) if i not in list(st_crs)[n + 1:]]
        sts={ student.objects.get(user=i['user'])  for i in st_crs}
        # st={student.objects.filter(user=User.objects.get(id=i['user']))  for i in res_list}
        # print(sts,'00022200000')
        x1=[pro(i.slug) for i in sts]
        res['profil']=x1
        # if request.GET.get('find')!=None:
        #     stu={student.objects.filter(name__contains=request.GET.get('find'),user=User.objects.get(id=i['user'])) for i in res_list}
        # else: 
        #     stu=st 
        # em=[]
        # for i in st:
        #     x=i.values('slug')
        #     x1=[pro(xi['slug']) for xi in x]
        #     res['profil']=x1 
        res['stud']=sts
        if request.GET.get('student')!=None:
            usr=request.GET.get('student')
        else:
            us= list(sts)[0]
            usre=us[0]
            usr=student.objects.get(name=usre).slug
       
        res['prof']=student.objects.filter(slug=usr)
        res['ins']=instructor.objects.get(slug=msg).slug
        if request.method=='POST':
            msgs=request.POST['msg']
            chats(msg=msgs,msgto=usr,msgby=msg).save()
            return redirect(request.get_full_path())
        chat1=list(chats.objects.filter(msgby=msg,msgto=usr))
        chat2=list(chats.objects.filter(msgto=msg,msgby=usr))
        li=chat1+chat2
        lis=[]
        cht=[]
        for i in li:
            lis.append(i.date.strftime("%d-%b-%y,%H:%M:%S"))
        lis.sort() 
        for i in lis:
            for x in li:
                if x.date.strftime("%d-%b-%y,%H:%M:%S")==i:
                    cht.append(x)
        res['chat']=cht
    return  render(request,'priveate-message.html',res)

def profile_certificates(request,certificate):
    li=[]
    instruct=instructor.objects.filter(slug=certificate)
    stud=student.objects.filter(slug=certificate)
    
    if len(instruct)>0:
        res={'instruct':instruct}
    # elif len(stud)>0:
    #     res={'instruct':stud}
    if len(instruct)>0:
        usr=instructor.objects.get(slug=certificate)
        cr=course_detail.objects.filter(course_instructor=usr)
        for c in cr:
            if c.course_certificate!= '':
                li.append(c)
        res['crtfct']=li

    return  render(request,'profile-certificates.html',res)

@login_required(login_url='loginregister')
def setting_genralinfo(request,genralinfo):
    if request.user.is_authenticated:
        res={}
        nxt=request.get_full_path()
        instruct=instructor.objects.filter(slug=genralinfo)
        stud=student.objects.filter(slug=genralinfo)

        if request.method=='POST':
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                # name = request.POST.get('name')
                email = request.POST.get('email')
                about=request.POST.get('about')
                img = request.FILES.get('img')
                fb_social=request.POST.get('fb_social')
                tw_social=request.POST.get('tw_social')
                li_social=request.POST.get('li_social')
                yt_social=request.POST.get('yt_social')   
                user=User.objects.get(id=request.user.id)
                if len(fname)!=0:
                    user.first_name = fname
                if len(lname)!=0:
                    user.last_name = lname
                user.save()
                if len(instruct)>0: 
                    inst=instruct[0]
                    inst.user=user
                    if len(fname)!=0 :
                        inst.name=fname+' '+lname
                    if img!=None:
                        inst.img=img
                    if len(email)!=0:
                        inst.email=email
                    if len(about)!=0:
                        inst.about=about
                    if len(fb_social)!=0:
                        inst.facebook=fb_social
                    if len(tw_social)!=0:
                        inst.twitter=tw_social
                    if len(yt_social)!=0:
                        inst.youtube=yt_social
                    if len(li_social)!=0:
                        inst.linkedin=li_social
                    inst.save()
                    messages.success(request,'Profile Updated.')
                    return redirect(request.get_full_path())
                elif len(stud)>0: 
                        st=stud[0]
                        st.user=user
                        if len(fname)!=0:
                            st.name=fname+' '+lname
                        if img!=None:
                          st.img=img
                        if len(email)!=0:
                            st.email=email
                        if len(about)!=0:
                            st.about=about
                        if len(fb_social)!=0:
                            st.facebook=fb_social
                        if len(tw_social)!=0:
                            st.twitter=tw_social
                        if len(yt_social)!=0:
                            st.youtube=yt_social
                        if len(li_social)!=0:
                            st.linkedin=li_social
                        st.save()
                        messages.success(request,'Profile Updated.')
                        return redirect(request.get_full_path())
                else:
                    return redirect(nxt)
        if len(instruct)>0:
            res={'instruct':instruct}
        elif len(stud)>0:
            if request.user.is_authenticated:  
                if request.user.userType.type=='2':
                 res={'instruct':stud}
            else:
                return redirect('error')
        
    
        return  render(request,'setting-genralinfo.html',res)
    else:
        return redirect('error')


def settings_avatar(request,avatar):
    
    if request.user.is_authenticated:
        instruct=instructor.objects.filter(slug=avatar)
        stud=student.objects.filter(slug=avatar)

        # if request.method=='POST':
        #     img = request.FILES['img'] 
        #     if len(instruct)>0: 
        #         inst=instruct[0]
        #         inst.img=img
        #         inst.save()
        #     elif len(stud)>0: 
        #         st=stud[0]
        #         st.img=img
        #         st.save()
        # if len(instruct)>0:
        #     res={'instruct':instruct}
        # elif len(stud)>0:
        #     res={'instruct':stud}
        
        
        return  render(request,'settings-avatar.html')
    else:
        return redirect('error')

    
def settings_privacy(request,privacy):
    
    if request.user.is_authenticated:    
        # instruct=instructor.objects.filter(slug=privacy)
        # stud=student.objects.filter(slug=privacy)
        # if len(instruct)>0:
        #     res={'instruct':instruct}
        # elif len(stud)>0:
        #     res={'instruct':stud}

        

        return  render(request,'settings-privacy.html')
    else:
        return redirect('error')


@login_required(login_url='loginregister')
def change_pwd(request,pwd):
    
    if request.user.is_authenticated:  
        res={}
        instruct=instructor.objects.filter(slug=pwd)
        stud=student.objects.filter(slug=pwd)
        if len(instruct)>0:
            slg=instructor.objects.get(slug=pwd)
            res={'instruct':instruct}
        elif len(stud)>0:

            if request.user.is_authenticated:  
                if request.user.userType.type=='2':
                    slg=student.objects.get(slug=pwd)
                    res={'instruct':stud}
            else:
                return redirect('error')
      

        if request.method == "POST":
            old = request.POST['old']
            new = request.POST['new']
            confirm = request.POST['confrm']
            user = User.objects.get(id=request.user.id)
            mail=user.email
            check=user.check_password(old)
            if confirm==new:
                if check==True:
                    user.set_password(new)
                    user.save()
                    user=User.objects.get(email=mail)
                    login(request,user)
                    messages.success(request, "Password Updated")
                    return redirect(f'/change-password/{slg.slug}')
                else:
                    messages.error(request, "Incorrect Old Password")
                    return redirect(f'/change-password/{slg.slug}')
            else:
                messages.error(request,'New And Confirm Password Not Match.')
        
        # if len(instruct)>0:
        #     res={'instruct':instruct}
        # elif len(stud)>0:
        #     res={'instruct':stud}

        return  render(request,'change-password.html',res)
    else:
        return redirect('error')


def profile(request,profile):
        res={}
        instruct=instructor.objects.filter(slug=profile)
        stud=student.objects.filter(slug=profile)
        
        if len(instruct)>0:
            ins=instructor.objects.get(slug=profile)
            inst_crs=course_detail.objects.filter(course_instructor=ins).count()
            res={'instruct':instruct,
            'inst_crs':inst_crs
            }
        elif  len(stud)>0 :    
            if request.user.is_authenticated:  
                if request.user.userType.type=='2':
                 res={'instruct':stud}
            else:
                return redirect('error')
        if request.user.is_authenticated:
            if request.user.userType.type=='1':
                cr=course_detail.objects.filter(course_instructor=instructor.objects.get(slug=profile))
                totl=0
                for c in cr:
                    crs=courses_purchase_order.objects.filter(course=c).count()
                    totl+=crs
                res['stud']=totl
            elif request.user.userType.type=='2':
                totl=0
                us=User.objects.get(id=request.user.id)
                crs=courses_purchase_order.objects.filter(user=us,status='Success').count()
                totl+=crs
                res['corse_prchase']=totl
            # else:
            #     res={'instruct':stud}
        return  render(request,'profile.html',res)
   
def success_story(request):
    return  render(request,'success-story.html')


def instructors(request):
    inst=instructor.objects.all()
    res={'instructor':inst}
    return  render(request,'instructor.html',res)


@login_required(login_url='loginregister')
def orders(request,order):
    res={}
    instruct=instructor.objects.filter(slug=order)
    stud=student.objects.filter(slug=order)
    if len(instruct)>0:
        res={'instruct':instruct}
    elif len(stud)>0:
        if request.user.is_authenticated:  
            if request.user.userType.type=='2':
                 res={'instruct':stud}
        else:
                return redirect('error')
      
    if request.user.is_authenticated:   
        c=User.objects.get(id=request.user.id)
        res['crs_oder']=courses_purchase_order.objects.filter(user=c,status='Success')
        res['prod_oder']=products_purchase_order.objects.filter(user=c,status='Success')
    return  render(request,'orders.html',res)


def quzess(request,quize):
    
    
    instruct=instructor.objects.filter(slug=quize)
    stud=student.objects.filter(slug=quize)
    
    if len(instruct)>0:
        res={'instruct':instruct}
    # elif len(stud)>0:
    #     res={'instruct':stud}

    return  render(request,'quzess.html',res)
