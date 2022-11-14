# Generated by Django 4.0.8 on 2022-11-14 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0163_remove_withdrwal_initiated_order_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 14, 15, 2, 27, 478415), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 14, 15, 2, 27, 478415), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 14, 15, 2, 27, 478415), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 14, 15, 2, 27, 478415), null=True),
        ),
        migrations.AlterField(
            model_name='withdrwal_initiated',
            name='withdrawan_status',
            field=models.CharField(blank=True, choices=[('initiated', 'Initiated'), ('pending', 'Pending'), ('partial', 'Partial'), ('sucess', 'Sucess')], default='', max_length=300, null=True),
        ),
    ]
