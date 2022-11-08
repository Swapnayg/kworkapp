# Generated by Django 4.0.8 on 2022-11-06 16:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0108_user_order_resolution_resolution_cancel_mssg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_earnings',
            name='order_amount',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user_earnings',
            name='platform_fees',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 6, 16, 44, 27, 346482), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 6, 16, 44, 27, 346482), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 6, 16, 44, 27, 346482), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 6, 16, 44, 27, 346482), null=True),
        ),
        migrations.AlterField(
            model_name='user_earnings',
            name='clearence_status',
            field=models.CharField(blank=True, choices=[('cleared', 'Cleared'), ('pending', 'Pending')], default='', max_length=300, null=True),
        ),
    ]