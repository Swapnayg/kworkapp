# Generated by Django 4.0.8 on 2022-10-20 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0061_request_offers_offer_status_by_buyer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Parameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_name', models.CharField(blank=True, max_length=200, null=True)),
                ('service_amount', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('service_fees', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('fees_type', models.CharField(blank=True, choices=[('percent', 'Percentage'), ('flat', 'Fixed Amount')], default='', max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Payment Parameter',
                'verbose_name_plural': 'Payment Parameters',
            },
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 13, 25, 36, 477621), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 13, 25, 36, 477621), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 13, 25, 36, 477621), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 13, 25, 36, 477621), null=True),
        ),
    ]
