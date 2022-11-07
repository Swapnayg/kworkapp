import datetime
from operator import truediv
from django.utils import timezone
import os
from django.forms import DateField
from django_countries.fields import CountryField
import shortuuid
from django.core.files import File
from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
import urllib
from shortuuid.django_fields import ShortUUIDField
from mainKwork import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from taggit.managers import TaggableManager


class MytypeField(models.Field):
    def db_type(self, connection):
        return 'timestamp'

class SellerLevels(models.Model):
    BOOL_CHOICES =[('level1', 'New or higher'),('level2', 'Advanced or higher'),('level3', 'Professional')]
    level_name =  models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="Basic",null=True)
    No_of_gigs = models.CharField(max_length=200,blank=True,default="0",null=True)
    No_of_offers = models.CharField(max_length=200,blank=True,default="0",null=True)
    
    class Meta:
        verbose_name = _("Seller Level")
        verbose_name_plural = _("Seller Levels")

    def __str__(self):
        return str(self.level_name)

class UserManager(BaseUserManager):
    def _create_user(self, email, username=None, is_admin=False, is_staff=False, is_active=True, password=None, country=None, avatar=None):
        'Method for actual creation of a user'
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin=is_admin,
            is_staff=is_staff,
            is_active=is_active,
            country=country,
            avatar=avatar
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, country=None, avatar=None):
        'Create a simple user'
        return self._create_user(email=email, username=username, password=password,country=country,avatar=avatar)

    def create_staffuser(self, email=None, username=None, password=None, country=None, avatar=None):
        'Create a staff user'
        return self._create_user(email=email, username=username, is_staff=True, password=password,country=country,avatar=avatar)

    def create_superuser(self, email=None, username=None, password=None, country=None, avatar=None):
        'Create a super user'
        return self._create_user(
            email=email, username=username, is_admin=True,
             is_staff=True, is_active=True, password=password,country=country,avatar=avatar
        )

