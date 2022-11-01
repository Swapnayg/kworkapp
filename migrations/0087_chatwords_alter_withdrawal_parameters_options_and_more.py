# Generated by Django 4.0.8 on 2022-10-31 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kworkapp', '0086_remove_order_conversation_conversation_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('slug', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Chat Word',
                'verbose_name_plural': 'Chat Words',
            },
        ),
        migrations.AlterModelOptions(
            name='withdrawal_parameters',
            options={'verbose_name': 'Parameter', 'verbose_name_plural': 'Parameters'},
        ),
        migrations.AddField(
            model_name='user',
            name='pay_pal_mail_id',
            field=models.EmailField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 31, 11, 31, 29, 826732), null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 31, 11, 31, 29, 826732), null=True),
        ),
        migrations.AlterField(
            model_name='learningtopicdetails',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 31, 11, 31, 29, 827788), null=True),
        ),
        migrations.AlterField(
            model_name='learntopics',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 31, 11, 31, 29, 826732), null=True),
        ),
    ]