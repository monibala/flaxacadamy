
from django.urls import path,include
from admin_dashboard import views

urlpatterns = [
    
  path('', views.ad_dash, name='ad_dash'),
  
  # path('admin-register/', views.ad_register, name='ad_register'),
  path('admin-login/', views.ad_login, name='ad_login'),
  
  
  path('password-change/<str:id>/', views.pwd_reset_change, name='pwd_reset_change'),
  path('admin-logout/', views.ad_logout, name='ad_logout'),
  path('admin-reset-password/', views.ad_forgot_pwd, name='ad_forgot_pwd'),

  path('admin-profile/', views.ad_profile, name='ad_profile'),

  path('profile-detail/<slug:inst>', views.inst_detail, name='inst_detail'),
  path('profile-details/<slug:stud>', views.stud_detail, name='stud_detail'),

  
  
  path('Blog-Elements/', views.blgele, name='blgele'),
  path('Who-use-this-courses/', views.who_this, name='who'),
  path('coupons/', views.coupons, name='coupons'),
  path('add-coupons/', views.add_coupon, name='add_coupon'),
  
  path('event-detail/', views.ad_event, name='ad_event'),
  path('product-detail/', views.ad_product, name='ad_product'),
  path('course-detail/', views.ad_crs, name='ad_course'),
  path('blog-detail/', views.ad_blogs, name='ad_blog'),
  path('instrucor-detail/', views.inst, name='inst'),
  path('student-detail/', views.stud, name='stud'),
  
  path('add-blog/', views.add_blog, name='add_blog'),
  path('add-course/', views.add_crs, name='add_crs'),
  path('add-event/', views.add_event, name='add_event'),
  path('add-product/', views.add_product, name='add_product'),
  
  path('page-not-found/', views.error404, name='404'),
  path('transactions/', views.payments, name='payments'),
  path('search-query/', views.srch, name='srch'),
  # path('profile-detail/', views.detail, name='detail'),

  
  # path('product-detail/', views.ad_product, name='ad_product'),
  # path('product-detail/', views.ad_product, name='ad_product'),
  # path('product-detail/', views.ad_product, name='ad_product'),
  # path('product-detail/', views.ad_product, name='ad_product'),
  # path('product-detail/', views.ad_product, name='ad_product'),


  
]
