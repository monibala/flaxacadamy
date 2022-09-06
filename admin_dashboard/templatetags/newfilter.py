


import imp
from posixpath import split
from django import template
from admin_dashboard.models import *
from course.models import *
from login_register.models import userType
from shop.models import courses_purchase_order, products_purchase_order
register = template.Library()

@register.filter(name='splt')
def splt(value,key):
    return  value.split(key)[0]


@register.filter(name='crs_count')
def crs_count(value):
    inst=instructor.objects.get(id=value)
    return course_detail.objects.filter(course_instructor=inst).count()


@register.filter(name='ordr')
def ordr(value):
    usr=User.objects.get(id=value)
    cou=courses_purchase_order.objects.filter(user=usr).count()+products_purchase_order.objects.filter(user=usr).count()
    print(cou,'////')
    return cou

# @register.filter(name='prod_ordr')
# def prod_ordr(value):
#     usr=User.objects.get(id=value)
#     return products_purchase_order.objects.filter(user=usr).count()

# @register.filter(name='parts')
# def parts(value,key):
#     return (value[:int(key)]+'\n'+value[int(key):int(key*2)]+'\n'+value[int(key*2):int(key*3)]+'\n'+value[int(key*3):int(key*4)]+'\n'+value[int(key*4):int(key*5)]+'\n'+value[int(key*6):])



@register.filter(name='imgs')
def imgs(value):
    usr=User.objects.get(id=value)
    return admin_profile.objects.get(user=usr).img


@register.filter(name='part')
def part(value):
    return value[:10]+'\n'+value[10:20]+'\n'+value[30:40]+'\n'+value[40:50]+'\n'+value[50:60]+'\n'+value[60:]



@register.filter(name='partion')
def part(value):
    return value[:50]+'\n'+value[50:100]+'\n'+value[100:]



@register.filter(name='getContact')
def getContact(value):
    return setting.objects.all()


# @register.filter(name='settings')
# def settings(value):
#     data = setting.objects.values(value)
#     if data.exists():
#         return data[0]    





@register.filter(name='add_class')
def add_class(value,arg):

    classess=value.field.widget.attrs.get('class','')
    if classess:
        classess=classess.split('')
    else:
        classess=[]
    new_class=arg.split(' ')
    for c in new_class:
        if c not in classess:
            classess.append(c)
    return value.as_widget(attrs={'class':' '.join(classess)})