class User(AbstractBaseUser):
    BOOL_CHOICES =[('Buyer', 'Buyer'),('Seller', 'Seller')]
    BOOL_CHOICES_STATUS =[('active', 'ACTIVE'),('warning', 'WARNING'),('blocked', 'BLOCKED')]
    BOOL_CHOICES_Levels =[('level1', 'New or higher'),('level2', 'Advanced or higher'),('level3', 'Professional')]
    email = models.EmailField(max_length=255, unique=True,default="",blank=True,null=True)
    username = models.CharField(max_length=150, unique=False,default="",blank=True,null=True)
    first_name = models.CharField(max_length=250,blank=True,default="",null=True)
    last_name = models.CharField(max_length=250,blank=True,default="",null=True)
    name =models.CharField(max_length=200,blank=True,default="",null=True)
    country =  CountryField(blank=True,default="",null=True)
    avatar = models.CharField(max_length=500, blank=True,default="",null=True)
    avg_respons = models.CharField(max_length=500, blank=True,default="1",null=True)
    last_delivery = models.CharField(max_length=500, blank=True,default="1",null=True)
    ordersin_progress = models.CharField(max_length=500, blank=True,default="0",null=True)
    avg_delivery_time = models.CharField(max_length=500, blank=True,default="Within 24 Hours",null=True)
    seller_level =  models.CharField(max_length=200,choices=BOOL_CHOICES_Levels,blank=True,default="level1",null=True)
    profile_type = models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="",null=True)
    profile_status = models.CharField(max_length=200,choices=BOOL_CHOICES_STATUS,blank=True,default="",null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    code = models.IntegerField(default=False)
    offers_left = models.IntegerField(default="0")
    is_staff = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    total_earning = models.CharField(max_length=200,blank=True,default="0",null=True)
    current_earning = models.CharField(max_length=200,blank=True,default="0",null=True)
    cancelled_earning = models.CharField(max_length=200,blank=True,default="0",null=True)
    avail_bal = models.CharField(max_length=200,blank=True,default="0",null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    affiliate_code= ShortUUIDField(length=6,max_length=6,alphabet="123456",blank=True,unique=True, editable=False, default=shortuuid.uuid,null=True)
    referrals_earnings =  models.IntegerField(blank=True,default="0",null=True)
    pay_pal_mail_id = models.EmailField(max_length=300, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        'Does the user have a specific permission?'
        return self.is_admin

    def has_module_perms(self, app_label):
        'Does the user have permissions to view the app `app_label`?'
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_all_permissions(user=None):
        if user.is_admin:
            return set()

    @property
    def has_staff_perm(self):
        'Is the user a member of staff?'
        return self.is_staff

    @property
    def has_active_perm(self):
        'Is the user active?'
        return self.is_active

    @property
    def has_admin_perm(self):
        'Is the user is super admin?'
        return self.is_admin

class Conversation(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="convo_starter")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="convo_participant")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")

    def __str__(self):
        return str(self.timestamp)
    
class ChatWords(models.Model):
    name =  models.CharField(max_length=200,blank=True,default="",null=True)
    slug =  models.CharField(max_length=200,blank=True,default="",null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Chat Word")
        verbose_name_plural = _("Chat Words")

    def __str__(self):
        return str(self.timestamp)

class Message(models.Model):
    BOOL_CHOICES_TYPES = [('chat', 'Chat Message'),('activity', 'Activity Message')]
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="message_receiver")
    text = models.CharField(max_length=1000,blank=True,null=True)
    attachment = models.CharField(max_length=500,blank=True,null=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    message_type = models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="",null=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return str(self.timestamp)



class PageEditor(models.Model):
    page_name = models.CharField(max_length=500)
    page_slug = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def edit_page_mode(self):
        return format_html(
        '<a class="btn" target="_blank" href="/admin/content_edit/{}/">Edit Contents</a>',
        self.page_slug,
    )
    class Meta:
        verbose_name = _("Page Editor")
        verbose_name_plural = _("Page Editor")

    def __str__(self):
        return self.page_slug



class supportTopic(models.Model):
    support_topic_Name = models.CharField(max_length=500)
    topic_category = models.CharField(max_length=500)
    slug = models.CharField(max_length=500,blank=True, null=True,unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Support Topic")
        verbose_name_plural = _("Support Topics")
        
    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        return super(supportTopic, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.slug

class supportMapping(models.Model):
    suport_topic = models.ForeignKey(supportTopic, on_delete=models.CASCADE,related_name="suport_topic")
    map_to =    models.ForeignKey(supportTopic, on_delete=models.CASCADE)   
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Support Mapping")
        verbose_name_plural = _("Support Mapping")

    def __str__(self):
        return str(self.timestamp)

class TopicDetails(models.Model):
    topic_Name = models.ForeignKey(supportTopic, on_delete=models.CASCADE,related_name="topic_Name",null=False,blank=False)
    topic_Desc =  models.TextField(blank=True,default="",null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Topic Details")
        verbose_name_plural = _("Topic Details")

    def __str__(self):
        return str(self.timestamp)


class Contactus(models.Model):
    BOOL_CHOICES =[('Received', 'Received'),('Contacted', 'Contacted'),]
    id = ShortUUIDField(length=6,max_length=6,alphabet="123456",primary_key=True,)
    email = models.EmailField(max_length=250, blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)
    status =  models.CharField(max_length=200,choices=BOOL_CHOICES,default='NA',)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return str(self.id)

class LearnTopics(models.Model):
    topic_names = models.CharField(max_length=1000, blank=True, null=True,unique=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Learning Topic")
        verbose_name_plural = _("Learning Topics")

    def __str__(self):
        return str(self.topic_names)

def servicefilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % ("Learning",filenm, ext)
    return os.path.join( 'learning/'+filename)

class LearningTopicDetails(models.Model):
    topic_Name = models.CharField(max_length=500, blank=True, null=True,unique=True)
    timeof_read_in_minute = models.CharField(max_length=200, blank=True, null=True)
    topic_description = models.CharField(max_length=1000, blank=True, null=True)
    image = models.FileField(upload_to = servicefilename ,max_length=255, null=True,blank=True)
    image_Text =  models.CharField(max_length=200, blank=True, null=True)
    video_url =  models.URLField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Learning Topic Detail")
        verbose_name_plural = _("Learning Topic Details")

    def __str__(self):
        return str(self.topic_Name)

class LearningTopicCounts(models.Model):
    topic_name = models.ForeignKey(LearningTopicDetails, on_delete=models.CASCADE,related_name="Learning_topic_Name",null=False,blank=False)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        verbose_name = _("Learning Topic Count")
        verbose_name_plural = _("Learning Topic Counts")

    def __str__(self):
        return str(self.topic_name)

def categoryfilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % (instance.category_Name.split()[0],filenm, ext)
    return os.path.join( 'category/'+filename)

def subcategoryfilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % (instance.sub_category_Name.split()[0],filenm, ext)
    return os.path.join( 'category/subcategory/'+filename)

class Categories(models.Model):
    image = models.FileField(upload_to = categoryfilename ,max_length=255, null=True,blank=True,help_text='Max width and height of the image will be 480:330')
    category_quote = models.CharField(max_length=800, blank=True, null=True)
    category_Name = models.CharField(max_length=500, blank=True, null=True)
    slug = models.CharField(max_length=300, blank=True, null=True)
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.category_Name)

class SubCategories(models.Model):
    category_Name = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="Category_Name",null=False,blank=False)
    sub_category_Name = models.CharField(max_length=500, blank=True, null=True)
    image = models.FileField(upload_to = subcategoryfilename ,max_length=255, null=True,blank=True,help_text='Max width and height of the image will be 480:330')
    slug = models.CharField(max_length=300, blank=True, null=True)
    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")

    def __str__(self):
        return str(self.sub_category_Name)


class SubSubCategories(models.Model):
    category_Name = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="MainCategory_Name",null=False,blank=False)
    sub_category_Name = models.ForeignKey(SubCategories, on_delete=models.CASCADE,related_name="SubCategory_Name",null=False,blank=False)
    sub_sub_category_Name = models.CharField(max_length=500, blank=True, null=True)
    slug = models.CharField(max_length=300, blank=True, null=True)
    tags = TaggableManager()

    def Tags(self):
        return ",".join([str(p) for p in self.tags.all()])

    class Meta:
        verbose_name = _("Main Menu")
        verbose_name_plural = _("Main Menus")

    def __str__(self):
        return str(self.sub_sub_category_Name)


class CharacterLimit(models.Model):
    Char_category_Name = models.CharField(max_length=500, blank=True, null=True)
    Hint_text = models.CharField(max_length=800, blank=True, null=True)
    Max_No_of_char_allowed = models.IntegerField( blank=True, null=True)

    class Meta:
        verbose_name = _("Character Limit")
        verbose_name_plural = _("Character Limits")

    def __str__(self):
        return str(self.Char_category_Name)


class UserProfileDetails(models.Model):
    main_category = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="main_category",null=True,blank=True)
    sub_category = models.ForeignKey(SubCategories, on_delete=models.CASCADE,related_name="sub_category",null=True,blank=True)
    profile_title = models.CharField(max_length=800, blank=True, null=True)
    profess_overview = models.CharField(max_length=1000, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profile")

    def __str__(self):
        return str(self.profile_title)

class Languages(models.Model):
    lng_Name = models.CharField(max_length=300, blank=True, null=True)
    lng_slug = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return str(self.lng_Name)

class UserLanguages(models.Model):
    BOOL_CHOICES =[('Basic', 'Basic'),('Fluent', 'Fluent'),('Conversational', 'Conversational')]
    language_name =  models.ForeignKey(Languages, on_delete=models.CASCADE,null=False,blank=False)
    lang_prof = models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="Basic",null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("User Language")
        verbose_name_plural = _("User Languages")

    def __str__(self):
        return str(self.language_name)



    
class Category_package_Details(models.Model):
    BOOL_CHOICES =[('number', 'Number'),('boolean', 'Boolean')]
    category_name = models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,null=False,blank=False)
    display_name = models.CharField(max_length=1000,blank=True,default="",null=True)
    helper_txt = models.CharField(max_length=1000,blank=True,default="",null=True)
    display_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    
    class Meta:
        verbose_name = _("Category Package")
        verbose_name_plural = _("Category Packages")

    def __str__(self):
        return str(self.display_name)

class Parameter(models.Model):
    BOOL_CHOICES =[('delivery_time', 'Delivery Time'),('extra_days', 'Extra Days'),('extra_time', 'Extra Time'),('no_revisions', 'No. of Revisions'),('res_days', 'Resolution Days')]
    parameter_name =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    parameter_value = models.CharField(max_length=1000,blank=True,default="",null=True)
    
    class Meta:
        verbose_name = _("Add On Gig Params")
        verbose_name_plural = _("Add On Gig Params")

    def __str__(self):
        return str(self.parameter_value)
    
class Category_package_Extra_Service(models.Model):
    BOOL_CHOICES =[('number', 'Number'),('extra_time', 'Extra Time'),('none', 'None')]
    category_name = models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,null=False,blank=False)
    display_name = models.CharField(max_length=1000,blank=True,default="",null=True)
    helper_txt = models.CharField(max_length=1000,blank=True,default="",null=True)
    display_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    
    class Meta:
        verbose_name = _("Category Extra Services")
        verbose_name_plural = _("Category Extra Services")

    def __str__(self):
        return str(self.display_name)


class UserGigs(models.Model):
    BOOL_CHOICES_STATUS =[('active', 'Active'),('pending', 'Pending'),('modification', 'Modification'),('draft', 'Draft'),('denied', 'Denied'),('paused', 'Paused')]
    gig_title =   models.CharField(max_length=1000,blank=True,default="",null=True)
    gig_category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True,blank=True)
    gig_sub_category = models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,null=True,blank=True)
    gig_description = models.TextField(blank=True,default="",null=True)
    gig_status =   models.CharField(max_length=200,choices=BOOL_CHOICES_STATUS,default="draft",blank=True,null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    
    class Meta:
        verbose_name = _("Gig Details")
        verbose_name_plural = _("Gig Details")

    def __str__(self):
        return str(self.gig_title)
    


class UserGigsImpressions(models.Model):
    BOOL_CHOICES =[('click', 'Click'),('ad', 'Ad')]
    ip_address = models.CharField(max_length=500,blank=True,default="",null=True)
    impress_type=  models.CharField(max_length=200,choices=BOOL_CHOICES,default="draft",blank=True,null=True)
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default="")
    impress_date =  models.DateTimeField(default=timezone.now, blank=True)
    
    class Meta:
        verbose_name = _("Gig Impression")
        verbose_name_plural = _("Gig Impressions")

    def __str__(self):
        return str(self.ip_address)

 
