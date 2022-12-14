# Generated by Django 4.0.8 on 2022-10-26 20:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0075_user_orders_due_date_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avail_bal',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='cancelled_earning',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='total_earning',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 20, 45, 54, 559344), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 20, 45, 54, 559344), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 20, 45, 54, 561344), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 20, 45, 54, 560344), null=True),
        ),
    ]
