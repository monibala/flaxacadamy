from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class userType(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="userType")
    type = models.CharField(max_length=20,choices=(("1",'instructor'),
                ("2","student")))

    def __str__(self):
        return self.user.username


class frgt_pwd(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='forgot_password')
    frg_token=models.CharField(max_length=1000)
    def __str__(self):
        return self.user.username