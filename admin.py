import json
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.dispatch import receiver
import whatismyip
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django_summernote.admin import SummernoteModelAdmin
from django.shortcuts import render
from kworkapp.models import Categories,UserGigPackages,Gig_favourites,User_orders_Extra_Gigs,Conversation,Conversation,Order_Message,Order_Conversation,Order_Delivery,Message_Response_Time,User_Order_Activity,User_Order_Resolution,User_Transactions,Payment_Parameters,Request_Offers,Referral_Users,UserGigPackage_Extra,Buyer_Post_Request,Seller_Reviews,Buyer_Reviews,UserGigsImpressions,User_orders,UserSearchTerms,UserGig_Extra_Delivery,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserAvailable,UserGigs,UserGigsTags, SellerLevels,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages,Withdrawal_Parameters,Buyer_Requirements, UserProfileDetails, supportMapping, supportTopic,Message
from mainKwork import settings
from django.core.files.base import ContentFile
from .forms import UserChangeForm, UserCreationForm
from django.urls import URLPattern, path,include
from django.contrib.auth.models import Group
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
import pycountry

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username','first_name','seller_level','last_name', 'name', 'is_admin', 'is_staff', 'is_active','avatar','country',"profile_type",'terms','affiliate_code','referrals_earnings','offers_left','current_earning')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username','seller_level', 'name', 'password','country',"profile_type",'terms',"avg_delivery_time","ordersin_progress",'offers_left',"avg_respons")}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2','country',"profile_type",'terms',"avg_delivery_time",'ordersin_progress','offers_left',"avg_respons")}
        ),
    )
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    filter_horizontal = ()
    
@receiver(post_save, sender=User)
def add_user(sender, **kwargs):
    if kwargs['created']: 
        if(kwargs.get('instance').is_admin == False):
            curr_user = User.objects.get(id=kwargs.get('instance').id)
            ip_address = str(whatismyip.whatismyip())   
            user_referral = Referral_Users.objects.get(ip_address=ip_address,refferal_user=None)
            user_referral.refferal_user = curr_user 
            user_referral.save() 

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

class AdminPageEditor(admin.ModelAdmin):
    list_display = ['page_name','page_slug','timestamp','edit_page_mode']
    #def has_add_permission(self, request, obj=None):
        #return False

    #def has_change_permission(self, request, obj=None):
        #return False

    #def has_delete_permission(self, request, obj=None):
        #return False

admin.site.register(PageEditor, AdminPageEditor)


class AdminSellerLevels(admin.ModelAdmin):
    list_display = ['level_name','No_of_gigs','No_of_offers']
    #def has_add_permission(self, request, obj=None):
        #return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(SellerLevels, AdminSellerLevels)

class AdminsupportTopic(admin.ModelAdmin):
    list_display = ['support_topic_Name','topic_category','timestamp']

admin.site.register(supportTopic, AdminsupportTopic)

class AdminsupportMapping(admin.ModelAdmin):
    list_display = ['suport_topic','map_to','timestamp']

admin.site.register(supportMapping, AdminsupportMapping)

class AdminContactus(admin.ModelAdmin):
    list_display = ['id','email','message','status','created_at','updated_at']

admin.site.register(Contactus, AdminContactus)

class AdminTopicDetails(SummernoteModelAdmin):
    list_display = ['topic_Name','topic_Desc','timestamp']
    summernote_fields = ('topic_Desc', )
    class Media:
        css = {'all': ('assets/css/frontend/topic_Details.css', )} 

admin.site.register(TopicDetails, AdminTopicDetails)

class AdminLearnTopics(admin.ModelAdmin):
    list_display = ['topic_names','created_at']

admin.site.register(LearnTopics, AdminLearnTopics)

class AdminCategory_package_Details(admin.ModelAdmin):
    list_display = ['category_name','helper_txt','display_name','display_type']

admin.site.register(Category_package_Details, AdminCategory_package_Details)

class AdminParameter(admin.ModelAdmin):
    list_display = ['parameter_name','parameter_value']

admin.site.register(Parameter, AdminParameter)


class AdminUser_orders(admin.ModelAdmin):
    list_display = ['order_no','order_status','package_gig_name','order_date','order_amount','due_date']

admin.site.register(User_orders, AdminUser_orders)


class AdminUser_Order_Activity(admin.ModelAdmin):
    list_display = ['order_message','order_amount','activity_date','order_no']

admin.site.register(User_Order_Activity, AdminUser_Order_Activity)


class AdminUser_Order_Resolution(admin.ModelAdmin):
    list_display = ['resolution_type','resolution_text','resolution_message','resolution_desc','resolution_personal_msg','resolution_days','resolution_date','resolution_status']

admin.site.register(User_Order_Resolution, AdminUser_Order_Resolution)


