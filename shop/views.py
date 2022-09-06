
from urllib import request
from django.shortcuts import render,redirect
from django.db.models import Count
from login_register.views import register
from .models import *
from django.core.paginator import Paginator
from course.models import*
from blog.models import*
from datetime import date, datetime

from django.contrib import messages
# for pyment integration
from math import ceil
import json
from .paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
# from .checksum import  generate_checksum, verify_checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';
from django.db.models import Sum,Avg

from django.contrib.auth.decorators import login_required
# Create your views here.
def shop(request):
    prod=product_detail.objects.all()
    lis=[]
    for x in product_detail.objects.all():
        try:    
            tot=cunt=0 
            if len(product_review.objects.filter(product=x))!=0:
                for i in product_review.objects.filter(product=x):
            
                    cunt+=i.rate
                tot=cunt/len(product_review.objects.filter(product=x))
                x.rating=tot
                x.save()
                lis.append({'id':x.id,'tot':int(format(tot,'.0f'))})
            else: 
                lis.append({'id':x.id,'tot':int(format(0,'.0f'))})
        except ZeroDivisionError:
                pass  
    
    if request.GET.get('category') != None:
        product_detl=product_detail.objects.filter(category=request.GET.get('category'))
    elif request.GET.get('tag') != None:
        product_detl=product_detail.objects.filter(product_tag=request.GET.get('tag'))
    elif request.GET.get('orderby') != None and request.GET.get('orderby') == 'menu_order':
        product_detl=product_detail.order_by('id')
    elif request.GET.get('orderby') != None and  request.GET.get('orderby') == 'popularity':
        product_detl=product_detail.objects.order_by('id')
    elif request.GET.get('orderby') != None and  request.GET.get('orderby') == 'price-desc':
        product_detl=product_detail.objects.order_by('-product_price')
    elif request.GET.get('orderby') != None and request.GET.get('orderby') == 'date':
        product_detl=product_detail.objects.order_by('-id')
    elif request.GET.get('orderby') != None and request.GET.get('orderby') == 'price':
        product_detl=product_detail.objects.order_by('product_price')
   
    else:
        product_detl=product_detail.objects.order_by('id')

    paginator=Paginator(product_detl,6)
    page_no=request.GET.get('page')
    products=paginator.get_page(page_no)
     
    
    dis=[]
    for p in products:
                dis.append({
                    'id':p.id,'disc':"{:.0f}".format(p.product_price-(p.product_price*p.discount/100)) })
    res={'product':products,'rate_count':lis,'discunt':dis,
    'count':product_detail.objects.all().count,
    'result_count':len(product_detl)}
    return  render(request,'shop.html',res)

def single_shop(request,shops):
    prod=product_detail.objects.all()
    product_detl=product_detail.objects.filter(slug=shops)
    # rt_count=[]
    # for p in prod:
    #     rt=product_review.objects.filter(product=p).aggregate(Count('rate'))
    #     rt['id']=p.id
    #     rt_count.append(rt)
    if request.method=='POST':
        if request.user.is_authenticated:
            review=request.POST['review']
            rate=request.POST['rate']
            usr=User.objects.get(id=request.user.id)
            shop=product_detail.objects.get(slug=shops)
            rvw=product_review(product=shop,review=review,rate=rate,user=usr)
            rvw.save()
            messages.success(request,'Review Posted.')
            return redirect(request.get_full_path())
        else:
            messages.warning(request,'Please Login Or Register.')
            return redirect('login')
    lis=[]
    for x in product_detail.objects.all():
        try:    
            tot=cunt=0 
            if len(product_review.objects.filter(product=x))!=0:
                for i in product_review.objects.filter(product=x):
            
                    cunt+=i.rate
                tot=cunt/len(product_review.objects.filter(product=x))
                x.rating=tot
                x.save()
                lis.append({'id':x.id,'tot':int(format(tot,'.0f'))})
            else: 
                lis.append({'id':x.id,'tot':int(format(0,'.0f'))})
        except ZeroDivisionError:
                pass  
    dis=[]
    for p in prod:
                dis.append({
                    'id':p.id,'disc':"{:.0f}".format(p.product_price-(p.product_price*p.discount/100)) })
   

    res={'product':product_detl,'rlt_product':prod,'discunt':dis,
    'rate_count':lis}
    return  render(request,'single-shop.html',res)

