# Generated by Django 3.2.6 on 2022-02-21 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_courses_purchase_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses_purchase_order',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='products_purchase_order',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
    ]