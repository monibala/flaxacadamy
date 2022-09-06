
from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class contact_msg(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='contact_message')
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=500)
    Msg=models.TextField()
    def __str__(self):
        return self.name

class operation_hours(models.Model):
    day_start=models.CharField(max_length=50)
    day_end=models.CharField(max_length=50)
    time_start=models.TimeField()
    time_end=models.TimeField()
    def __str__(self):
        return self.day_start+' '+self.day_end

class contact_page_info(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    about_contact=models.TextField(null=True,blank=True)
    address=models.TextField()
    mail=models.EmailField()
    gmail=models.EmailField()
    mobile=models.IntegerField()
    phone=models.IntegerField()
    hour=models.ManyToManyField(operation_hours)
    def __str__(self):
        return self.user.username
