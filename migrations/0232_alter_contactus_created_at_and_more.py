# Generated by Django 4.0.8 on 2022-12-23 12:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0231_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 23, 12, 16, 0, 681085), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 23, 12, 16, 0, 681085), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 23, 12, 16, 0, 681085), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 23, 12, 16, 0, 681085), null=True),
        ),
        migrations.CreateModel(
            name='AdminLogging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('mail_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('log_type', models.CharField(blank=True, choices=[('gig_creation', 'Gig Creation'), ('request_post', 'Buyer Request'), ('withdrawal', 'Withdrawal'), ('support', 'Support')], default='', max_length=300, null=True)),
                ('rejection_message', models.TextField(blank=True, default='', null=True)),
                ('log_status', models.CharField(blank=True, choices=[('approve', 'Approved'), ('rejected', 'Rejected'), ('close', 'Close Ticket')], default='', max_length=300, null=True)),
                ('log_created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('gig_Details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.usergigs')),
            ],
            options={
                'verbose_name': 'Logging',
                'verbose_name_plural': 'Logging',
            },
        ),
    ]
