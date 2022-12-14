# Generated by Django 4.1.1 on 2022-10-23 17:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0041_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer_post_request',
            name='service_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Post_SubCategory_Name', to='kworkapp.subsubcategories'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 17, 5, 48, 295915), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 17, 5, 48, 295915), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 17, 5, 48, 296915), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 17, 5, 48, 295915), null=True),
        ),
    ]
