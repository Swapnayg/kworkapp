# Generated by Django 4.0.8 on 2022-12-14 22:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0220_user_orders_extra_gigs_gig_extra_delivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer_post_request',
            name='service_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Post_SubCategory_Name', to='kworkapp.subcategories'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 14, 22, 43, 25, 166610), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 14, 22, 43, 25, 166610), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 14, 22, 43, 25, 168608), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 14, 22, 43, 25, 167612), null=True),
        ),
    ]