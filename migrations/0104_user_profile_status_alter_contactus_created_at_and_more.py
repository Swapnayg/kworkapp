# Generated by Django 4.0.8 on 2022-11-05 18:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0103_user_transactions_flutter_fluw_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_status',
            field=models.CharField(blank=True, choices=[('active', 'ACTIVE'), ('warning', 'WARNING'), ('blocked', 'BLOCKED')], default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 18, 21, 55, 349778), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 18, 21, 55, 349778), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 18, 21, 55, 350779), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 5, 18, 21, 55, 349778), null=True),
        ),
        migrations.CreateModel(
            name='User_warning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('confirmed_status', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('confirmed_on', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Warning',
                'verbose_name_plural': 'User Warnings',
            },
        ),
        migrations.CreateModel(
            name='SpamDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detected_on', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('detected_word', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.chatwords')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Spam Detection',
                'verbose_name_plural': 'Spam Detections',
            },
        ),
    ]
