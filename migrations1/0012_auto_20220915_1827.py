# Generated by Django 3.2.13 on 2022-09-15 18:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0011_auto_20220915_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 15, 18, 27, 25, 427327), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 15, 18, 27, 25, 427327), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 15, 18, 27, 25, 428327), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 15, 18, 27, 25, 427327), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_type',
            field=models.CharField(blank=True, choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userlanguages',
            name='lang_prof',
            field=models.CharField(blank=True, choices=[('Basic', 'Basic'), ('Fluent', 'Fluent'), ('Conversational', 'Conversational')], default='Basic', max_length=200, null=True),
        ),
    ]
