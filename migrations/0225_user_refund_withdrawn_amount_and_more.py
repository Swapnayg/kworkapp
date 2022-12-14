# Generated by Django 4.0.8 on 2022-12-20 17:17

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0224_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_refund',
            name='withdrawn_amount',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user_refund',
            name='withdrawn_on',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='user_refund',
            name='withdrawn_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='withdrwal_initiated',
            name='initiated_type',
            field=models.CharField(blank=True, choices=[('initiated', 'Initiated'), ('pending', 'Pending'), ('partial', 'Partial'), ('sucess', 'Sucess')], default='', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='withdrwal_initiated',
            name='with_email',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 20, 17, 17, 32, 625995), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 20, 17, 17, 32, 625995), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 20, 17, 17, 32, 626995), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 20, 17, 17, 32, 626995), null=True),
        ),
        migrations.AlterField(
            model_name='user_transactions',
            name='transaction_status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('rufunded', 'Rufunded')], default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='withdrwal_initiated',
            name='withdrawan_status',
            field=models.CharField(blank=True, choices=[('earnings', 'Earnings'), ('refund', 'Refund')], default='', max_length=300, null=True),
        ),
    ]
