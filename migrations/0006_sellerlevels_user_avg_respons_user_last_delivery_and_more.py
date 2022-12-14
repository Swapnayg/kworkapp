# Generated by Django 4.1.1 on 2022-10-01 13:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0005_alter_contactus_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerLevels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(blank=True, choices=[('level1', 'Level One'), ('level2', 'Level Two'), ('top_rated', 'Top Rated Seller')], default='Basic', max_length=200, null=True)),
                ('No_of_gigs', models.CharField(blank=True, default='0', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Seller Level',
                'verbose_name_plural': 'Seller Levels',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='avg_respons',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_delivery',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 1, 13, 13, 21, 351805), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 1, 13, 13, 21, 351805), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 1, 13, 13, 21, 352806), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 1, 13, 13, 21, 352806), null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], default='Basic', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='seller_level',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='kworkapp.sellerlevels'),
        ),
    ]
