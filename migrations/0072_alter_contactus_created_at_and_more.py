# Generated by Django 4.0.8 on 2022-10-26 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0071_remove_user_orders_user_id_user_orders_offer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 16, 36, 13, 695309), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 16, 36, 13, 695309), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 16, 36, 13, 695309), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 16, 36, 13, 695309), null=True),
        ),
        migrations.AlterField(
            model_name='user_orders',
            name='order_status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('delivered', 'Delivered'), ('cancel', 'Cancelled'), ('completed', 'Completed')], default='Basic', max_length=200, null=True),
        ),
    ]
