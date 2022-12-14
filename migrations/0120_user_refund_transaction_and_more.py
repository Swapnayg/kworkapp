# Generated by Django 4.0.8 on 2022-11-08 17:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0119_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_refund',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.user_transactions'),
        ),
        migrations.AddField(
            model_name='user_transactions',
            name='credit_ref_numbers',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 17, 45, 45, 761550), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 17, 45, 45, 761550), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 17, 45, 45, 761550), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 8, 17, 45, 45, 761550), null=True),
        ),
        migrations.AlterField(
            model_name='user_transactions',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('paypal', 'Paypal'), ('flutterwave', 'Flutterwave'), ('credit', 'Credit')], default='', max_length=300, null=True),
        ),
    ]
