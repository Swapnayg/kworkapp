# Generated by Django 4.0.8 on 2022-11-05 22:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0106_remove_user_refund_aval_with_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_warning',
            name='spamword',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.spamdetection'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 44, 10, 834894), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 44, 10, 850520), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 44, 10, 850520), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 22, 44, 10, 850520), null=True),
        ),
        migrations.AlterField(
            model_name='user_warning',
            name='confirmed_status',
            field=models.BooleanField(default=False),
        ),
    ]
