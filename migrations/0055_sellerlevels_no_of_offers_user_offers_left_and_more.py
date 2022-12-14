# Generated by Django 4.1.1 on 2022-10-16 19:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0054_buyer_post_request_buyer_request_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerlevels',
            name='No_of_offers',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='offers_left',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 56, 54, 21430), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 56, 54, 21430), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 56, 54, 22431), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 56, 54, 22431), null=True),
        ),
    ]
