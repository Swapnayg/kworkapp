# Generated by Django 4.0.8 on 2022-11-08 20:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0126_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 20, 44, 58, 12387), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 20, 44, 58, 12387), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 20, 44, 58, 12387), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 20, 44, 58, 12387), null=True),
        ),
        migrations.AlterField(
            model_name='user_earnings',
            name='clearence_status',
            field=models.CharField(blank=True, choices=[('cleared', 'Cleared'), ('pending', 'Pending')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user_earnings',
            name='earning_type',
            field=models.CharField(blank=True, choices=[('order', 'Order'), ('affiliate', 'Affiliate'), ('tip', 'Tip'), ('cancelled', 'Cancelled')], default='', max_length=300, null=True),
        ),
    ]