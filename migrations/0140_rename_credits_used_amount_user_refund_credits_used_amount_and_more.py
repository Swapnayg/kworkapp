# Generated by Django 4.0.8 on 2022-11-09 16:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0139_user_earnings_credit_used_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='credits_used_amount',
            new_name='refund_credits_used_amount',
        ),
        migrations.AddField(
            model_name='user',
            name='with_credits_used_amount',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 9, 16, 25, 43, 229734), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 9, 16, 25, 43, 229734), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 9, 16, 25, 43, 229734), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 9, 16, 25, 43, 229734), null=True),
        ),
    ]
