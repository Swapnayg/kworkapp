# Generated by Django 4.0.8 on 2022-11-19 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0188_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomNotifications',
            new_name='KworkCustomNotifications',
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 19, 15, 46, 57, 652443), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 19, 15, 46, 57, 652443), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 19, 15, 46, 57, 653445), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 19, 15, 46, 57, 653445), null=True),
        ),
    ]
