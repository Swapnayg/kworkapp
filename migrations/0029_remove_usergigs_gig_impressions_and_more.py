# Generated by Django 4.1.1 on 2022-10-10 05:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0028_remove_user_orders_id_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergigs',
            name='gig_impressions',
        ),
        migrations.AddField(
            model_name='user_orders',
            name='order_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 5, 47, 28, 431215), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 5, 47, 28, 431215), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 5, 47, 28, 431215), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 5, 47, 28, 431215), null=True),
        ),
        migrations.CreateModel(
            name='UserGigsImpressions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('impress_type', models.CharField(blank=True, choices=[('click', 'Click'), ('ad', 'Ad')], default='draft', max_length=200, null=True)),
                ('impress_date', models.DateTimeField(auto_now_add=True)),
                ('gig_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.usergigs')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gig Impression',
                'verbose_name_plural': 'Gig Impressions',
            },
        ),
    ]
