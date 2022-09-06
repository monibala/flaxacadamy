from django.contrib import admin
from .models import*
# Register your models here.
@admin.register(product_detail)
class product_detailAdmin(admin.ModelAdmin):
    list_display=['category','product_tag','product_title'[:20]]

@admin.register(update_order)
class updt_odrAdmin(admin.ModelAdmin):
    list_display=['user']

@admin.register(PaytmTransaction)
class payAdmin(admin.ModelAdmin):
    list_display=['ORDERID']


@admin.register(product_review)
class shop_review(admin.ModelAdmin):
    
    list_display_links=('product','user','id')
    list_display=['id','user','product'[:20],'rate','review']


@admin.register(cart)
class cart(admin.ModelAdmin):
    
    list_display_links=('userid','prod_name','id')
    list_display=['id','userid','prod_name','prod_id','quntity']


@admin.register(products_purchase_order)
class product_order(admin.ModelAdmin):
    
    list_display_links=('user',)
    list_display=['user','product','address','fname','amount']


@admin.register(courses_purchase_order)
class course_order(admin.ModelAdmin):
    
    list_display_links=('user',)
    list_display=['user','course','address','status','fname','amount']


@admin.register(coupon_code)
class coupon_code(admin.ModelAdmin):
    
    list_display_links=('code','id')
    list_display=['id','code','valid_date','discount']