class UserGigsTags(models.Model):
    BOOL_CHOICES =[('Basic', 'Basic'),('Fluent', 'Fluent'),('Conversational', 'Conversational')]
    gig_tag_name = models.CharField(max_length=500,blank=True,default="",null=True)
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Tags")
        verbose_name_plural = _("Gig Tags")

    def __str__(self):
        return str(self.gig_tag_name)


class UserAvailable(models.Model):
    BOOL_CHOICES =[('vacation', "I'm going on vacation"),('overbooked', "I'm overbooked"),('other', 'Other')]
    available_from = models.CharField(max_length=500,blank=True,default="",null=True)
    available_to = models.CharField(max_length=500,blank=True,default="",null=True)
    available_mssg = models.TextField(max_length=1000,blank=True,default="",null=True)
    available_for_new =  models.BooleanField(default=False)
    available_types =  models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    
    class Meta:
        verbose_name = _("User Available")
        verbose_name_plural = _("User Available")

    def __str__(self):
        return str(self.available_from)
  
class UserSearchTerms(models.Model):
    BOOL_CHOICES =[('user', "user"),('keyword', "keyword")]
    search_words = models.CharField(max_length=1000,blank=True,default="",null=True)
    ip_address=  models.CharField(max_length=1000,blank=True,default="",null=True)
    search_types =  models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default="")
    
    class Meta:
        verbose_name = _("User Search Term")
        verbose_name_plural = _("User Search Terms")

    def __str__(self):
        return str(self.ip_address)
    
    
