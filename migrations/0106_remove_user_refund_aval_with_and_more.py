# Generated by Django 4.0.8 on 2022-11-05 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0105_order_delivery_resolution_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_refund',
            name='aval_with',
        ),
        migrations.RemoveField(
            model_name='user_refund',
            name='cleared_on',
        ),
        migrations.RemoveField(
            model_name='user_refund',
            name='clearence_date',
        ),
        migrations.RemoveField(
            model_name='user_refund',
            name='clearence_status',
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 0, 27, 364526), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 0, 27, 364526), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 0, 27, 364526), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 0, 27, 364526), null=True),
        ),
    ]