class AdminSeller_Reviews(admin.ModelAdmin):
    list_display = ['communication','recommendation','service','average_val','buyer_response','buyer_resp_date','review_message','order_no','package_gig_name','s_review_from','s_review_to','review_date']

admin.site.register(Seller_Reviews, AdminSeller_Reviews)


class AdminBuyer_Reviews(admin.ModelAdmin):
    list_display = ['review_message','order_no','package_gig_name','b_review_from','seller_response','seller_resp_date','rating_val','b_review_to','review_date']

admin.site.register(Buyer_Reviews, AdminBuyer_Reviews)

class AdminCategory_package_Extra_Service(admin.ModelAdmin):
    list_display = ['category_name','helper_txt','display_name','display_type']

admin.site.register(Category_package_Extra_Service, AdminCategory_package_Extra_Service)


class AdminGig_favourites(admin.ModelAdmin):
    list_display = ['gig_name','user_id']

admin.site.register(Gig_favourites, AdminGig_favourites)

class AdminLearningTopicDetails(admin.ModelAdmin):
    list_display = ['topic_Name','topic_description','image_Text']

admin.site.register(LearningTopicDetails, AdminLearningTopicDetails)

class AdminOrder_Conversation(admin.ModelAdmin):
    list_display = ['initiator','receiver','timestamp','order_no']

admin.site.register(Order_Conversation, AdminOrder_Conversation)

class AdminConversation(admin.ModelAdmin):
    list_display = ['initiator','receiver','timestamp']

admin.site.register(Conversation, AdminConversation)

class AdminMessage(admin.ModelAdmin):
    list_display = ['sender','receiver','text','attachment','conversation_id','timestamp','message_type']

admin.site.register(Message, AdminMessage)

class AdminMessage_Response_Time(admin.ModelAdmin):
    list_display = ['receiver','timestamp']

admin.site.register(Message_Response_Time, AdminMessage_Response_Time)


class AdminUser_orders_Extra_Gigs(admin.ModelAdmin):
    list_display = ['order_no','package_gig_name','gig_extra_package']

admin.site.register(User_orders_Extra_Gigs, AdminUser_orders_Extra_Gigs)


class AdminOrder_Delivery(admin.ModelAdmin):
    list_display = ['delivery_message','attachment','delivery_date','order_no','delivered_by','delivered_to','delivery_status']

admin.site.register(Order_Delivery, AdminOrder_Delivery)

class AdminOrder_Message(admin.ModelAdmin):
    list_display = ['sender','receiver','text','attachment','conversation_id','timestamp','order_no','message_type']

admin.site.register(Order_Message, AdminOrder_Message)


class AdminLearningTopicCounts(admin.ModelAdmin):
    list_display = ['topic_name','ip_address']

admin.site.register(LearningTopicCounts, AdminLearningTopicCounts)

class AdminCategories(admin.ModelAdmin):
    list_display = ['category_Name','image','slug','category_quote']

admin.site.register(Categories, AdminCategories)

class AdminSubCategories(admin.ModelAdmin):
    list_display = ['category_Name','sub_category_Name','image','slug']

admin.site.register(SubCategories, AdminSubCategories)

class AdminSubSubCategories(admin.ModelAdmin):
    list_display = ['category_Name','sub_category_Name','sub_sub_category_Name','slug','Tags']
    
    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','assets/js/sub_sub_category.js')

admin.site.register(SubSubCategories, AdminSubSubCategories)


class AdminCharacterLimit(admin.ModelAdmin):
    list_display = ['Char_category_Name','Hint_text','Max_No_of_char_allowed']
    #readonly_fields = ['Char_category_Name']

admin.site.register(CharacterLimit, AdminCharacterLimit)


class AdminUserProfileDetails(admin.ModelAdmin):
    list_display = ['main_category','sub_category','profile_title','profess_overview','user_id']
    class Media:
        css = {'all': ('assets/css/frontend/admin_post_request.css', )} 
    
    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','assets/js/sub_sub_category1.js')
        
admin.site.register(UserProfileDetails, AdminUserProfileDetails)

class AdminLanguages(admin.ModelAdmin):
    list_display = ['lng_Name','lng_slug']

admin.site.register(Languages, AdminLanguages)

class AdminUserLanguages(admin.ModelAdmin):
    list_display = ['language_name','lang_prof','user_id']

admin.site.register(UserLanguages, AdminUserLanguages)

class AdminUserSearchTerms(admin.ModelAdmin):
    list_display = ['search_words','ip_address','search_types','user_id']

admin.site.register(UserSearchTerms, AdminUserSearchTerms)


class AdminUserGigs(admin.ModelAdmin):
    list_display = ['gig_title','gig_category','gig_sub_category','gig_description','gig_status','user_id']
    class Media:
        css = {'all': ('assets/css/frontend/admin_post_request.css', )} 

