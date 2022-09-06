# from turtle import mode

from django.db import models


# Create your models here.


class Newsletter_subscriber(models.Model):
    suscriber_email=models.EmailField()

    def __str__(self):
        return self.suscriber_email


class New_Course(models.Model):
    c_price = models.IntegerField()
    c_image = models.ImageField()
    c_name = models.CharField(max_length=100)
    c_description = models.TextField(max_length=500)
