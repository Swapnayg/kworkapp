# Generated by Django 4.1.1 on 2022-10-23 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0042_alter_buyer_post_request_service_sub_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer_reviews',
            name='seller_response',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 19, 28, 49, 796537), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 19, 28, 49, 796537), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 19, 28, 49, 796537), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 19, 28, 49, 796537), null=True),
        ),
    ]