class UserGigPackages(models.Model):
    BOOL_CHOICES =[('basic', 'Basic'),('standard', 'Standard'),('enterprise', 'Enterprise')]
    package_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    package_title = models.CharField(max_length=500,blank=True,default="",null=True)
    package_description = models.TextField(blank=True,default="",null=True)
    package_delivery =  models.ForeignKey(Parameter, on_delete=models.CASCADE,related_name="package_delivery",null=False,blank=False)
    package_revisions =  models.ForeignKey(Parameter, on_delete=models.CASCADE,related_name="package_revisions",null=False,blank=False)
    package_data =  models.TextField(blank=True,default="",null=True)
    package_price = models.CharField(max_length=300,blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Packages")
        verbose_name_plural = _("Gig Packages")

    def __str__(self):
        return str(self.package_title)
    

class UserGig_Extra_Delivery(models.Model):
    BOOL_CHOICES =[('basic', 'Basic'),('standard', 'Standard'),('enterprise', 'Enterprise')]
    package_type =   models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,null=True)
    delivery_in = models.ForeignKey(Parameter, on_delete=models.CASCADE,null=False,blank=False)
    extra_price =  models.CharField(max_length=500,blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Extra Delivery")
        verbose_name_plural = _("Gig Extra Delivery")

    def __str__(self):
        return str(self.user_id)

 
class UserGigPackage_Extra(models.Model):
    package_data =  models.TextField(blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Package Extra")
        verbose_name_plural = _("Gig Package Extra")

    def __str__(self):
        return str(self.user_id)

class UserExtra_gigs(models.Model):
    extra_gig_title = models.CharField(max_length=500,blank=True,default="",null=True)
    extra_gig_description =  models.TextField(blank=True,default="",null=True)
    extra_gig_price = models.CharField(max_length=500,blank=True,default="",null=True)
    extra_gig_duration = models.ForeignKey(Parameter, on_delete=models.CASCADE,null=False,blank=False)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Extra Gig")
        verbose_name_plural = _("Extra Gigs")

    def __str__(self):
        return str(self.extra_gig_title)
    
    
class Usergig_faq(models.Model):
    gig_faq_question = models.CharField(max_length=800,blank=True,default="",null=True)
    gig_faq_answer =  models.TextField(blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Faq")
        verbose_name_plural = _("Gig Faqs")

    def __str__(self):
        return str(self.gig_faq_question)
    
class Usergig_image(models.Model):
    gig_image = models.CharField(max_length=800,blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Image")
        verbose_name_plural = _("Gig Images")

    def __str__(self):
        return str(self.gig_image)
    
    
class Usergig_requirement(models.Model):
    gig_req_question =  models.CharField(max_length=800,blank=True,default="",null=True)
    gig_req_ans_type =  models.CharField(max_length=800,blank=True,default="",null=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Requirement")
        verbose_name_plural = _("Gig Requirements")

    def __str__(self):
        return str(self.gig_req_question)
    
class Buyer_Post_Request(models.Model):
    BOOL_CHOICES =[('24hours', '24 Hours'),('3days', '3 Days'),('7days', '7 Days'),('other', 'Others')]
    BOOL_CHOICES_TYPES =[('individual', 'Individual'),('all', 'All')]
    BOOL_CHOICES_STATUS =[('active', 'Active'),('paused', 'Paused'),('pending', 'Pending'),('rejected', 'Rejected')]
    service_desc = models.TextField(blank=True,default="",null=True)
    service_images = models.TextField(blank=True,default="",null=True)
    buyer_request_id = ShortUUIDField(length=6,max_length=10,alphabet="123456",blank=True, editable=True, default=shortuuid.uuid,null=True)
    service_category =  models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="Post_Category_Name",null=False,blank=False)
    service_sub_category =  models.ForeignKey(SubSubCategories, on_delete=models.CASCADE,related_name="Post_SubCategory_Name",null=False,blank=False)
    service_time = models.CharField(max_length=300,choices=BOOL_CHOICES,blank=True,default="Basic",null=True)
    service_budget = models.CharField(max_length=300,blank=True,default="",null=True)
    service_date = models.DateTimeField(default=timezone.now, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    send_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="post_send_to",null=True,blank=True,default="")
    service_type = models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="all",null=True)
    service_status = models.CharField(max_length=300,choices=BOOL_CHOICES_STATUS,blank=True,default="pending",null=True)
    
    class Meta:
        verbose_name = _("Post Request")
        verbose_name_plural = _("Post Requests")

    def __str__(self):
        return str(self.user_id)
    
class Gig_favourites(models.Model):
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    class Meta:
        verbose_name = _("Gig Favourite")
        verbose_name_plural = _("Gig Favourites")

    def __str__(self):
        return str(self.gig_name)

class Referral_Users(models.Model):
    affiliate_code = models.CharField(max_length=300,blank=True,default="",null=True)
    ip_address =  models.CharField(max_length=300,blank=True,default="",null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="affiliate_user",null=False,blank=False)
    refferal_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="referral_user",null=True,blank=True,default="")
    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")

    def __str__(self):
        return str(self.affiliate_code)
    
class Request_Offers(models.Model):
    BOOL_CHOICES_TYPES =[('custom', 'Custom'),('request', 'Request')]
    BOOL_CHOICES_STATUS = [('active', 'Active'),('deleted', 'Removed')]
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    buyer_request = models.ForeignKey(Buyer_Post_Request, on_delete=models.CASCADE,null=False,blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    offer_desc =  models.TextField(blank=True,default="",null=True)
    offer_budget = models.CharField(max_length=300,blank=True,default="",null=True)
    offer_time = models.CharField(max_length=300,blank=True,default="",null=True)
    no_revisions = models.CharField(max_length=300,blank=True,default="",null=True)
    ask_requirements =  models.BooleanField(default=False)
    extra_parameters =  models.TextField(blank=True,default="",null=True)
    offer_type = models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="all",null=True)
    offer_date = models.DateTimeField(default=timezone.now, blank=True)
    offer_status_by_buyer = models.CharField(max_length=300,choices=BOOL_CHOICES_STATUS,blank=True,default="active",null=True)
    
    class Meta:
        verbose_name = _("Request Offer")
        verbose_name_plural = _("Request Offers")
        
    def __str__(self):
        return str(self.gig_name)  

class Payment_Parameters(models.Model):
    BOOL_CHOICES_TYPES =[('percent', 'Percentage'),('flat', 'Fixed Amount')]
    parameter_name =   models.CharField(max_length=200,blank=True,null=True)
    service_amount = models.CharField(max_length=500,blank=True,default="",null=True)
    service_fees = models.CharField(max_length=500,blank=True,default="",null=True)
    fees_type = models.CharField(max_length=500,choices=BOOL_CHOICES_TYPES,blank=True,default="",null=True)
    
    class Meta:
        verbose_name = _("Payment Parameter")
        verbose_name_plural = _("Payment Parameters")

    def __str__(self):
        return str(self.parameter_name)

class Addon_Parameters(models.Model):
    parameter_name =   models.CharField(max_length=200,blank=True,null=True)
    no_of_days = models.CharField(max_length=500,blank=True,default="",null=True)
    
    class Meta:
        verbose_name = _("Add On Parameter")
        verbose_name_plural = _("Add On Parameters")

    def __str__(self):
        return str(self.no_of_days)

class User_orders(models.Model):
    BOOL_CHOICES =[('active', 'Active'),('delivered', 'Delivered'),('cancel', 'Cancelled'),('completed', 'Completed')]
    order_no =  ShortUUIDField(length=6,max_length=6,alphabet="123456",primary_key=True,)
    order_status =  models.CharField(max_length=200,choices=BOOL_CHOICES,blank=True,default="Basic",null=True)
    order_amount =   models.CharField(max_length=200,blank=True,null=True)
    due_date =  models.DateTimeField(default=timezone.now, blank=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    order_date = models.DateTimeField(default=timezone.now, blank=True)
    offer_id = models.ForeignKey(Request_Offers, on_delete=models.CASCADE,null=True,blank=True)
    order_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="order_by",null=True,blank=True)
    order_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="order_to",null=True,blank=True)
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.order_no)

