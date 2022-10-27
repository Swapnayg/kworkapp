# Generated by Django 4.1.1 on 2022-10-10 07:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0031_user_created_at_user_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 7, 34, 59, 947568), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 7, 34, 59, 947568), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 7, 34, 59, 947568), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 7, 34, 59, 947568), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avg_delivery_time',
            field=models.CharField(blank=True, default='1', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_delivery',
            field=models.CharField(blank=True, default='1', max_length=500, null=True),
        ),
    ]
