# Generated by Django 4.0.8 on 2022-11-03 22:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0090_uploadfile_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_message',
            name='resolution',
        ),
        migrations.AddField(
            model_name='user_order_resolution',
            name='message',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_contact', to='kworkapp.order_message'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 3, 22, 26, 47, 15010), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 3, 22, 26, 47, 15010), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 3, 22, 26, 47, 15010), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 3, 22, 26, 47, 15010), null=True),
        ),
    ]