class User_orders_Extra_Gigs(models.Model):
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    gig_extra_package = models.ForeignKey(UserExtra_gigs, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Order Extra Offer")
        verbose_name_plural = _("Order Extra Offer")

    def __str__(self):
        return str(self.order_no)

class Seller_Reviews(models.Model):
    BOOL_CHOICES =[('active', 'Active'),('cancel', 'Cancelled'),('completed', 'Completed')]
    communication = models.CharField(max_length=200,blank=True,default="",null=True)
    recommendation = models.CharField(max_length=200,blank=True,default="",null=True)
    service = models.CharField(max_length=200,blank=True,default="",null=True)
    average_val = models.CharField(max_length=200,blank=True,default="",null=True)
    buyer_response = models.TextField(blank=True,default="",null=True)
    review_message = models.TextField(blank=True,default="",null=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    s_review_from = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False,related_name="s_review_from")
    s_review_to = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False, related_name="s_review_to")
    review_date = models.DateTimeField(default=timezone.now, blank=True)
    buyer_resp_date = models.DateTimeField(default=timezone.now, blank=True)
    
    class Meta:
        verbose_name = _("Seller Review")
        verbose_name_plural = _("Seller Reviews")

    def __str__(self):
        return str(self.recommendation)

class Buyer_Reviews(models.Model):
    BOOL_CHOICES =[('active', 'Active'),('cancel', 'Cancelled'),('completed', 'Completed')]
    review_message = models.TextField(blank=True,default="",null=True)
    seller_response = models.TextField(blank=True,default="",null=True)
    rating_val = models.CharField(max_length=200,blank=True,default="",null=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=False,blank=False)
    package_gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    b_review_from = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False,related_name="b_review_from")
    b_review_to = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False,related_name="b_review_to")
    review_date = models.DateTimeField(default=timezone.now, blank=True)
    seller_resp_date = models.DateTimeField(default=timezone.now, blank=True)
    
    class Meta:
        verbose_name = _("Buyer Review")
        verbose_name_plural = _("Buyer Reviews")

    def __str__(self):
        return str(self.review_message)
    
