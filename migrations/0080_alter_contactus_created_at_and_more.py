# Generated by Django 4.0.8 on 2022-10-27 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0079_buyer_requirements_order_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 26, 14, 219270), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 26, 14, 219270), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 26, 14, 222273), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 26, 14, 220272), null=True),
        ),
    ]
