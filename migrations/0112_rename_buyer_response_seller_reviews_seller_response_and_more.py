# Generated by Django 4.0.8 on 2022-11-07 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0111_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller_reviews',
            old_name='buyer_response',
            new_name='seller_response',
        ),
        migrations.RemoveField(
            model_name='buyer_reviews',
            name='seller_response',
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 7, 11, 14, 54, 189833), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 7, 11, 14, 54, 189833), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 7, 11, 14, 54, 190834), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 7, 11, 14, 54, 189833), null=True),
        ),
    ]