from django.contrib import admin
from django.urls import path,include
from shop import views

urlpatterns = [
  

  path('cart/', views.mycart, name='cart'),

  path('checkout/', views.checkout, name='checkout'),


  path('lp-checkout/', views.lp_checkout, name='lp-checkout'),


  path('purchase-guide/', views.purchase_guide, name='purchase-guide'),

  path('order-booked/', views.order_book, name='book'),

  path('shop/', views.shop, name='shop'),

  path('shop-detail/<slug:shops>', views.single_shop, name='single-shop'),

  path('add-to-cart/<slug:addcart>',views.add_to_cart,name='add-to-cart'),
  
  path('order/',views.order,name='order'),
  
  path('product-detail/<int:id>',views.detail,name='product-detail'),


  # path("paytm/", views.paytms, name="paytms"),
  path("handlerequest/", views.handle_request, name="HandleRequest"),
  ]