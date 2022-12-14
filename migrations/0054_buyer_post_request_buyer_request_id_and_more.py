# Generated by Django 4.1.1 on 2022-10-16 19:05

import datetime
from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0053_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer_post_request',
            name='buyer_request_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456', blank=True, length=6, max_length=10, null=True, prefix=''),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 5, 18, 511445), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 5, 18, 511445), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 5, 18, 511445), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 16, 19, 5, 18, 511445), null=True),
        ),
    ]
