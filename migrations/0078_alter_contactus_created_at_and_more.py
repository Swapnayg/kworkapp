# Generated by Django 4.0.8 on 2022-10-27 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0077_user_order_resolution_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 16, 35, 405574), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 16, 35, 405574), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 16, 35, 406575), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 16, 35, 405574), null=True),
        ),
    ]
