# Generated by Django 4.1.1 on 2022-10-10 23:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0032_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 23, 1, 12, 717275), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 23, 1, 12, 717275), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 23, 1, 12, 717275), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 10, 23, 1, 12, 717275), null=True),
        ),
        migrations.CreateModel(
            name='Seller_Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('recommendation', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('service', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('review_message', models.TextField()),
                ('review_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('order_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.user_orders')),
                ('package_gig_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.usergigs')),
                ('s_review_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_review_from', to=settings.AUTH_USER_MODEL)),
                ('s_review_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_review_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Seller Review',
                'verbose_name_plural': 'Seller Reviews',
            },
        ),
        migrations.CreateModel(
            name='Buyer_Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_message', models.TextField()),
                ('review_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('order_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.user_orders')),
                ('package_gig_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.usergigs')),
                ('s_review_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='b_review_from', to=settings.AUTH_USER_MODEL)),
                ('s_review_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='b_review_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Buyer Review',
                'verbose_name_plural': 'Buyer Reviews',
            },
        ),
    ]