@login_required(login_url='loginregister')
def mycart(request):
    cartlist=cart.objects.filter(userid=request.user.id)
    li=[]
    res={}
    total=0

    dlt_item_id=request.GET.get('delete')
    slg=request.GET.get('slg')
    crt=cart.objects.filter(prod_id=dlt_item_id,slug=slg)
    crt.delete()
  
    for c in cartlist:
        prod=product_detail.objects.filter(id=c.prod_id,slug=c.slug)
        crs=course_detail.objects.filter(id=c.prod_id,slug=c.slug)
        
        if len(prod)>0:
            prod=product_detail.objects.get(id=c.prod_id)
            subtotal=prod.product_price*c.quntity
            total+=subtotal
            c.total=total
            c.save()
            li.append([prod,c.quntity,subtotal])
        elif len(crs)>0:
            prod=course_detail.objects.get(id=c.prod_id)
            subtotal=prod.course_price*c.quntity
            total+=subtotal
            c.total=total
            c.save()
            li.append([prod,c.quntity,subtotal])
    if request.method=='POST':
        cou_code=request.POST.get('coupon_code')
        if cou_code.isdigit():
            cd=coupon_code.objects.filter(code=cou_code)
            if len(cd)>0:
                cod=coupon_code.objects.get(code=cou_code)
                for c in cartlist:
                    c.coupon=cod.code 
                    c.save()
                # messages.success(request,'Coupon Applied.')
                if cod.valid_date>date.today():
                    cd=int((cod.discount*total)/100)
                    total=total-cd
                    c.total=total
                    c.save()
                    messages.success(request,'Coupon Applied.')
                else:
                    messages.warning(request,'Coupon Expire !')
                    return  redirect('cart')   
            else:
                    messages.error(request,'Invalid Coupon !')
                    return  redirect('cart')   
        else:
                    messages.error(request,'Invalid Coupon Code !')
                    return  redirect('cart')
   
    res={'cart':li,'total':total}
    return  render(request,'cart.html',res)


@login_required(login_url='loginregister')
def add_to_cart(request,addcart):
    if request.user.is_authenticated:
        carts=cart.objects.all()
        products=product_detail.objects.filter(slug=addcart)
        crs=course_detail.objects.filter(slug=addcart)   
        if len(products)==1:
            product=product_detail.objects.get(slug=addcart)
            prods=cart.objects.filter(prod_id=product.id,userid=request.user.id,slug=product.slug)
            if len(prods)>0:
                prod=prods[0]
                prod.quntity+=1
                prod.save()
            else:
                prod=cart.objects.create(slug=product.slug,userid=request.user.id,prod_id=product.id,
                prod_name=product.product_title,quntity=1)
        elif len(crs)==1:
            courses=course_detail.objects.get(slug=addcart)
            alredy_crs=courses_purchase_order.objects.filter(course=courses,user=User.objects.get(id=request.user.id))
            prods=cart.objects.filter(prod_id=courses.id,userid=request.user.id,slug=courses.slug)
            print(alredy_crs,'ppppppppppp')
            if len(alredy_crs)!=1:
                if len(prods)>0:
                    if len(prods)>0:
                        prod=prods[0]
                        prod.quntity=1
                        prod.save()
                        messages.warning(request,'Course Already In Cart.')
                else:
                    prod=cart.objects.create(slug=courses.slug,userid=request.user.id,prod_id=courses.id,prod_name=courses.course_title,quntity=1)
            else:
                messages.warning(request,'You Are Already Enrolled This Course.')
                return redirect(request.META['HTTP_REFERER'])
        return redirect('cart')
    else:
        messages.warning(request,'Please Login Or Register.')
        return redirect('loginregister')


@login_required(login_url='loginregister')
def checkout(request):
    cartlist=cart.objects.filter(userid=request.user.id)
    li=[]
    res={}
    total=0
    for c in cartlist:
        prod=product_detail.objects.filter(id=c.prod_id,slug=c.slug)
        crs=course_detail.objects.filter(id=c.prod_id,slug=c.slug)
        
        if len(prod)>0:
            prod=product_detail.objects.get(id=c.prod_id)
            subtotal=prod.product_price*c.quntity
            total+=subtotal
            
            li.append([prod,c.quntity,subtotal]) 
            cd=coupon_code.objects.filter(code=c.coupon)
            if len(cd)>0:
                cod=coupon_code.objects.get(code=c.coupon)
                if cod.valid_date>date.today():
                    cd=int((cod.discount*total)/100)
                    total=total-cd
                    # c.total=total
                 
        elif len(crs)>0:
            prod=course_detail.objects.get(id=c.prod_id)
            subtotal=prod.course_price*c.quntity
            total+=subtotal
            # c.total=total
            cd=coupon_code.objects.filter(code=c.coupon)
            li.append([prod,c.quntity,subtotal])
            if len(cd)>0:
                cod=coupon_code.objects.get(code=c.coupon)
                if cod.valid_date>date.today():
                    cd=int((cod.discount*total)/100)
                    total=total-cd
                    # c.total=total
            
        res={'cart':li,'total':total}
    return render(request, 'checkout.html',res)

