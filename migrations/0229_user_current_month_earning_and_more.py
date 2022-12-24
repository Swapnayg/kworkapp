# Generated by Django 4.0.8 on 2022-12-22 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0228_referral_users_refer_date_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_month_earning',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 22, 17, 24, 51, 686126), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 22, 17, 24, 51, 686126), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 22, 17, 24, 51, 686126), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 22, 17, 24, 51, 686126), null=True),
        ),
        migrations.AlterField(
            model_name='user_order_activity',
            name='activity_type',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('delivered', 'Delivered'), ('cancel', 'Cancelled'), ('e_cancel', 'E_Cancelled'), ('extension', 'Extension'), ('completed', 'Completed'), ('transaction', 'Transaction'), ('withdrawal', 'Withdrawal'), ('credit', 'Credit'), ('pending', 'Pending'), ('cleared', 'Cleared'), ('tip', 'tip'), ('affiliate', 'Affiliate'), ('used_credit', 'Credits Used')], default='', max_length=300, null=True),
        ),
    ]