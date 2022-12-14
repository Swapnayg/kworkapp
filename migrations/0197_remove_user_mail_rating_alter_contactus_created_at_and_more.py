# Generated by Django 4.0.8 on 2022-11-28 18:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0196_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mail_rating',
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 28, 18, 57, 15, 592536), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 28, 18, 57, 15, 592536), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 28, 18, 57, 15, 592536), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 28, 18, 57, 15, 592536), null=True),
        ),
        migrations.AlterField(
            model_name='smtp_settings',
            name='mail_port',
            field=models.CharField(blank=True, choices=[('587', '587'), ('465', '465')], default='587', max_length=300, null=True),
        ),
    ]
