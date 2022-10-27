# Generated by Django 4.1.1 on 2022-10-08 00:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0022_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 8, 0, 38, 51, 115373), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 8, 0, 38, 51, 115373), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 8, 0, 38, 51, 116374), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 8, 0, 38, 51, 116374), null=True),
        ),
        migrations.CreateModel(
            name='UserGig_Extra_Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_type', models.CharField(blank=True, choices=[('basic', 'Basic'), ('standard', 'Standard'), ('enterprise', 'Enterprise')], max_length=200, null=True)),
                ('extra_price', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('delivery_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.parameter')),
                ('package_gig_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.usergigs')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gig Extra Delivery',
                'verbose_name_plural': 'Gig Extra Delivery',
            },
        ),
    ]
