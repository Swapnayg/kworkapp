# Generated by Django 4.1.1 on 2022-10-23 13:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0038_remove_useravailable_gig_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 13, 20, 2, 425497), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 13, 20, 2, 425497), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 13, 20, 2, 426497), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 23, 13, 20, 2, 426497), null=True),
        ),
        migrations.CreateModel(
            name='Buyer_Post_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_desc', models.TextField()),
                ('service_images', models.TextField()),
                ('service_time', models.CharField(blank=True, choices=[('24hours', '24 Hours'), ('3days', '3 Days'), ('7days', '7 Days'), ('other', 'Others')], default='Basic', max_length=300, null=True)),
                ('service_budget', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('service_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Post_Category_Name', to='kworkapp.categories')),
                ('service_sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Post_SubCategory_Name', to='kworkapp.subcategories')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post Request',
                'verbose_name_plural': 'Post Requests',
            },
        ),
    ]
