# Generated by Django 4.1.1 on 2022-10-15 12:53

import datetime
from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0046_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='affiliate_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456', blank=True, length=6, max_length=6, null=True, prefix=''),
        ),
        migrations.AddField(
            model_name='user',
            name='referrals',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='referrals_earnings',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='characterlimit',
            name='Max_No_of_char_allowed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 12, 53, 9, 323657), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 12, 53, 9, 323657), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 12, 53, 9, 325659), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 12, 53, 9, 324658), null=True),
        ),
    ]