class Buyer_Requirements(models.Model):
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    requirement_ques = models.CharField(max_length=800,blank=True,default="",null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False)
    default_req = models.BooleanField(default=False)
    requirement_ans = models.TextField(blank=True,default="",null=True)
    req_documents = models.TextField(blank=True,default="",null=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Buyer Requirement")
        verbose_name_plural = _("Buyer Requirements")
        
    def __str__(self):
        return str(self.requirement_ques)


class User_Transactions(models.Model):
    BOOL_CHOICES_TYPES = [('paypal', 'Paypal'),('flutterwave', 'Flutterwave')]
    gig_name = models.ForeignKey(UserGigs, on_delete=models.CASCADE,null=False,blank=False)
    offer_id = models.ForeignKey(Request_Offers, on_delete=models.CASCADE,null=False,blank=False)
    payment_type = models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="",null=True)
    transaction_id = models.CharField(max_length=300,blank=True,default="",null=True)
    transaction_ref =models.CharField(max_length=300,blank=True,default="",null=True)
    payment_status = models.CharField(max_length=300,blank=True,default="",null=True)
    payment_currency = models.CharField(max_length=300,blank=True,default="",null=True)
    offer_amount = models.CharField(max_length=300,blank=True,default="",null=True)
    processing_fees = models.CharField(max_length=300,blank=True,default="",null=True)
    total_amount = models.CharField(max_length=300,blank=True,default="",null=True)
    paypal_id = models.CharField(max_length=500,blank=True,default="",null=True)
    paypal_email = models.CharField(max_length=500,blank=True,default="",null=True)
    flutter_account_id = models.CharField(max_length=500,blank=True,default="",null=True)
    flutter_app_fee = models.CharField(max_length=500,blank=True,default="",null=True)
    flutter_fluw_ref = models.CharField(max_length=1000,blank=True,default="",null=True)
    flutter_pay_type = models.CharField(max_length=500,blank=True,default="",null=True)
    transaction_date = models.DateTimeField(default=timezone.now, blank=True)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="paid_by",null=True,blank=True)
    paid_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="paid_to",null=True,blank=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        
    def __str__(self):
        return str(self.payment_type)

