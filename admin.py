import json
from django.contrib import admin
from email.mime.multipart import MIMEMultipart
from social.apps.django_app.default.models import UserSocialAuth
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import AdminSite
from django.dispatch import receiver
from django_summernote.models import Attachment
from kworkapp.mail_templates import MailTemplates
from taggit.admin import Tag
from django.db.models import Q
#from django.contrib.sites.models import Site
from django.shortcuts import redirect, render
from import_export import fields, resources
from taggit.managers import TaggableManager
from import_export.widgets import ForeignKeyWidget
from import_export.signals import post_import, post_export
from import_export.widgets import Widget
from import_export.formats import base_formats
from import_export import resources
from import_export import fields, resources, widgets
from datetime import datetime, timedelta,date
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin,ExportActionModelAdmin, ImportExportModelAdmin, ImportMixin
import whatismyip
from django.views import View
from django.db.models.signals import post_save,pre_delete,post_delete
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django_summernote.admin import SummernoteModelAdmin
from django.shortcuts import render
from kworkapp.models import Categories,UserGigPackages,SMTP_settings,SellerLevels4,LogoImages,CustomNotifications,UploadFile,Withdrwal_initiated,Notification_commands,Api_keys,SpamDetection,User_warning,User_Refund,User_Earnings,ChatWords,Gig_favourites,User_orders_Extra_Gigs,Conversation,Conversation,Order_Message,Order_Conversation,Order_Delivery,Message_Response_Time,User_Order_Activity,User_Order_Resolution,User_Transactions,Payment_Parameters,Request_Offers,Referral_Users,UserGigPackage_Extra,Buyer_Post_Request,Seller_Reviews,Buyer_Reviews,UserGigsImpressions,User_orders,UserSearchTerms,UserGig_Extra_Delivery,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserAvailable,UserGigs,UserGigsTags,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages,Addon_Parameters,Buyer_Requirements, UserProfileDetails, supportMapping, supportTopic,Message
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
from django.template.response import TemplateResponse

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username','first_name','user_level','last_name', 'name', 'is_admin', 'is_staff', 'is_active','avatar','country',"profile_type",'terms','profile_status','affiliate_code','referrals_earnings','offers_left','current_earning','pay_pal_mail_id','mail_message','mail_order','mail_updates','unblocked_count')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    readonly_fields = ['unblocked_count']
    fieldsets = (
        (None, {'fields': ('email', 'username','user_level', 'name', 'password','country',"profile_type",'terms',"avg_delivery_time","ordersin_progress",'offers_left',"avg_respons",'profile_status','unblocked_count')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2','country',"profile_type",'terms',"avg_delivery_time",'ordersin_progress','offers_left',"avg_respons",'profile_status','unblocked_count')}
        ),
    )
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    filter_horizontal = ()
    
@receiver(pre_delete, sender=User)
def model_post_delete(sender, instance, **kwargs):
    if(instance.id is None):
        pass
    else:
        userobj = User.objects.get(email = instance.email)
        UserSocialAuth.objects.filter(user=userobj).delete()
        
@receiver(pre_save, sender=User)
def update_blocked_status(sender, instance, **kwargs):
    if(instance.pk is None):
        pass
    else:
        previous_val = User.objects.get(pk = instance.pk)
        prev_unblock_val =  int(str(previous_val.unblocked_count))
        previous_status =  str(previous_val.profile_status)
        if(previous_status == "blocked"):
            if(instance.profile_status == "active"):
                User_warning.objects.filter(user_id=previous_val).delete()
                SpamDetection.objects.filter(user_id=previous_val).delete()
                instance.unblocked_count = str(int(prev_unblock_val) + 1) 

def get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    # Retrieve the original list
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models customably within each app.
    for app in app_list:
        if app['app_label'] == 'kworkapp':
            ordering = {
                'Users': 1,
                'Page Editor': 2,
                'User_Earnings': 3,
                'User_Refund': 4,
                'Seller Levels':5,
                'Support Topics':6,
                'Support Mapping':7,
                'Contacts':8,
                'Topic Details':9,
                'Learning Topics':10,
                'Category Packages':11,
                'Add On Gig Params':12,
                'Orders':13,
                'Order Activities':14,
                'Chat Words':15,
                'Upload files':16,
                'Order Refunds':17,
                'Order Earnings':18,
                'Order Resolution Center':19,
                'Seller Reviews':20,
                'Buyer Reviews':21,
                'Category Extra Services':22,
                'Gig Favourites':23,
                'User Warnings':24,
                'Spam Detections ':25,
                'Learning Topic Details':26,
                'Order Conversations':27,
                'Conversations':28,
                'Messages':29,
                'Message Interval':30,
                'Order Extra Offer':31,
                'Order Delivery':32,
                'Order Messages':33,
                'Learning Topic Counts':34,
                'Categories':35,
                'Sub Categories':36,
                'Main Menus':37,
                'Character Limits':38,
                'User Profile':39,
                'Languages':40,
                'User Languages':41,
                'User Search Terms':42,
                'Gig Details':43,
                'Gig Impressions':44,
                'User Available':45,
                'Post Requests':46,
                'Gig Packages':47,
                'Gig Package Extra':48,
                'Buyer Requirements':49,
                'Request Offers':50,
                'Gig Extra Delivery':51,
                'Extra Gigs':51,
                'Gig Faqs':52,
                'Gig Images':53,
                'Gig Requirements':54,
                'Gig Tags':55,
                'Referrals':56,
                'Api Keys':57,
                'Add On Parameters':58,
                'Transactions':60,
                'Payment Parameters':59,
                'Withdrawals':60,
                'Notification Settings':61,
                'Notifications':62,
                'Logo':63,
                'SMTP Settings':64,
            }
            app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = get_app_list

@receiver(post_save, sender=User)
def add_user(sender, **kwargs):
    if kwargs['created']: 
        if(kwargs.get('instance').is_admin == False):
            curr_user = User.objects.get(id=kwargs.get('instance').id)
            ip_address = str(whatismyip.whatismyip())
            try:               
                user_referral = Referral_Users.objects.get(ip_address=ip_address,refferal_user=None)
                user_referral.refferal_user = curr_user 
                user_referral.save()
            except:
                pass

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.unregister(Attachment)
admin.site.unregister(Tag)
#admin.site.unregister(Site)

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
    list_display = ['level_name','level_slug','No_of_gigs','No_of_offers','level_badge','up_order_amount','up_order_count','record_check']
# #     #def has_add_permission(self, request, obj=None):
# #         #return False

# #     # def has_change_permission(self, request, obj=None):
# #     #     return False

# #     # def has_delete_permission(self, request, obj=None):
# #     #     return False

admin.site.register(SellerLevels4, AdminSellerLevels)

class AdminsupportTopic(admin.ModelAdmin):
    list_display = ['support_topic_Name','topic_category','timestamp','slug']

admin.site.register(supportTopic, AdminsupportTopic)

class AdminWithdrwal_initiated(admin.ModelAdmin):
    list_display = ['withdrawal_amount','withdrawal_message','initiated_date','user_id','withdrawan_status','withdrawn_date']
    readonly_fields = ['withdrawal_amount','initiated_date','user_id','withdrawn_date']
    
admin.site.register(Withdrwal_initiated, AdminWithdrwal_initiated)


@receiver(pre_save, sender=Withdrwal_initiated)
def update_pay_status(sender, instance, **kwargs):
    if(instance.id is None):
        pass
    else:
        if(instance.withdrawan_status == "sucess"):
            userDetails = User.objects.get(username = instance.user_id.username)
            user_earnings = User_Earnings.objects.filter(user_id=userDetails, clearence_status="cleared")
            for earn in user_earnings:
                if(earn.aval_with != None):
                    if(round(float(earn.aval_with),2) != 0.00):
                        if(earn.withdrawn_amount == None):
                            with_draw_amount = round(float(earn.aval_with),2)
                            earn.withdrawn_amount = round(float(earn.aval_with),2)
                            earn.aval_with = 0.00
                            earn.withdrawn_status = True
                            earn.withdrawn_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            earn.clearence_status = "completed"
                            earn.save()
                            order_details = User_orders.objects.get(pk = earn.order_no.pk)
                            order_by = User.objects.get(pk = order_details.order_by.pk)
                            order_to = User.objects.get(pk = order_details.order_to.pk)
                            order_ativity1 = User_Order_Activity(order_message = "Withdrawal Completed !",order_amount = with_draw_amount, order_no=order_details,activity_type="withdrawal",activity_by=order_by,activity_to=order_to)
                            order_ativity1.save()


@receiver(post_save, sender=Withdrwal_initiated)
def update_trasactions_status(sender, instance, **kwargs):
    if(instance.id is None):
        pass
    else:
        previous = Withdrwal_initiated.objects.get(id=instance.id)
        if(previous.withdrawan_status == "sucess"):
            senderObj = User.objects.get(username = 'admin')
            receiverObj =  User.objects.get(username = gig_details.user_id.username)
            notification_settings = Notification_commands.objects.get(slug = "payment_sucessful")
            if(notification_settings.is_active == True):
                noti_create = CustomNotifications(sender = senderObj, recipient=receiverObj, verb='withdrawal',description="Your Withdrawal of "+ str(previous.withdrawal_amount) + " is sucessful.")
                noti_create.save()
            userDetails = User.objects.get(username = instance.user_id.username)
            update_all_balancevalues(userDetails)
                            

def update_all_balancevalues(username):
    userDetails = User.objects.get(username = username)
    total_earning_val = 0
    current_earning_val = 0
    cancelled_earning_val = 0
    avail_bal_val = 0
    availcredit_bal_val = 0
    affilite_earn_val = 0
    withdrawed_credit_val = 0
    with_used_credit_val = 0
    ref_used_credit_val = 0
    total_earnng = User_Earnings.objects.filter(user_id=userDetails) 
    for earn in total_earnng:
        if(earn.earning_type == "cancelled"):
            cancelled_earning_val = round(float(float(cancelled_earning_val) + float(earn.earning_amount)),2)
        if(earn.earning_type == "affiliate"):
            affilite_earn_val = round(float(float(affilite_earn_val) + float(earn.earning_amount)),2)
        if(earn.earning_type != "cancelled"):
            total_earning_val = round(float(float(total_earning_val) + float(earn.earning_amount)),2)
        if(earn.withdrawn_amount != None):
            if(earn.withdrawn_amount != ''):
                withdrawed_credit_val = round(float(float(withdrawed_credit_val) + float(earn.withdrawn_amount)),2)
        if(earn.credit_used != None):
            if(earn.credit_used != ''):
                with_used_credit_val = round(float(float(with_used_credit_val) + float(earn.credit_used)),2)
        if(earn.aval_with != None or earn.clearence_status == "cleared" ):
            if(earn.withdrawn_amount != "" or earn.credit_used != "" or  earn.aval_with != "" or len(earn.aval_with.strip()) != 0):
                try:
                    avail_bal_val = round(float(float(avail_bal_val) + float(earn.aval_with)),2)
                except:
                    avail_bal_val = round(float(avail_bal_val),2)
        if(earn.clearence_status == "pending" ):
            current_earning_val = round(float(float(current_earning_val) + float(earn.earning_amount)),2)
        try:
            earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S").date()
        except:
            earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S.%f").date()
        todays_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if(int(todays_date.month) == int(earned_date.month)):
            cancelled_earning_val = round(float(float(cancelled_earning_val) + float(earn.earning_amount)),2)
    refund_earning = User_Refund.objects.filter(user_id=userDetails,refund_status="cancelled")
    for r_earn in refund_earning:
        availcredit_bal_val = round(float(float(availcredit_bal_val) + float(r_earn.refund_amount)),2)
        if(r_earn.credit_used != None):
            if(r_earn.credit_used != ''):
                ref_used_credit_val = round(float(float(ref_used_credit_val) + float(r_earn.credit_used)),2)
    if(UserAvailable.objects.filter(user_id=userDetails).exists() == True):
        user_avail_details = UserAvailable.objects.get(user_id=userDetails)
        try:
            availableto_date = datetime.strptime(str(user_avail_details.available_to),"%Y-%m-%d %H:%M:%S").date()
        except:
	        availableto_date = datetime.strptime(str(user_avail_details.available_to),"%Y-%m-%d %H:%M:%S.%f").date()
        if(int(todays_date.month) == int(availableto_date.month) and int(todays_date.day) == int(availableto_date.day) and int(todays_date.year) == int(availableto_date.year) ):
            UserAvailable.objects.filter(user_id=userDetails).delete()
    userDetails.total_earning = total_earning_val
    userDetails.current_earning = current_earning_val
    userDetails.cancelled_earning = cancelled_earning_val
    userDetails.avail_bal = avail_bal_val
    userDetails.availcredit_bal = availcredit_bal_val
    userDetails.referrals_earnings = affilite_earn_val
    userDetails.withdrawn_amount = withdrawed_credit_val
    userDetails.with_credits_used_amount = with_used_credit_val
    userDetails.refund_credits_used_amount = ref_used_credit_val
    userDetails.save()


                        
class AdminNotification_commands(admin.ModelAdmin):
    list_display = ['notification','slug','is_active','mail_active']

admin.site.register(Notification_commands, AdminNotification_commands)

class AdminsupportMapping(admin.ModelAdmin):
    list_display = ['suport_topic','map_to','timestamp']

admin.site.register(supportMapping, AdminsupportMapping)

class AdminContactus(admin.ModelAdmin):
    list_display = ['id','email','message','status','created_at','updated_at']

admin.site.register(Contactus, AdminContactus)

class AdminCustomNotifications(admin.ModelAdmin):
    list_display = ['sender','recipient','verb','description','order_no','timestamp','is_read']

admin.site.register(CustomNotifications, AdminCustomNotifications)

class AdminTopicDetails(SummernoteModelAdmin):
    list_display = ['topic_Name','topic_Desc','timestamp']
    summernote_fields = ('topic_Desc', )
    class Media:
        css = {'all': ('assets/css/frontend/topic_Details.css', )} 

admin.site.register(TopicDetails, AdminTopicDetails)

class AdminLogoImages(admin.ModelAdmin):
    list_display = ['image','slug']

admin.site.register(LogoImages, AdminLogoImages)

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
    list_display = ['order_no','order_status','package_gig_name','order_date','order_amount','due_date','completed_date','incoming_request']

admin.site.register(User_orders, AdminUser_orders)


@receiver(pre_save, sender=User_orders)
def update_order_status(sender, instance, **kwargs):
    if(instance.pk is None):
        pass
    else:
        try:
            previous_val = User_orders.objects.get(pk = instance.pk)
            previous_status =  str(previous_val.order_status)
            if(previous_status == "active" or previous_status == "delivered"):
                if(instance.order_status == "cancel" and instance.incoming_request == "admin"):
                    order_details = User_orders.objects.get(order_no = instance.order_no)
                    order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    order_details.save()
                    order_by_user = User.objects.get(username= order_details.order_by.username)
                    order_to_user = User.objects.get(username= order_details.order_to.username)
                    transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                    transaction.transaction_status = "cancelled"
                    transaction.save()
                    try:    
                        cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                    except:
                        cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)
                    order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "Order Cancelled",conversation_id=cover_detls,order_no=order_details,message_type="chat")
                    order_message.save()
                    User_Order_Resolution.objects.filter(raised_by = order_by_user, raised_to= order_to_user,resolution_status="pending").update(resolution_status="rejected", resolution_cancel_mssg = "Order Cancelled.")
                    User_Order_Resolution.objects.filter(raised_by = order_to_user, raised_to= order_by_user,resolution_status="pending").update(resolution_status="rejected", resolution_cancel_mssg = "Order Cancelled.")
                    get_message =  Order_Message.objects.get(pk = order_message.pk)
                    resolution= User_Order_Resolution(resolution_type='cancel',resolution_text = "Cancellation Request",resolution_message="Cancellation Request",resolution_desc="Cancellation Request",resolution_status="accepted",order_no=order_details,raised_by=order_by_user,raised_to=order_to_user,message=get_message)
                    resolution.save()
                    res_details = User_Order_Resolution.objects.get(pk = resolution.pk)
                    refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res_details,order_no=order_details,transaction=transaction ,user_id=order_by_user)
                    refund_details.save()  
                    order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                    order_ativity.save()
                    earning_val = 0
                    if(float(order_details.order_amount) <=40):
                        payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                        for p in payment_parameters:
                            serv_fees_val = p.service_fees
                            serv_fees_type = p.fees_type
                            if(serv_fees_type == "flat"):
                                service_fees_price =  int(serv_fees_val)
                            else:
                                perceof_budg = float((float(order_details.order_amount)* int(serv_fees_val))/100)
                                service_fees_price = round(perceof_budg,2)
                    else:
                        payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                        for p in payment_parameters:
                            serv_fees_val = p.service_fees
                            serv_fees_type = p.fees_type
                            if(serv_fees_type == "flat"):
                                service_fees_price =  int(serv_fees_val)
                            else:
                                perceof_budg = float((float(order_details.order_amount)* int(serv_fees_val))/100)
                                service_fees_price = round(perceof_budg,2)
                    earning_val = float(earning_val) + (round(float(round(float(order_details.order_amount),2) - service_fees_price),2))
                    order_ativity1 = User_Order_Activity(order_message = "Cancelled Payment Refunded to Buyer",order_amount = earning_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                    order_ativity1.save()
                    service_fees_price = 0
                    if(float(order_details.order_amount) <=40):
                        payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                        for p in payment_parameters:
                            serv_fees_val = p.service_fees
                            serv_fees_type = p.fees_type
                            if(serv_fees_type == "flat"):
                                service_fees_price =  int(serv_fees_val)
                            else:
                                perceof_budg = float((float(order_details.order_amount)* int(serv_fees_val))/100)
                                service_fees_price = round(perceof_budg,2)
                    else:
                        payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                        for p in payment_parameters:
                            serv_fees_val = p.service_fees
                            serv_fees_type = p.fees_type
                            if(serv_fees_type == "flat"):
                                service_fees_price =  int(serv_fees_val)
                            else:
                                perceof_budg = float((float(order_details.order_amount)* int(serv_fees_val))/100)
                                service_fees_price = round(perceof_budg,2)
                    earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                    refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=None,clearence_status="cancelled",cleared_on=None,user_id=order_to_user,earning_type="cancelled",affiliate_user=None)
                    refund_details.save()
                    update_all_balancevalues(order_by_user)
                    update_all_balancevalues(order_to_user)
                    notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                    if(notification_cancel.is_active == True):
                        noti_create = CustomNotifications(sender = order_to_user, recipient=order_by_user, verb='order' ,order_no = order_details,description= str(order_to_user.username).title() + " cancelled the Order.")
                        noti_create.save()
                    if(order_by_user.mail_order == True):
                        mail_content = MailTemplates.order_cancelled_buyer(str(order_by_user.username).title(),str("#"+order_details.order_no))
                        SendEmailAct(str(order_by_user.email),mail_content,"Your order has been cancelled.")
                    if(order_to_user.mail_order == True):
                        mail_content = MailTemplates.order_cancelled_seller(str(order_to_user.username).title(),str(order_by_user.username).title(),str("#"+order_details.order_no))
                        SendEmailAct(str(order_to_user.email),mail_content,"Your order has been cancelled by " + str(order_to_user.username).title() + ".")
            else:
                if(previous_status == "completed"):
                    
                    if(instance.order_status == "cancel" and instance.incoming_request == "admin"):
                        order_details = User_orders.objects.get(order_no = instance.order_no)
                        order_by_user = User.objects.get(username= order_details.order_by.username)
                        order_to_user = User.objects.get(username= order_details.order_to.username)
                        earning_details = User_Earnings.objects.get(order_no=order_details,user_id=order_to_user,earning_type="order")
                        clearence_date = ''
                        earning_tip = None
                        try:
                            earning_tip = User_Earnings.objects.get(order_no=order_details,user_id=order_to_user,earning_type="tip")
                        except:
                            earning_tip = None
                        try:
                            clearence_date = datetime.strptime(str(earning_details.clearence_date),"%Y-%m-%d %H:%M:%S").date()
                        except:
                            clearence_date = datetime.strptime(str(earning_details.clearence_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        refunded_val = 0
                        can_order_val = 0
                        can_tip_val = 0
                        todays_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        if(int(todays_date.month) == int(clearence_date.month) and int(clearence_date.day) > int(todays_date.day) and int(todays_date.year) == int(clearence_date.year)):
                            earning_details.clearence_status = "cancelled"
                            earning_details.earning_type = "cancelled"
                            earning_details.save()
                            transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                            transaction.transaction_status = "cancelled"
                            transaction.save()
                            try:    
                                cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                            except:
                                cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)
                            order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "Order Cancelled by Admin",conversation_id=cover_detls,order_no=order_details,message_type="chat")
                            order_message.save()
                            get_message =  Order_Message.objects.get(pk = order_message.pk)
                            resolution= User_Order_Resolution(resolution_type='cancel',resolution_text = "Cancellation Request",resolution_message="Cancellation Request",resolution_desc="Cancellation Request",resolution_status="accepted",order_no=order_details,raised_by=order_by_user,raised_to=order_to_user,message=get_message)
                            resolution.save()
                            res_details = User_Order_Resolution.objects.get(pk = resolution.pk)
                            refunded_val = float(float(refunded_val) + float(earning_details.order_amount))
                            can_order_val = float(earning_details.earning_amount)
                            if(earning_tip != None):
                                transaction_tip = User_Transactions.objects.get(order_no=order_details,paid_for='tip')
                                transaction_tip.transaction_status = "cancelled"
                                transaction_tip.save()
                                refunded_val = float(float(refunded_val) + float(earning_tip.order_amount))
                                can_tip_val = float(float(can_tip_val) + float(earning_tip.earning_amount))
                                earning_tip.clearence_status = "cancelled"
                                earning_tip.earning_type = "cancelled"
                                earning_tip.save()
                                order_ativity = User_Order_Activity(order_message = "×1 Tip Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                                order_ativity.save()
                                order_ativity1 = User_Order_Activity(order_message = "Cancelled Tip Refunded to Buyer",order_amount = can_tip_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                                order_ativity1.save()
                                User_Order_Activity.objects.filter(order_message="Pending for Clearence",order_no=order_details,activity_type="pending",activity_by=order_by_user,activity_to=order_to_user).delete()
                                User_Order_Activity.objects.filter(order_message="Tip Provide by Buyer",order_no=order_details,activity_type="tip",activity_by=order_by_user,activity_to=order_to_user).delete()
                            refund_details = User_Refund(refund_amount=refunded_val,resolution=res_details,order_no=order_details,transaction=transaction ,user_id=order_by_user)
                            refund_details.save()
                            order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                            order_ativity.save()
                            order_ativity1 = User_Order_Activity(order_message = "Cancelled Payment Refunded to Buyer",order_amount = can_order_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                            order_ativity1.save()
                            User_Order_Activity.objects.filter(order_message="Pending for Clearence",order_no=order_details,activity_type="pending",activity_by=order_by_user,activity_to=order_to_user).delete()
                            User_Order_Activity.objects.filter(order_message="×1 Order Completed",order_no=order_details,activity_type="completed",activity_by=order_by_user,activity_to=order_to_user).delete()
                            Seller_Reviews.objects.filter(s_review_from=order_by_user,s_review_to=order_to_user).delete()
                            Buyer_Reviews.objects.filter(b_review_from=order_to_user,b_review_to=order_by_user).delete()
                            update_all_balancevalues(order_by_user)
                            update_all_balancevalues(order_to_user)
                            notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                            if(notification_cancel.is_active == True):
                                noti_create = CustomNotifications(sender = order_to_user, recipient=order_by_user, verb='order' ,order_no = order_details,description= str(order_to_user.username).title() + " cancelled the Order.")
                                noti_create.save()
                            if(order_by_user.mail_order == True):
                                mail_content = MailTemplates.order_cancelled_buyer(str(order_by_user.username).title(),str("#"+order_details.order_no))
                                SendEmailAct(str(order_by_user.email),mail_content,"Your order has been cancelled.")
                            if(order_to_user.mail_order == True):
                                mail_content = MailTemplates.order_cancelled_seller(str(order_to_user.username).title(),str(order_by_user.username).title(),str("#"+order_details.order_no))
                                SendEmailAct(str(order_to_user.email),mail_content,"Your order has been cancelled by " + str(order_to_user.username).title() + ".") 
        except:
            pass
                

class AdminUser_Order_Activity(admin.ModelAdmin):
    list_display = ['order_message','order_amount','activity_date','order_no','activity_type','activity_by','activity_to']

admin.site.register(User_Order_Activity, AdminUser_Order_Activity)


class AdminChatWords(admin.ModelAdmin):
    list_display = ['name','slug','timestamp']

admin.site.register(ChatWords, AdminChatWords)


class AdminUploadFile(admin.ModelAdmin):
    list_display = ['existingPath','name','eof','timestamp']

admin.site.register(UploadFile, AdminUploadFile)

class AdminUser_Refund(admin.ModelAdmin):
    list_display = ['refund_amount','refund_date','used_on','used_offer_id','resolution','order_no','credit_used','transaction','refund_status','user_id']

admin.site.register(User_Refund, AdminUser_Refund)

class AdminUser_Earnings(admin.ModelAdmin):
    list_display = ['order_amount','earning_amount','earning_date','platform_fees','aval_with','resolution','order_no','clearence_date','clearence_status','cleared_on','user_id','earning_type','affiliate_user','withdrawn_on','withdrawn_amount','credit_used','used_on','used_offer_id','withdrawn_status']

admin.site.register(User_Earnings, AdminUser_Earnings)


class AdminUser_Order_Resolution(admin.ModelAdmin):
    list_display = ['resolution_type','resolution_text','resolution_message','resolution_desc','resolution_days','resolution_date','resolution_status','order_no','raised_by','raised_to','message','resolution_last_date']

admin.site.register(User_Order_Resolution, AdminUser_Order_Resolution)

class AdminSeller_Reviews(admin.ModelAdmin):
    list_display = ['communication','recommendation','service','average_val','seller_response','buyer_resp_date','review_message','order_no','package_gig_name','s_review_from','s_review_to','review_date']

admin.site.register(Seller_Reviews, AdminSeller_Reviews)

class AdminBuyer_Reviews(admin.ModelAdmin):
    list_display = ['review_message','order_no','package_gig_name','b_review_from','rating_val','b_review_to','review_date']

admin.site.register(Buyer_Reviews, AdminBuyer_Reviews)

class AdminCategory_package_Extra_Service(admin.ModelAdmin):
    list_display = ['category_name','helper_txt','display_name','display_type']

admin.site.register(Category_package_Extra_Service, AdminCategory_package_Extra_Service)


class AdminGig_favourites(admin.ModelAdmin):
    list_display = ['gig_name','user_id']

admin.site.register(Gig_favourites, AdminGig_favourites)


class AdminUser_warning(admin.ModelAdmin):
    list_display = ['user_id','warning_date','confirmed_status','confirmed_on','spamword']

admin.site.register(User_warning, AdminUser_warning)


class AdminSpamDetection(admin.ModelAdmin):
    list_display = ['user_id','detected_word','detected_on','block_button']
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('block-scenario/<int:pk>/', self.block_scenario, name="admin_block_scenario"),
        ]
        return my_urls + urls
    
    def block_scenario(self, request, pk):
        get_spam_detection = SpamDetection.objects.get(pk = pk)
        if(get_spam_detection.sent_status != "sent"):
            spam_user = User.objects.get(username = get_spam_detection.user_id.username)
            add_warning = User_warning(user_id= spam_user,confirmed_on=None,spamword= get_spam_detection)
            add_warning.save()
            get_spam_detection.sent_status = 'sent'
            get_spam_detection.save()
        return redirect(request.META.get('HTTP_REFERER'))
    

admin.site.register(SpamDetection, AdminSpamDetection)

def view_admin_dashboard(request, format=None):
    return render(request , 'admin_dashboard.html')

class AdminLearningTopicDetails(admin.ModelAdmin):
    list_display = ['topic_Name','topic_description','image_Text','video_url','upload_pdf','created_at']

admin.site.register(LearningTopicDetails, AdminLearningTopicDetails)

class AdminOrder_Conversation(admin.ModelAdmin):
    list_display = ['initiator','receiver','timestamp','order_no']

admin.site.register(Order_Conversation, AdminOrder_Conversation)

class AdminConversation(admin.ModelAdmin):
    list_display = ['initiator','receiver','timestamp','convers_type']

admin.site.register(Conversation, AdminConversation)

class AdminMessage(admin.ModelAdmin):
    list_display = ['sender','receiver','text','attachment','is_read','request_offers_id','conversation_id','timestamp','message_type','buyer_request_id','mail_sent']

admin.site.register(Message, AdminMessage)

class AdminMessage_Response_Time(admin.ModelAdmin):
    list_display = ['receiver','timestamp']

admin.site.register(Message_Response_Time, AdminMessage_Response_Time)


class AdminUser_orders_Extra_Gigs(admin.ModelAdmin):
    list_display = ['order_no','package_gig_name','gig_extra_package','gig_extra_delivery']

admin.site.register(User_orders_Extra_Gigs, AdminUser_orders_Extra_Gigs)


class AdminOrder_Delivery(admin.ModelAdmin):
    list_display = ['delivery_message','attachment','delivery_date','order_no','delivered_by','delivered_to','delivery_status','resolution','total_revision','current_revision']

admin.site.register(Order_Delivery, AdminOrder_Delivery)

class AdminOrder_Message(admin.ModelAdmin):
    list_display = ['sender','receiver','text','attachment','conversation_id','timestamp','order_no','message_type','is_read','mail_sent']

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



class MainMenuExportResource(resources.ModelResource):
    category_Name = fields.Field(column_name='category_Name', attribute='category_Name',
               widget=widgets.ForeignKeyWidget(model=Categories, field='category_Name'))
    sub_category_Name = fields.Field(column_name='sub_category_Name', attribute='sub_category_Name',
               widget=widgets.ForeignKeyWidget(model=SubCategories, field='sub_category_Name'))
    sub_sub_category_Name = fields.Field(column_name='sub_sub_category_Name', attribute='sub_sub_category_Name',
               widget=widgets.CharWidget())
    slug = fields.Field(column_name='slug', attribute='slug',
               widget=widgets.CharWidget())
    Tags = fields.Field(column_name='Tags', attribute='Tags',
               widget=widgets.CharWidget())
         
class AdminSubSubCategories(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['category_Name','sub_category_Name','sub_sub_category_Name','slug','Tags']
    
    class Media:
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','assets/js/sub_sub_category.js')
    
    def get_export_resource_class(self):
        return MainMenuExportResource
    
    # def get_import_resource_class(self):     
    #     return MainMenuExportResource
    
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
        js = ('https://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js','assets/js/sub_sub_category1.js')
        
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
    list_display = ['gig_title','gig_category','gig_sub_category','gig_description','gig_status','user_id','gig_share_link']
    class Media:
        css = {'all': ('assets/css/frontend/admin_post_request.css', )} 


@receiver(post_save, sender=UserGigs)
def update_gig_status(sender, instance, **kwargs):
    if(instance.id is None):
        pass
    else:
        gig_details = UserGigs.objects.get(id=instance.id)
        if(gig_details.gig_status == "active"):
            senderobj = User.objects.get(username = 'admin')
            receiverobj =  User.objects.get(username = gig_details.user_id.username)
            notification_settings = Notification_commands.objects.get(slug = "gig_active")
            if(notification_settings.is_active == True):
                noti_create = CustomNotifications(sender = senderobj, recipient=receiverobj, verb='gig',description="Your Gig is Approved")
                noti_create.save()
        elif(gig_details.gig_status == "modification"):
            senderobj = User.objects.get(username = 'admin')
            receiverobj =  User.objects.get(username = gig_details.user_id.username)
            notification_settings = Notification_commands.objects.get(slug = "gig_modification")
            if(notification_settings.is_active == True):
                noti_create = CustomNotifications(sender = senderobj, recipient=receiverobj, verb='gig',description="Your Gig requires Modifications")
                noti_create.save()
        elif(gig_details.gig_status == "denied"):
            senderobj = User.objects.get(username = 'admin')
            receiverobj =  User.objects.get(username = gig_details.user_id.username)
            notification_settings = Notification_commands.objects.get(slug = "gig_denied")
            if(notification_settings.is_active == True):
                noti_create = CustomNotifications(sender = senderobj, recipient=receiverobj, verb='gig',description="Your Gig is Denied")
                noti_create.save()
admin.site.register(UserGigs, AdminUserGigs)


class AdminUserGigsImpressions(admin.ModelAdmin):
    list_display = ['ip_address','impress_type','gig_name','user_id','impress_date']

admin.site.register(UserGigsImpressions, AdminUserGigsImpressions)


class AdminUserAvailable(admin.ModelAdmin):
    list_display = ['available_from','available_to','available_mssg','available_for_new','available_types','user_id']

admin.site.register(UserAvailable, AdminUserAvailable)


class AdminBuyer_Post_Request(admin.ModelAdmin):
    list_display = ['service_desc','service_images','service_category','send_to','service_type','buyer_request_id','service_sub_category','service_time','service_budget','service_date','user_id','service_status','individual_request_status']
    class Media:
        css = {'all': ('assets/css/frontend/admin_post_request.css', )}
        
@receiver(post_save, sender=Buyer_Post_Request)
def update_post_status(sender, instance, **kwargs):
    if(instance.id is None):
        pass
    else:
        post_request = Buyer_Post_Request.objects.get(id=instance.id)
        if(post_request.service_status == "active"):
            senderObj = User.objects.get(username = 'admin')
            receiverObj =  User.objects.get(username = post_request.user_id.username)
            notification_settings = Notification_commands.objects.get(slug = "buyer_post_request_active")
            if(notification_settings.is_active == True):
                noti_create = CustomNotifications(sender = senderObj, recipient=receiverObj, verb='request',description="Your Request is Approved")
                noti_create.save()
        elif(post_request.service_status == "rejected"):
            senderObj = User.objects.get(username = 'admin')
            receiverObj =  User.objects.get(username = post_request.user_id.username)
            notification_settings = Notification_commands.objects.get(slug = "buyer_post_request_rejected")
            if(notification_settings.is_active == True):
                noti_create = CustomNotifications(sender = senderObj, recipient=receiverObj, verb='request',description="Your Request is Rejected")
                noti_create.save()
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
    list_display = ['gig_name','buyer_request','user_id','custom_user','offer_desc','offer_budget','offer_time','no_revisions','ask_requirements','extra_parameters','offer_type','offer_date','offer_status_by_buyer']
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
    list_display = ['affiliate_code','ip_address','user_id','refferal_user','seller_affi_amount','buyer_affi_amount','buyer_affi_done','seller_affi_done']

admin.site.register(Referral_Users, AdminReferral_Users)


class AdminApi_keys(admin.ModelAdmin):
    list_display = ['api_name','secrete_key','private_key','created_on']

admin.site.register(Api_keys, AdminApi_keys)


class AdminSMTP_settings(admin.ModelAdmin):
    list_display = ['mail_host','mail_address','mail_password','mail_port','is_active','created_on']

admin.site.register(SMTP_settings, AdminSMTP_settings)


class AdminAddon_Parameters(admin.ModelAdmin):
    list_display = ['parameter_name','no_of_days']

admin.site.register(Addon_Parameters, AdminAddon_Parameters)


class AdminUser_Transactions(admin.ModelAdmin):
    list_display = ['gig_name','offer_id','payment_type','transaction_id','payment_status','paypal_id','paypal_email','flutter_account_id','order_no','transaction_status','paid_for','credits_used']

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
    if(Id == "index"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "about"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "affiliate_program"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "approval_process"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "buyer_protection"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "earn_letworkbdone"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "for_freelancer"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "privacy"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "prohibited_service"):
        context = {'templateName':Id+ ".html"}
    elif(Id == "terms"):
        context = {'templateName':Id+ ".html"}
    return render(request , 'contents.html',context)


def get_admin_urls(urls):
    def get_urls():
        my_urls =  [
            path('view_admin_dashboard/', view_admin_dashboard, name="view_admin_dashboard"),
        ]
        return my_urls + urls
    return get_urls

admin.autodiscover()

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls


def SendEmailAct(sendto,message,subject):
    mailsettings = SMTP_settings.objects.filter(is_active= True).first()
    sender_address = mailsettings.mail_address
    sender_password = mailsettings.mail_password
    themsg = MIMEMultipart()
    themsg['Subject'] = subject
    themsg['To'] = sendto
    themsg['From'] = sender_address
    themsg.attach(MIMEText(message, 'html'))
    themsg = themsg.as_string()  
    if( int(mailsettings.mail_port) == 587):
        smtp = smtplib.SMTP(mailsettings.mail_host,int(mailsettings.mail_port))
        smtp.starttls()
    else:
        smtp = smtplib.SMTP_SSL(mailsettings.mail_host, int(mailsettings.mail_port))
    smtp.login(sender_address, sender_password)
    smtp.sendmail(sender_address, sendto, themsg)
    smtp.quit()
    return "mail Sent" 