@login_required(login_url='loginregister')
def order(request):
    cartlist=cart.objects.filter(userid=request.user.id)
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        country=request.POST['country']
        address=request.POST['address']
        address2=request.POST.get('address2')
        city=request.POST['city']
        postal_code=request.POST['postal_code']
        province=request.POST['state']
        phone=request.POST['phone']
        payment_method=request.POST['payment_method']
        comapny=request.POST.get('company')
        order_notes=request.POST.get('order_notes')
        upt=update_order(user=User.objects.get(id=request.user.id))
        upt.save()
        for c in cartlist:
            prod=product_detail.objects.filter(id=c.prod_id,slug=c.slug)
            crs=course_detail.objects.filter(id=c.prod_id,slug=c.slug)
        
            if len(prod)>0:
                prod=product_detail.objects.get(id=c.prod_id)
                subtotal=prod.product_price*c.quntity
                cd=coupon_code.objects.filter(code=c.coupon)
                if len(cd)>0:
                    cod=coupon_code.objects.get(code=c.coupon)
                    if cod.valid_date>date.today():
                        cd=int((cod.discount*subtotal)/100)
                        subtotal-=cd
                user=User.objects.get(id=c.userid)
                orders=products_purchase_order(product=prod,user=user,fname=fname,lname=lname,email=email,phone=phone,country=country,city=city,
                address=address+' '+address2,company=comapny,province=province,postal_code=postal_code,payment=payment_method,
                order_notes=order_notes,quntity=c.quntity,amount=subtotal,order_id=uuid.uuid4())
                orders.save()
                upt.prod_orders.add(orders)
                upt.save()
                prods = product_detail.objects.filter(id=c.prod_id)
                qunt=prod.quntity-c.quntity
                if len(prods)>0:
                        ob=prods[0]
                        ob.quntity=qunt
                        ob.save()
                amt=cart.objects.values('total').filter(userid=request.user.id).last()       
            elif len(crs)>0:
                crs=course_detail.objects.get(id=c.prod_id)
                subtotal=crs.course_price*c.quntity
                cd=coupon_code.objects.filter(code=c.coupon)              
                if len(cd)>0:
                    cod=coupon_code.objects.get(code=c.coupon)
                    if cod.valid_date>date.today():
                        cd=int((cod.discount*subtotal)/100)
                        subtotal-=cd
                user=User.objects.get(id=c.userid)
                orders=courses_purchase_order(course=crs,user=user,fname=fname,lname=lname,email=email,phone=phone,country=country,city=city,
                address=address+' '+address2,company=comapny,province=province,postal_code=postal_code,payment=payment_method,
                order_notes=order_notes,quntity=c.quntity,amount=subtotal,order_id=uuid.uuid4())
                orders.save()
                upt.crs_orders.add(orders)
                upt.save()
                crss = course_detail.objects.filter(id=c.prod_id)
                if len(crss)>0:
                        ob=crss[0]
                        ob.student_no+=1
                        ob.save()
                amt=cart.objects.values('total').filter(userid=request.user.id).last()
                
        # print(update_order.objects.all(),'kkkkkkkkk')       
        param_dict={
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(upt.updt_id),
            'TXN_AMOUNT': str(format(amt['total'],'.2f')),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            # 'CALLBACK_URL':'https://cyberacdamy.herokuapp.com/handlerequest/',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/', 

            }  
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'paytms.html', {'param_dict': param_dict})
        
    return redirect('checkout')

@csrf_exempt
def handle_request(request):
    
    # paytm will send you post request here
    form = request.POST
    res_dict = {}
    for i in form.keys():
        res_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(res_dict, MERCHANT_KEY, checksum)
    if verify:
        if res_dict['RESPCODE'] == '01':
            upt=update_order.objects.filter(updt_id=res_dict["ORDERID"])
            if len(upt)>0:
                for i in upt:
                    print(i.crs_orders.all(),'pppp')
                    for c in i.crs_orders.all():
                        courses_purchase_order.objects.filter(order_id=c.order_id).update(status="Success") 
                    for p in i.prod_orders.all():
                        products_purchase_order.objects.filter(order_id=p.order_id).update(status="Success")
                PaytmTransaction(**res_dict).save()
               
            return redirect('book')   
        else:
            # messages.error(request,'Payment was unsuccessful because  '  + res_dict['RESPMSG'])
            
            messages.error(request,'Somthing Went Wrong ! your order is failed.')
            return redirect('checkout')
    return render(request, 'paymentstatus.html', {'response': res_dict})



def order_book(request):
    inst=instructor.objects.filter(user=User.objects.get(id=request.user.id))
    stud=student.objects.filter(user=User.objects.get(id=request.user.id))

    cartlist=cart.objects.filter(userid=request.user.id)
    cartlist.delete()
    upt=update_order.objects.filter(user=User.objects.get(id=request.user.id)).delete()
    messages.success(request,'Order Saved Successfully.\n Order Payment success.')
    if len(inst)>0:
        return redirect('orders',order=instructor.objects.get(user=User.objects.get(id=request.user.id)).slug )
    elif len(stud)>0:
        return redirect('orders',order=student.objects.get(user=User.objects.get(id=request.user.id)).slug)


def purchase_guide(request):
    blg_tag=blog_detail.objects.values('tags')
    tag1={t['tags'] for t in blg_tag}

    prod_tag=product_detail.objects.values('product_tag')
    tag2={t['product_tag'] for t in prod_tag}
    tg=tag1.union(tag2)
    
    res={'tag':tg}
    
    return render(request,'purchase-guide.html',res)

def lp_checkout(request):
    return  render(request,'lp-checkout.html')


def detail(request,id):
    product_detl=product_detail.objects.filter(id=id)
    return redirect('shop',{'det':product_detl})


