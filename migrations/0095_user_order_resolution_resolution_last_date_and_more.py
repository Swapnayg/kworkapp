# Generated by Django 4.0.8 on 2022-11-04 12:51

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0094_supporttopic_slug_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_order_resolution',
            name='resolution_last_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 4, 12, 51, 46, 49788), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 4, 12, 51, 46, 50787), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 4, 12, 51, 46, 50787), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 4, 12, 51, 46, 50787), null=True),
        ),
    ]