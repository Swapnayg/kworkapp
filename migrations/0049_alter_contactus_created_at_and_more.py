# Generated by Django 4.1.1 on 2022-10-15 15:21

import datetime
from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0048_remove_user_referrals_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 15, 21, 37, 742394), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 15, 21, 37, 742394), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 15, 21, 37, 744395), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 15, 21, 37, 743394), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='affiliate_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456', blank=True, editable=False, length=6, max_length=6, null=True, prefix='', unique=True),
        ),
    ]
