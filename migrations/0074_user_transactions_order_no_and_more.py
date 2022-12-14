# Generated by Django 4.0.8 on 2022-10-26 18:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0073_user_orders_order_amount_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_transactions',
            name='order_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.user_orders'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 18, 23, 36, 514015), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 18, 23, 36, 514015), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 18, 23, 36, 515015), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 18, 23, 36, 515015), null=True),
        ),
        migrations.AlterField(
            model_name='seller_reviews',
            name='order_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.user_orders'),
        ),
    ]
