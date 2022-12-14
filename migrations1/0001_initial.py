# Generated by Django 3.2.13 on 2022-09-14 15:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import kworkapp.models
import shortuuid.django_fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('name', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, default='', max_length=2, null=True)),
                ('avatar', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('profile_type', models.CharField(blank=True, choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], default='', max_length=10, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('code', models.IntegerField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, help_text='Max width and height of the image will be 480:330', max_length=255, null=True, upload_to=kworkapp.models.categoryfilename)),
                ('category_quote', models.CharField(blank=True, max_length=800, null=True)),
                ('category_Name', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Contactus',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='123456', length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('message', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Contacted', 'Contacted')], default='NA', max_length=200)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 14, 15, 36, 34, 931334), null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 14, 15, 36, 34, 931334), null=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_starter', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_participant', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
            },
        ),
        migrations.CreateModel(
            name='LearningTopicDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_Name', models.CharField(blank=True, max_length=500, null=True, unique=True)),
                ('timeof_read_in_minute', models.CharField(blank=True, max_length=200, null=True)),
                ('topic_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('image', models.FileField(blank=True, max_length=255, null=True, upload_to=kworkapp.models.servicefilename)),
                ('image_Text', models.CharField(blank=True, max_length=200, null=True)),
                ('video_url', models.URLField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 14, 15, 36, 34, 932334), null=True)),
            ],
            options={
                'verbose_name': 'Learning Topic Detail',
                'verbose_name_plural': 'Learning Topic Details',
            },
        ),
        migrations.CreateModel(
            name='LearnTopics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_names', models.CharField(blank=True, max_length=1000, null=True, unique=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 14, 15, 36, 34, 932334), null=True)),
            ],
            options={
                'verbose_name': 'Learning Topic',
                'verbose_name_plural': 'Learning Topics',
            },
        ),
        migrations.CreateModel(
            name='PageEditor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=500)),
                ('page_slug', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Page Editor',
                'verbose_name_plural': 'Page Editor',
            },
        ),
        migrations.CreateModel(
            name='SubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_Name', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.FileField(blank=True, help_text='Max width and height of the image will be 480:330', max_length=255, null=True, upload_to=kworkapp.models.subcategoryfilename)),
                ('slug', models.CharField(blank=True, max_length=300, null=True)),
                ('category_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Category_Name', to='kworkapp.categories')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
            },
        ),
        migrations.CreateModel(
            name='supportTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_topic_Name', models.CharField(max_length=500)),
                ('topic_category', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Support Topic',
                'verbose_name_plural': 'Support Topics',
            },
        ),
        migrations.CreateModel(
            name='TopicDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_Desc', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('topic_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_Name', to='kworkapp.supporttopic')),
            ],
            options={
                'verbose_name': 'Topic Details',
                'verbose_name_plural': 'Topic Details',
            },
        ),
        migrations.CreateModel(
            name='supportMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('map_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.supporttopic')),
                ('suport_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suport_topic', to='kworkapp.supporttopic')),
            ],
            options={
                'verbose_name': 'Support Mapping',
                'verbose_name_plural': 'Support Mapping',
            },
        ),
        migrations.CreateModel(
            name='SubSubCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_sub_category_Name', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=300, null=True)),
                ('category_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MainCategory_Name', to='kworkapp.categories')),
                ('sub_category_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SubCategory_Name', to='kworkapp.subcategories')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Main Menu',
                'verbose_name_plural': 'Main Menus',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('attachment', models.ImageField(blank=True, upload_to='')),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kworkapp.conversation')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='LearningTopicCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=200, null=True)),
                ('topic_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Learning_topic_Name', to='kworkapp.learningtopicdetails')),
            ],
            options={
                'verbose_name': 'Learning Topic Count',
                'verbose_name_plural': 'Learning Topic Counts',
            },
        ),
    ]
