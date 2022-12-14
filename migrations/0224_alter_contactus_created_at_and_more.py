# Generated by Django 4.0.8 on 2022-12-19 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0223_user_orders_incoming_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 19, 17, 55, 16, 45766), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 19, 17, 55, 16, 45766), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 19, 17, 55, 16, 47764), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 19, 17, 55, 16, 46764), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='referrals_earnings',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
    ]