class User_Order_Activity(models.Model):
    order_message =  models.CharField(max_length=1000,blank=True,null=True)
    order_amount =   models.CharField(max_length=200,blank=True,null=True)
    activity_date = models.DateTimeField(default=timezone.now, blank=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Order Activity")
        verbose_name_plural = _("Order Activities")

    def __str__(self):
        return str(self.order_message)
    


class Order_Conversation(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_convo_starter")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_convo_participant")
    timestamp = models.DateTimeField(auto_now_add=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name = _("Order Conversation")
        verbose_name_plural = _("Order Conversations")

    def __str__(self):
        return str(self.timestamp)
    
    
class Order_Message(models.Model):
    BOOL_CHOICES_TYPES = [('chat', 'Chat Message'),('activity', 'Activity Message')]
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order_message_sender")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order_message_receiver")
    text =models.CharField(max_length=1000,blank=True,null=True)
    attachment = models.CharField(max_length=500,blank=True,null=True)
    conversation_id = models.ForeignKey(Order_Conversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    message_type = models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="",null=True)

    class Meta:
        verbose_name = _("Order Message")
        verbose_name_plural = _("Order Messages")

    def __str__(self):
        return str(self.timestamp)


class Message_Response_Time(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_recieved")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Message Response Analysis")
        verbose_name_plural = _("Message Response Analysys")

    def __str__(self):
        return str(self.timestamp)   
		
class UploadFile(models.Model):
    existingPath = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()
    
class User_Order_Resolution(models.Model):
    BOOL_CHOICES_TYPES = [('cancel', 'Cancel Order'),('extention', 'Extension Days'),('delivered', 'Delivered'),('completed', 'Completed')]
    BOOL_CHOICES_STATUS = [('accepted', 'Accepted'),('rejected', 'Rejected'),('pending', 'Pending')]
    resolution_type =  models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="",null=True)
    resolution_text =   models.CharField(max_length=500,blank=True,null=True)
    resolution_message =   models.CharField(max_length=200,blank=True,null=True)
    resolution_desc =   models.CharField(max_length=1000,blank=True,null=True)
    resolution_cancel_mssg =   models.CharField(max_length=1000,blank=True,null=True)
    resolution_days =   models.CharField(max_length=200,blank=True,null=True)
    resolution_last_date =   models.DateTimeField(default=timezone.now,null=True,blank=True)
    ext_prev_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    ext_new_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    resolution_date = models.DateTimeField(default=timezone.now, blank=True)
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="raised_by",null=True,blank=True)
    raised_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="raised_to",null=True,blank=True)
    resolution_status =  models.CharField(max_length=300,choices=BOOL_CHOICES_STATUS,blank=True,default="",null=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    message = models.ForeignKey(Order_Message, on_delete=models.CASCADE, related_name="message_contact",blank=True,default="",null=True)
    
    class Meta:
        verbose_name = _("Order Resolution Center")
        verbose_name_plural = _("Order Resolution Center")

    def __str__(self):
        return str(self.resolution_text)




class User_Refund(models.Model):
    refund_amount = models.CharField(max_length=500,blank=True,default="",null=True)
    refund_date = models.DateTimeField(default=timezone.now, blank=True)
    resolution =   models.ForeignKey(User_Order_Resolution, on_delete=models.CASCADE,null=True,blank=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Order Refund")
        verbose_name_plural = _("Order Refunds")

    def __str__(self):
        return str(self.refund_amount)

class User_Earnings(models.Model):
    BOOL_CHOICES_STATUS = [('cleared', 'Cleared'),('pending', 'Pending')]
    order_amount = models.CharField(max_length=500,blank=True,default="",null=True)
    earning_amount = models.CharField(max_length=500,blank=True,default="",null=True)
    platform_fees = models.CharField(max_length=500,blank=True,default="",null=True)
    aval_with = models.CharField(max_length=500,blank=True,default="",null=True)
    earning_date = models.DateTimeField(default=timezone.now, blank=True)
    resolution =   models.ForeignKey(User_Order_Resolution, on_delete=models.CASCADE,null=True,blank=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    clearence_date = models.DateTimeField(default=timezone.now, blank=True,null=True)
    clearence_status =  models.CharField(max_length=300,choices=BOOL_CHOICES_STATUS,blank=True,default="",null=True)
    cleared_on = models.DateTimeField(default=timezone.now, blank=True,null=True)
    
    class Meta:
        verbose_name = _("Order Earning")
        verbose_name_plural = _("Order Earnings")

    def __str__(self):
        return str(self.earning_amount)
    
    
    
class Api_keys(models.Model):
    BOOL_CHOICES_STATUS = [('google', 'Google'),('facebook', 'Facebook'),('paypal', 'Paypal'),('flutterwave', 'Flutterwave')]
    api_name =  models.CharField(max_length=300,choices=BOOL_CHOICES_STATUS,blank=True,default="",null=True, unique=True)
    secrete_key = models.CharField(max_length=1000,blank=True,default="",null=True)
    private_key = models.CharField(max_length=1000,blank=True,default="",null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=True)
    
    class Meta:
        verbose_name = _("Api Key")
        verbose_name_plural = _("Api Keys")

    def __str__(self):
        return str(self.api_name)

class SpamDetection(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    detected_word =  models.ForeignKey(ChatWords, on_delete=models.CASCADE,null=True,blank=True)
    detected_on = models.DateTimeField(default=timezone.now, blank=True)
    
    def block_button(self):
            return format_html('<a href="{}" class="link">Warn User</a>',
            reverse_lazy("admin:admin_block_scenario", args=[self.pk])
        )
            
    class Meta:
        verbose_name = _("Spam Detection")
        verbose_name_plural = _("Spam Detections")

    def __str__(self):
        return str(self.detected_word)
    
class User_warning(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    warning_date = models.DateTimeField(default=timezone.now, blank=True)
    confirmed_status =  models.BooleanField(default=False)
    confirmed_on = models.DateTimeField(default=timezone.now, blank=True)
    spamword =  models.ForeignKey(SpamDetection, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("User Warning")
        verbose_name_plural = _("User Warnings")

    def __str__(self):
        return str(self.warning_date)


class Order_Delivery(models.Model):
    BOOL_CHOICES_TYPES = [('delivered', 'Delivered'),('completed', 'Completed'),('draft', 'Draft')]
    delivery_message =models.CharField(max_length=1000,blank=True,null=True)
    attachment = models.CharField(max_length=1000,blank=True,null=True)
    delivery_date = models.DateTimeField(default=timezone.now, blank=True)
    order_no =   models.ForeignKey(User_orders, on_delete=models.CASCADE,null=True,blank=True)
    delivered_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="delivered_by",null=True,blank=True)
    delivered_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="delivered_to",null=True,blank=True)
    delivery_status = models.CharField(max_length=300,choices=BOOL_CHOICES_TYPES,blank=True,default="",null=True)
    resolution = models.ForeignKey(User_Order_Resolution, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name = _("Order Delivery")
        verbose_name_plural = _("Order Delivery")

    def __str__(self):
        return str(self.delivery_date)