admin.site.register(UserGigs, AdminUserGigs)


class AdminUserGigsImpressions(admin.ModelAdmin):
    list_display = ['ip_address','impress_type','gig_name','user_id','impress_date']

admin.site.register(UserGigsImpressions, AdminUserGigsImpressions)


class AdminUserAvailable(admin.ModelAdmin):
    list_display = ['available_from','available_to','available_mssg','available_for_new','available_types','user_id']

admin.site.register(UserAvailable, AdminUserAvailable)


class AdminBuyer_Post_Request(admin.ModelAdmin):
    list_display = ['service_desc','service_images','service_category','send_to','service_type','buyer_request_id','service_sub_category','service_time','service_budget','service_date','user_id','service_status']
    class Media:
        css = {'all': ('assets/css/frontend/admin_post_request.css', )} 

admin.site.register(Buyer_Post_Request, AdminBuyer_Post_Request)


class AdminUserPackageGig(admin.ModelAdmin):
    list_display = ['package_type','package_title','package_description','package_delivery','package_revisions','package_data','package_price','package_gig_name','user_id']

admin.site.register(UserGigPackages, AdminUserPackageGig)

class AdminUserGigPackage_Extra(admin.ModelAdmin):
    list_display = ['package_data','package_gig_name','user_id']

admin.site.register(UserGigPackage_Extra, AdminUserGigPackage_Extra)

class AdminBuyer_Requirements(admin.ModelAdmin):
    list_display = ['gig_name','requirement_ques','user_id','default_req','requirement_ans','req_documents','order_no']

admin.site.register(Buyer_Requirements, AdminBuyer_Requirements)


class AdminRequest_Offers(admin.ModelAdmin):
    list_display = ['gig_name','buyer_request','user_id','offer_desc','offer_budget','offer_time','no_revisions','ask_requirements','extra_parameters','offer_type','offer_date','offer_status_by_buyer']
    class Media:
        css = {'all': ('assets/css/frontend/admin_post_request.css', )}
admin.site.register(Request_Offers, AdminRequest_Offers)


class AdminUserGig_Extra_Delivery(admin.ModelAdmin):
    list_display = ['package_type','delivery_in','extra_price','package_gig_name','user_id']

admin.site.register(UserGig_Extra_Delivery, AdminUserGig_Extra_Delivery)


class AdminUserExtra_gigs(admin.ModelAdmin):
    list_display = ['extra_gig_title','extra_gig_description','extra_gig_price','extra_gig_duration','package_gig_name','user_id']

admin.site.register(UserExtra_gigs, AdminUserExtra_gigs)


class AdminUsergig_faq(admin.ModelAdmin):
    list_display = ['gig_faq_question','gig_faq_answer','package_gig_name','user_id']

admin.site.register(Usergig_faq, AdminUsergig_faq)

class AdminUsergig_image(admin.ModelAdmin):
    list_display = ['gig_image','package_gig_name','user_id']

admin.site.register(Usergig_image, AdminUsergig_image)


class AdminUsergig_requirement(admin.ModelAdmin):
    list_display = ['gig_req_question','gig_req_ans_type','package_gig_name','user_id']

admin.site.register(Usergig_requirement, AdminUsergig_requirement)


class AdminUserGigsTags(admin.ModelAdmin):
    list_display = ['gig_tag_name','gig_name','user_id']

admin.site.register(UserGigsTags, AdminUserGigsTags)



class AdminReferral_Users(admin.ModelAdmin):
    list_display = ['affiliate_code','ip_address','user_id','refferal_user']

admin.site.register(Referral_Users, AdminReferral_Users)


class AdminWithdrawal_Parameters(admin.ModelAdmin):
    list_display = ['parameter_name','no_of_days']

admin.site.register(Withdrawal_Parameters, AdminWithdrawal_Parameters)


class AdminUser_Transactions(admin.ModelAdmin):
    list_display = ['gig_name','offer_id','payment_type','transaction_id','payment_status','paypal_id','paypal_email','flutter_account_id','order_no']

admin.site.register(User_Transactions, AdminUser_Transactions)


class AdminPayment_Parameters(admin.ModelAdmin):
    list_display = ['parameter_name','service_amount','service_fees','fees_type']

admin.site.register(Payment_Parameters, AdminPayment_Parameters)

def get_admin_urls(urls):
    def get_urls():
        my_urls =  [
           path('content_edit/<str:Id>/', content_editView,name='content_edit'), 
        ]
        return my_urls + urls
    return get_urls

admin.autodiscover()

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls

def content_editView(request,Id=''):
    print(Id+ ".html")
    return render(request , 'contents.html',{'templateName':Id+ ".html"})

