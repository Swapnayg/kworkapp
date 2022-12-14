# Generated by Django 4.0.8 on 2022-11-20 11:29

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0190_rename_kworkcustomnotifications_customnotifications_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 20, 11, 29, 26, 934778), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 20, 11, 29, 26, 934778), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 20, 11, 29, 26, 936778), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 20, 11, 29, 26, 935777), null=True),
        ),
    ]
