
from operator import mod
from django.db import models

# Create your models here.

from user_profile.models import*

from user_profile.models import slug_generator

class who_this_crs_for(models.Model):
    crs=models.CharField(max_length=1000)
    title=models.TextField()
    def __str__(self):
        return   self.crs[:25]+' - '+(self.title[:10])

from ckeditor.fields import RichTextField
class course_detail(models.Model):
    course_instructor=models.ForeignKey(instructor,on_delete=models.CASCADE,related_name='course_instructor_detail')
    course_price=models.IntegerField(default='Free')
    course_img=models.ImageField(upload_to='image/course/')
    course_title=models.CharField(max_length=1000,unique=True) 
    slug=models.SlugField(max_length=1000,unique=True)  
    short_course_description=RichTextField(blank=True,null=True) 
    course_description=RichTextField()
    lession_no=models.IntegerField(default=0)
    student_no=models.IntegerField(default=0)
    course_duration_in_weeks=models.IntegerField(default=0)
    category=models.CharField(max_length=100)
    course_certificate=models.FileField(blank=True,null=True)
    who_this_course=models.ManyToManyField(who_this_crs_for,blank=True)
    course_quiz=models.CharField(max_length=100,blank=True,null=True)


    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slug_generator(course_detail,self.course_title)
        super(course_detail, self).save(*args, **kwargs)
  
    def __str__(self):
        return   (self.course_title)




class crs_review(models.Model):
    crs=models.ForeignKey(course_detail,on_delete=models.CASCADE,null=True,related_name='course_review')
    comment=models.TextField()
    rate=models.IntegerField(null=True)
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    dateby=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return  self.name.username
