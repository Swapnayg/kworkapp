from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import sub
from django.utils import timesince
import psycopg2
import bisect
import smtplib
import shortuuid
import html
from kworkapp.mail_templates import MailTemplates
from functools import reduce
from paypalrestsdk import Payment,Refund,Sale
import paypalrestsdk
from operator import itemgetter
from python_flutterwave import payment
from datetime import datetime, timedelta,date
from dateutil import relativedelta
from pathlib import Path
from tabnanny import verbose
from django.views import View
from urllib.parse import urlparse
import whatismyip
from django_countries import countries
import pathlib
from django.contrib.auth import logout
from django.shortcuts import redirect, render
import re
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from django.core import serializers
import json
from kworkapp.models import Categories,UserGigPackages,AdminLogging,SellerLevels4,SMTP_settings,LogoImages,CustomNotifications,UploadFile,Withdrwal_initiated,Notification_commands,Api_keys,SpamDetection,User_warning,User_Refund,User_Earnings,ChatWords,Gig_favourites,User_orders_Extra_Gigs,Conversation,Conversation,Order_Message,Order_Conversation,Order_Delivery,Message_Response_Time,User_Order_Activity,User_Order_Resolution,User_Transactions,Payment_Parameters,Request_Offers,Referral_Users,UserGigPackage_Extra,Buyer_Post_Request,Seller_Reviews,Buyer_Reviews,UserGigsImpressions,User_orders,UserSearchTerms,UserGig_Extra_Delivery,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserAvailable,UserGigs,UserGigsTags,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages,Addon_Parameters,Buyer_Requirements, UserProfileDetails, supportMapping, supportTopic,Message
import operator

class indexView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'index.html')

class menu_pageView(View):
    return_url = None
    def get(self , request,category=''):
        category_details = Categories.objects.get(category_Name=category)
        sub_category = SubCategories.objects.filter(category_Name=category_details)
        return render(request , 'menu_page.html',{"details":category_details,"sub_details":sub_category})


class all_gigs_pageView(View):
    return_url = None
    def get(self , request,category='',subcategry='',topic=''):
        tagslist= []
        sub_sub_category = []
        if(len(subcategry)== 0):
            category_details = Categories.objects.get(category_Name=category)
            sub_categoryd = SubCategories.objects.get(category_Name=category_details,sub_category_Name=topic)
            sub_sub_category = SubSubCategories.objects.filter(category_Name=category_details,sub_category_Name=sub_categoryd)
            for sub in sub_sub_category:
                for sub_cat in sub.tags.all():
                    tagslist.append(sub_cat.name.strip())
        else:
            category_details = Categories.objects.get(category_Name=category)
            sub_categoryd = SubCategories.objects.get(category_Name=category_details,sub_category_Name=subcategry)
            sub_sub_category = SubSubCategories.objects.filter(category_Name=category_details,sub_category_Name=sub_categoryd)
            for sub in sub_sub_category:
                for sub_cat in sub.tags.all():
                    tagslist.append(sub_cat.name.strip())
        seller_levels = SellerLevels4.objects.all()
        return render(request , 'gigs_page.html',{"details":category_details,"sub_details":sub_categoryd,"sub_topics":sub_sub_category,"tagslist":tagslist,"seller_levels":seller_levels})

class aboutView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'about.html')

class privacyView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'privacy.html')

class gig_View_View(View):
    return_url = None
    def get(self , request,username='',gig_title='',share = 0):
        try:
            userDetails = User.objects.exclude(profile_status="blocked").get(username = username)
            if(userDetails != None):
                ipAddress = ''
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ipAddress = x_forwarded_for.split(',')[0]
                languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
                userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                pro_last_delivery = ''
                u_last_delivery = ''
                u_created_on= ''
                try:
                    u_last_delivery = datetime.strptime(str(userDetails.u_last_delivery),"%Y-%m-%d %H:%M:%S.%f").date()
                except:
                    u_last_delivery = datetime.strptime(str(userDetails.u_last_delivery),"%Y-%m-%d %H:%M:%S").date()
                try:
                    u_created_on = datetime.strptime(str(userDetails.created_at),"%Y-%m-%d %H:%M:%S.%f").date()
                except:
                    u_created_on = datetime.strptime(str(userDetails.created_at),"%Y-%m-%d %H:%M:%S").date()
                if(int(u_last_delivery.month) == int(u_created_on.month) and int(u_last_delivery.day) == int(u_created_on.day) and int(u_last_delivery.year) == int(u_created_on.year)):
                    pro_last_delivery = "Just Started"
                else:
                    pro_last_delivery =  userDetails.u_last_delivery
                userlang = []
                english_profi = ''
                userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                for lang in userlanguages:
                    userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof}) 
                gig_details = ''
                if(int(share) == 1):
                    try:
                        gig_details = UserGigs.objects.get(user_id=userDetails ,gig_share_link= gig_title,gig_status="active")
                    except:
                        gig_details = ''
                else:  
                    try:
                        gig_details = UserGigs.objects.get(user_id=userDetails ,gig_title= gig_title,gig_status="active")
                    except:
                        gig_details = ''
                if(gig_details != ''):
                    gig_package_details = UserGigPackages.objects.filter(user_id=userDetails ,package_gig_name= gig_details)
                    gig_image_details = Usergig_image.objects.filter(user_id=userDetails ,package_gig_name= gig_details)
                    seller_reviews = Seller_Reviews.objects.filter(s_review_to=userDetails,package_gig_name= gig_details)
                    seller_all_reviews = Seller_Reviews.objects.filter(s_review_to=userDetails)
                    active_orders_cnt = User_orders.objects.filter(package_gig_name = gig_details,order_status="active").count()
                    comm_count = 0
                    recc_count = 0
                    serv_count = 0
                    seller_count = 0
                    seller_all_count = 0
                    s_review_date = ''
                    seller_rev_data = []
                    for sa_review in seller_all_reviews:
                        seller_all_count = seller_all_count + float(sa_review.average_val)
                    for s_review in seller_reviews:
                        comm_count = comm_count + int(s_review.communication)
                        recc_count = recc_count + int(s_review.recommendation)
                        serv_count = serv_count + int(s_review.service)
                        seller_count = seller_count + float(s_review.average_val)
                        s_review_date = s_review.review_date
                        s_resp_date = s_review.buyer_resp_date
                        country_flag_icon = '/static/assets/images/flags/'+ s_review.s_review_from.country.code.lower()+ '.svg'
                        seller_rev_data.append({"message":s_review.review_message,"review":s_review.average_val,"sender":s_review.s_review_from,"review_date":s_review_date,"seller_resp_date":s_resp_date,"buyer_resp":s_review.seller_response,"country_flag":country_flag_icon})                 
                    try:
                        seller_count = round(float(round(seller_count/len(seller_reviews),0)))
                    except:
                        seller_count = 0
                    try:
                        comm_count = round(comm_count/len(seller_reviews),1)
                    except:
                        comm_count = 0
                    try:
                        recc_count = round(recc_count/len(seller_reviews),1)
                    except:
                        recc_count = 0
                    try:
                        serv_count = round(serv_count/len(seller_reviews),1)
                    except:
                        serv_count = 0
                    try:
                        seller_all_count = round(seller_all_count/len(seller_all_reviews),1)
                    except:
                        seller_all_count = 0
                    seller_levl= str(userDetails.user_level.level_name)
                    active_gigs_details = UserGigs.objects.filter(user_id=userDetails, gig_status='active').exclude(gig_title=gig_details.gig_title)
                    active_gigs_data= []
                    for u_gig in active_gigs_details:
                        gig_image = Usergig_image.objects.filter(user_id=userDetails,package_gig_name=u_gig).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        active_gigs_data.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url})
                    favourite_Count= Gig_favourites.objects.filter(gig_name=gig_details).count()
                    curr_fav = ''
                    if(Gig_favourites.objects.filter(gig_name=gig_details,user_id=userDetails).exists() == True):
                        curr_fav = 'yes'
                    else:
                        curr_fav = 'no'
                    if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
                        userDetails1 = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                        impressions = UserGigsImpressions(ip_address=str(ipAddress),impress_type ="click" ,gig_name=gig_details, user_id=userDetails1)
                        impressions.save()
                    else:   
                        impressions = UserGigsImpressions(ip_address=str(ipAddress),impress_type ="click" ,gig_name=gig_details)
                        impressions.save()
                    extra_gigs = UserExtra_gigs.objects.filter(package_gig_name=gig_details)
                    return render(request , 'Dashboard/view_gig.html',{'userDetails':userDetails,"profile_Details":userProfileDetails,"userlanguages":userlang,"gig_details":gig_details,"gig_package_Details":gig_package_details,"gig_image_Details":gig_image_details,"gig_reviews":seller_rev_data,"seller_count":seller_count,"comm_count":comm_count,"recc_count":recc_count,"serv_count":serv_count,"seller_level":seller_levl,"seller_all_review":seller_all_reviews,"seller_all_count":seller_all_count,"Other_gigs":active_gigs_data,"fav_count":favourite_Count,"current_user_fav":curr_fav,"extra_gigs":extra_gigs,"active_orders":active_orders_cnt,"profile_last_delivery":pro_last_delivery,"has_records":"yes"})      
                else:
                    gig_details = []    
                    return render(request , 'Dashboard/view_gig.html',{"has_records":"no"} )
            else:
                return render(request , 'Dashboard/view_gig.html',{"has_records":"no"} )     
        except:
            return render(request , 'register.html')
            
class buyer_protectionView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'buyer_protection.html')

class term_serviceView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'terms.html')

class for_freelancerView(View):
    return_url = None
    def get(self , request,username=''):
        userdata= []
        subcategory= SubCategories.objects.all()
        for sub_cat in subcategory:
            u_profile = UserProfileDetails.objects.filter(sub_category=sub_cat).first()
            if(u_profile != None):
                if(len(userdata) <= 8):
                    userdata.append({"username":u_profile.user_id.username, "profession":u_profile.sub_category.sub_category_Name,"joined_dt":u_profile.user_id.created_at,"profile_img":u_profile.user_id.avatar})
        return render(request , 'for_freelancer.html',{"user_details":userdata})

class earn_letorkbdoneView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'earn_letworkbdone.html')

class categoriesView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'categories.html')

class affiliate_programView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'affiliate_program.html') 

class reviews_View(View):
    return_url = None
    def get(self , request,username=''):
        categories = Categories.objects.all()
        buyer_reviews = Buyer_Reviews.objects.all()
        buyer_count = 0
        for b_review in buyer_reviews:
            buyer_count = buyer_count + int(b_review.rating_val)
        try:
            buyer_count = round(buyer_count/len(buyer_reviews),1)
        except:
            buyer_count = 0
        slideruserdata= []
        subcategory= SubCategories.objects.all()
        for sub_cat in subcategory:
            u_profile = UserProfileDetails.objects.filter(sub_category=sub_cat).first()
            if(u_profile != None):
                if(len(slideruserdata) <= 4):
                    slideruserdata.append({"username":u_profile.user_id.username, "profession":str(u_profile.sub_category.sub_category_Name).lower(),"joined_dt":u_profile.user_id.created_at,"profile_img":u_profile.user_id.avatar,"category_img":str(sub_cat.image)})
        return render(request , 'reviews.html',{"categories":categories,"no_reviews":len(buyer_reviews), "aver_count":buyer_count,"slider_user_Details":slideruserdata})

class prohibited_service_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'prohibited_service.html')
    
class approval_process_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'approval_process.html')

class faq_View(View):
    return_url = None
    def get(self , request,username=''):
        support_desc = 0
        charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "contact_support_description"))
        for c in charcterlimits:
            if(c.Char_category_Name == "contact_support_description"):
                support_desc = c.Max_No_of_char_allowed
        return render(request , 'faq.html',{"support_desc":support_desc})


class contact_support_View(View):
    return_url = None
    def get(self , request,username=''):
        support_desc = 0
        charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "contact_support_description"))
        for c in charcterlimits:
            if(c.Char_category_Name == "contact_support_description"):
                support_desc = c.Max_No_of_char_allowed
        return render(request , 'contact_support.html',{"support_desc":support_desc})

class partners_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'partners.html')


class signup_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'register.html')

class login_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'login.html')

class profile_view(View):
    return_url = None
    def get(self , request,username=''):
        try:
            try:
                userDetails = User.objects.get(username=username ,profile_status="active")
            except:
                userDetails = ''
            if(userDetails != ''):
                userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                pro_last_delivery = ''
                u_last_delivery = ''
                u_created_on= ''
                try:
                    u_last_delivery = datetime.strptime(str(userDetails.u_last_delivery),"%Y-%m-%d %H:%M:%S.%f").date()
                except:
                    u_last_delivery = datetime.strptime(str(userDetails.u_last_delivery),"%Y-%m-%d %H:%M:%S").date()
                try:
                    u_created_on = datetime.strptime(str(userDetails.created_at),"%Y-%m-%d %H:%M:%S.%f").date()
                except:
                    u_created_on = datetime.strptime(str(userDetails.created_at),"%Y-%m-%d %H:%M:%S").date()
                if(int(u_last_delivery.month) == int(u_created_on.month) and int(u_last_delivery.day) == int(u_created_on.day) and int(u_last_delivery.year) == int(u_created_on.year)):
                    pro_last_delivery = "Just Started"
                else:
                    pro_last_delivery = userDetails.u_last_delivery
                userlang = []
                for lang in userlanguages:
                    userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})  
                active_gig_details = []
                draft_gig_details = []
                user_gigs_details = UserGigs.objects.filter(user_id=userDetails)
                seller_reviews = Seller_Reviews.objects.filter(s_review_to=userDetails)
                buyer_reviews = Buyer_Reviews.objects.filter(b_review_to=userDetails)
                categories = Categories.objects.all()
                comm_count = 0
                recc_count = 0
                serv_count = 0
                seller_count = 0
                buyer_count = 0
                b_review_date = ''
                seller_rev_data = []
                buyer_rev_data = []
                for s_review in seller_reviews:
                    comm_count = comm_count + int(s_review.communication)
                    recc_count = recc_count + int(s_review.recommendation)
                    serv_count = serv_count + int(s_review.service)
                    seller_count = seller_count + float(s_review.average_val)
                    s_review_date = s_review.review_date
                    s_resp_date = s_review.buyer_resp_date
                    country_flag_icon = '/static/assets/images/flags/'+ s_review.s_review_from.country.code.lower()+ '.svg'
                    seller_rev_data.append({"message":s_review.review_message,"review":s_review.average_val,"sender":s_review.s_review_from,"review_date":s_review_date,"seller_resp_date":s_resp_date,"buyer_resp":s_review.seller_response,"country_flag":country_flag_icon})                 
                for b_review in buyer_reviews:
                    buyer_count = buyer_count + int(b_review.rating_val)
                    b_review_date = b_review.review_date
                    b_country_flag_icon = '/static/assets/images/flags/'+ b_review.b_review_from.country.code.lower()+ '.svg'
                    buyer_rev_data.append({"message":b_review.review_message,"review":b_review.rating_val,"sender":b_review.b_review_from,"review_date":b_review_date,"country_flag":b_country_flag_icon})
                try:
                    seller_count = round(float(round(seller_count/len(seller_reviews),0)))
                except:
                    seller_count = 0
                try:
                    comm_count = round(comm_count/len(seller_reviews),1)
                except:
                    comm_count = 0
                try:
                    recc_count = round(recc_count/len(seller_reviews),1)
                except:
                    recc_count = 0
                try:
                    serv_count = round(serv_count/len(seller_reviews),1)
                except:
                    serv_count = 0
                try: 
                    buyer_count = round(buyer_count/len(buyer_reviews),1)
                except:
                    buyer_count = 0
                user_availability= []
                try:
                    user_availability_list = UserAvailable.objects.get(Q(user_id=userDetails))
                    user_availability.append({"available_from":datetime.strptime(str(user_availability_list.available_from), "%Y-%m-%d"),"available_to":datetime.strptime(str(user_availability_list.available_to), "%Y-%m-%d"),"available_mssg":str(user_availability_list.available_mssg),"available_for_new":str(user_availability_list.available_for_new),"available_types":str(user_availability_list.available_types)})
                except:
                    user_availability = []
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="available_reason") | Q(Char_category_Name= "post_request_desc"))
                available_char = 0
                post_request_char = 0
                min_selling_price = 0
                resolution_ext = Addon_Parameters.objects.filter(Q(parameter_name="min_starting_price") )
                for ext in resolution_ext:
                    if(ext.parameter_name == "min_starting_price"):
                        min_selling_price = ext.no_of_days
                for c in charcterlimits:
                    if(c.Char_category_Name == "available_reason"):
                        available_char = c.Max_No_of_char_allowed
                    elif(c.Char_category_Name == "post_request_desc"):
                        post_request_char = c.Max_No_of_char_allowed
                for u_gig in user_gigs_details:
                    userpack= UserGigPackages.objects.filter(package_gig_name=u_gig , user_id = userDetails , package_type= 'basic').first() 
                    gig_image = Usergig_image.objects.filter(user_id=userDetails,package_gig_name=u_gig).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    else:
                        gig_image_url = ''
                    if(userpack != None):
                        start_price = userpack.package_price
                    else:
                        start_price = 0 
                    if(u_gig.gig_status == "active"):
                        active_gig_details.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Share_link":u_gig.gig_share_link,"gig_UserName":u_gig.user_id.username,"gig_Image":gig_image_url,"start_price":start_price})
                    elif(u_gig.gig_status == "draft"):
                        draft_gig_details.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Share_link":u_gig.gig_share_link,"gig_UserName":u_gig.user_id.username,"gig_Image":gig_image_url,"start_price":start_price})                    
                return render(request , 'Dashboard/profile.html',{'userDetails':userDetails,"profile_Details":userProfileDetails,"userlanguages":userlang,"active_gigs":active_gig_details,"draft_gigs":draft_gig_details,"seller_reviews":seller_rev_data,"seller_count":seller_count,"comm_count":comm_count,"recc_count":recc_count,"serv_count":serv_count,"buyer_count":buyer_count,"buyer_reviews":buyer_rev_data,"character_avail":int(available_char),"character_post_request":int(post_request_char),"user_avail":user_availability,"categories":categories,"profile_last_delivery":pro_last_delivery,"has_records":"yes","min_price":min_selling_price})                 
            else:
                return render(request , 'Dashboard/profile.html',{"has_records":"no"})
        except:
            return render(request , 'register.html')

class buyer_dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"buyer"
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try: 
                userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                active_gigs_details = UserGigs.objects.filter(gig_status='active')
                active_gigs_data= []
                category_list = []
                categories = Categories.objects.all()
                for c in categories:
                    sub_cat = SubSubCategories.objects.filter(category_Name=c).first()
                    if(sub_cat != None):
                        category_list.append({"cat_name":sub_cat.category_Name.category_Name,"subcat_name":sub_cat.sub_category_Name.sub_category_Name,"subsubcat_name":sub_cat.sub_sub_category_Name})
                pop_category_list = []
                for u_gig in active_gigs_details:
                    gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                        if str(u_gig.gig_category.category_Name) not in pop_category_list:
                            pop_category_list.append(str(u_gig.gig_category.category_Name))
                            active_gigs_data.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_user":u_gig.user_id.id,"gig_username":u_gig.user_id.username,"gig_cat_name":str(u_gig.gig_category.category_Name), "gig_cat_image":str(u_gig.gig_category.image)})
                impression_gigs = UserGigsImpressions.objects.filter(user_id= userDetails).values("gig_name").distinct()
                impression_data = []
                impre_gig_list = []
                for imp in impression_gigs:
                    if(imp["gig_name"] != None):
                        gig_data = UserGigs.objects.exclude(user_id__profile_status="blocked").get(pk=imp["gig_name"])
                        if(gig_data!= None):
                            if(str(gig_data.gig_title).strip() not in impre_gig_list):
                                impre_gig_list.append(str(gig_data.gig_title).strip())
                                imp_gig_image_url = ''
                                imp_gig_image = Usergig_image.objects.filter(package_gig_name=gig_data).first() 
                                if(imp_gig_image != None):
                                    imp_gig_image_url = imp_gig_image.gig_image
                                start_price = 0
                                userpack= UserGigPackages.objects.filter(package_gig_name=gig_data, package_type= 'basic').first() 
                                if(userpack != None):
                                    start_price = userpack.package_price
                                else:
                                    start_price = 0 
                                seller_reviews = Seller_Reviews.objects.filter(package_gig_name= gig_data)
                                seller_count = 0
                                for s_review in seller_reviews:
                                    seller_count = seller_count + float(s_review.average_val)
                                try:
                                    seller_count = round(float(seller_count/len(seller_reviews)))
                                except:
                                    seller_count = 0   
                                impression_data.append({"gig_title":gig_data.gig_title,"gig_img_url":imp_gig_image_url,"start_price":start_price,"seller_count":seller_count,"review_count":len(seller_reviews),"gig_username":gig_data.user_id.username, "gig_gig_img":gig_data.user_id.avatar,"gig_seller_level":gig_data.user_id.user_level.level_name})
                search_term = UserSearchTerms.objects.filter(user_id=userDetails).values("search_words").distinct()
                search_data = []
                gig_names_list = []
                gigs_details = []
                for search in search_term:
                    filterList =  search["search_words"].strip().split(" ")
                    query = Q()
                    query1 = Q()
                    query2 = Q()
                    for letter in filterList:
                        query = query | Q(category_Name__icontains=letter)
                        query1 = query1 | Q(sub_sub_category_Name__icontains=letter)
                        query2 = query2 | Q(gig_title__icontains=letter)
                    gig_category_details = Categories.objects.filter(category_Name__icontains= search["search_words"].strip())
                    gig_sub_category_details = SubSubCategories.objects.filter(sub_sub_category_Name__icontains= search["search_words"].strip())
                    gig_category_details1 = Categories.objects.filter(category_Name= search["search_words"].strip())
                    gig_category_details2 = Categories.objects.filter(query)
                    gig_sub_category_details1 = SubSubCategories.objects.filter(sub_sub_category_Name= search["search_words"].strip())
                    gig_sub_category_details2 = SubSubCategories.objects.filter(query1)
                    if(len(gig_category_details)!=0):
                        for gig_cat in gig_category_details:
                            gigs_details = UserGigs.objects.filter(gig_category =gig_cat.pk, gig_status='active').exclude(user_id__profile_status="blocked")
                    elif(len(gig_category_details1)!=0):
                        for gig_cat in gig_category_details1:
                            gigs_details = UserGigs.objects.filter(gig_category =gig_cat.pk, gig_status='active').exclude(user_id__profile_status="blocked")
                    elif(len(gig_category_details2)!=0):
                        for gig_cat in gig_category_details2:
                            gigs_details = UserGigs.objects.filter(gig_category =gig_cat.pk, gig_status='active').exclude(user_id__profile_status="blocked")
                    elif(len(gig_sub_category_details)!=0):
                        for gig_cat in gig_sub_category_details:
                            gigs_details = UserGigs.objects.filter(gig_category =gig_cat.pk, gig_status='active').exclude(user_id__profile_status="blocked") 
                    elif(len(gig_sub_category_details1)!=0):
                        for gig_cat in gig_sub_category_details1:
                            gigs_details = UserGigs.objects.filter(gig_category =gig_cat.pk, gig_status='active').exclude(user_id__profile_status="blocked")     
                    elif(len(gig_sub_category_details2)!=0):
                        for gig_cat in gig_sub_category_details2:
                            gigs_details = UserGigs.objects.filter(gig_category =gig_cat.pk, gig_status='active').exclude(user_id__profile_status="blocked")        
                    if(len(gigs_details) == 0):
                        gigs_details = UserGigs.objects.filter(gig_title__icontains= search["search_words"].strip(), gig_status='active').exclude(user_id__profile_status="blocked")
                        if(len(gigs_details) ==0):
                            gigs_details = UserGigs.objects.filter(query2, gig_status='active').exclude(user_id__profile_status="blocked")
                            if(len(gigs_details) ==0):
                                gigs_details = UserGigs.objects.filter(gig_title =  search["search_words"].strip(), gig_status='active').exclude(user_id__profile_status="blocked")
                    for sear_gig_data in gigs_details:
                        if(str(sear_gig_data.gig_title).strip() not in gig_names_list):
                            gig_names_list.append(str(sear_gig_data.gig_title).strip())
                            search_gig_image_url = ''
                            sea_gig_image = Usergig_image.objects.filter(package_gig_name=sear_gig_data).first() 
                            if(sea_gig_image != None):
                                search_gig_image_url = sea_gig_image.gig_image
                            start_price = 0
                            sear_userpack= UserGigPackages.objects.filter(package_gig_name=sear_gig_data, package_type= 'basic').first() 
                            if(sear_userpack != None):
                                search_start_price = sear_userpack.package_price
                            else:
                                search_start_price = 0 
                            sear_seller_reviews = Seller_Reviews.objects.filter(package_gig_name= sear_gig_data)
                            sea_seller_count = 0
                            for ss_review in sear_seller_reviews:
                                sea_seller_count = sea_seller_count + float(ss_review.average_val)
                            try:
                                sea_seller_count = round(float(sea_seller_count/len(sear_seller_reviews)))
                            except:
                                sea_seller_count = 0   
                            search_data.append({"gig_title":sear_gig_data.gig_title,"gig_img_url":search_gig_image_url,"start_price":search_start_price,"seller_count":sea_seller_count,"review_count":len(sear_seller_reviews),"gig_username":sear_gig_data.user_id.username, "gig_gig_img":sear_gig_data.user_id.avatar,"gig_seller_level":sear_gig_data.user_id.user_level.level_name})
                return render(request , 'Dashboard/buyer_dashboard.html',{"P_gig_details":active_gigs_data,"cat_list":category_list,"cat_list_json":json.dumps(category_list),"impression_gigs":impression_data,"search_data":search_data})               
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')       

class search_gig_view(View):
    return_url = None
    def get(self , request,keyword=''):
        ipAddress = ''
        keyword = keyword. lower()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipAddress = x_forwarded_for.split(',')[0]
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(ipAddress),search_types="keyword")
            search_term.save()
        else:   
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(ipAddress),search_types="keyword")
            search_term.save()
        filterList = keyword.strip().split(" ")
        query = Q()
        query1 = Q()
        query2 = Q()
        for letter in filterList:
            query = query | Q(category_Name__icontains=letter)
            query1 = query1 | Q(sub_sub_category_Name__icontains=letter)
            query2 = query2 | Q(gig_title__icontains=letter)
        gig_category_details = Categories.objects.filter(category_Name__icontains=keyword.strip())
        gig_sub_category_details = SubSubCategories.objects.filter(sub_sub_category_Name__icontains=keyword.strip())
        gig_category_details1 = Categories.objects.filter(category_Name=keyword.strip())
        gig_category_details2 = Categories.objects.filter(query)
        gig_sub_category_details1 = SubSubCategories.objects.filter(sub_sub_category_Name=keyword.strip())
        gig_sub_category_details2 = SubSubCategories.objects.filter(query1)
        gigs_details = []
        if(len(gig_category_details)!=0):
            for gig_cat in gig_category_details:
                gigs_details = UserGigs.objects.filter(gig_category =gig_cat, gig_status='active').exclude(user_id__profile_status="blocked")
        elif(len(gig_category_details1)!=0):
            for gig_cat in gig_category_details1:
                gigs_details = UserGigs.objects.filter(gig_category =gig_cat, gig_status='active').exclude(user_id__profile_status="blocked")
        elif(len(gig_category_details2)!=0):
            for gig_cat in gig_category_details2:
                gigs_details = UserGigs.objects.filter(gig_category =gig_cat, gig_status='active').exclude(user_id__profile_status="blocked")
        elif(len(gig_sub_category_details)!=0):
            for sub_gig_cat in gig_sub_category_details:
                gigs_details = UserGigs.objects.filter(gig_sub_category =sub_gig_cat, gig_status='active').exclude(user_id__profile_status="blocked") 
        elif(len(gig_sub_category_details1)!=0):
            for sub_gig_cat in gig_sub_category_details1:
                gigs_details = UserGigs.objects.filter(gig_sub_category =sub_gig_cat, gig_status='active').exclude(user_id__profile_status="blocked")     
        elif(len(gig_sub_category_details2)!=0):
            for sub_gig_cat in gig_sub_category_details2:
                gigs_details = UserGigs.objects.filter(gig_sub_category =sub_gig_cat, gig_status='active').exclude(user_id__profile_status="blocked")   
        if(len(gigs_details) == 0):
            gigs_details = UserGigs.objects.filter(gig_title__icontains=keyword, gig_status='active').exclude(user_id__profile_status="blocked")
            if(len(gigs_details) ==0):
                gigs_details = UserGigs.objects.filter(query2, gig_status='active').exclude(user_id__profile_status="blocked")
                if(len(gigs_details) ==0):
                    gigs_details = UserGigs.objects.filter(gig_title = keyword, gig_status='active').exclude(user_id__profile_status="blocked")
        active_gigs_data = []
        search_gig_list = []
        for u_gig in gigs_details:
            if(str(u_gig.gig_title).strip() not in search_gig_list):
                search_gig_list.append(str(u_gig.gig_title).strip())
                gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
                if(gig_image != None):
                    gig_image_url = gig_image.gig_image
                start_price = 0
                userpack= UserGigPackages.objects.filter(package_gig_name=u_gig, package_type= 'basic').first() 
                if(userpack != None):
                    start_price = userpack.package_price
                else:
                    start_price = 0 
                seller_reviews = Seller_Reviews.objects.filter(package_gig_name= u_gig)
                seller_count = 0
                for s_review in seller_reviews:
                    seller_count = seller_count + float(s_review.average_val)
                try:
                    seller_count = round(float(seller_count/len(seller_reviews)))
                except:
                    seller_count = 0  
                active_gigs_data.append({"gig_title":u_gig.gig_title, "gig_img_url":gig_image_url,"start_price":start_price,"seller_count":seller_count,"review_count":len(seller_reviews),"gig_username":u_gig.user_id.username, "gig_gig_img":u_gig.user_id.avatar,"gig_seller_level":u_gig.user_id.user_level.level_name})
        return render(request , 'search_gig.html',{"active_gigs":active_gigs_data,"keyword":keyword})


class search_profile_view(View):
    return_url = None
    def get(self , request,keyword=''):
        user_details_li= []
        ipAddress = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipAddress = x_forwarded_for.split(',')[0]
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(ipAddress),search_types="user")
            search_term.save()
        else:   
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(ipAddress),search_types="user")
            search_term.save()
        user_details = User.objects.filter(username__icontains=keyword).exclude(profile_status="blocked")
        for u in user_details:
            country_flag_icon = '/static/assets/images/flags/'+ u.country.code.lower()+ '.svg'
            seller_reviews = Seller_Reviews.objects.filter(s_review_to=u).count()
            user_details_li.append({"username":u.username,"user_level":u.user_level.level_name,"country":u.country.name,"profile_img":u.avatar,"c_flag":country_flag_icon, "u_ratings":seller_reviews})
        return render(request , 'search_user.html',{"keyword":keyword,"user_details":user_details_li})

def logout_social(request):
    logout(request)
    return redirect('index')
    

class seller_main_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"seller"
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(userDetails.pay_pal_mail_id != None):
                    s_active_orders = []
                    s_delivered_orders = []
                    s_completed_orders = []
                    s_cancelled_orders = []
                    active_earnings = 0
                    active_rate = 0
                    delivered_rate = 0
                    completed_rate = 0
                    total_orders = User_orders.objects.filter(order_to = userDetails).count()
                    s_active_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "active")
                    s_delivered_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "delivered")
                    s_completed_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "completed")
                    s_cancelled_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "cancel")
                    for a_order in s_active_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        order_status = ''
                        due_in_str = ''
                        active_earnings = float(active_earnings) + float(a_order.order_amount)
                        due_date = ''
                        try:
                            due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S.%f")
                        except:
                            due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S")
                        end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        diff = relativedelta.relativedelta(due_date, end_date)
                        num = int(diff.days)
                        num1 = int(diff.hours)
                        if num > 0:
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        elif num == 0:
                            if(num1 > 0):
                                order_status = "progress"
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                            else:
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                                order_status = "late"
                                formatted_due_date = "failed" 
                        s_active_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"order_price":a_order.order_amount,"delivery_time":due_in_str,"del_satus":order_status,"order_id":a_order.order_no})
                    for a_order in s_delivered_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        s_delivered_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"order_price":a_order.order_amount,"del_satus":"Delivered","order_id":a_order.order_no})
                    for a_order in s_completed_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        s_completed_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"order_price":a_order.order_amount,"del_satus":"Completed","order_id":a_order.order_no})
                    for a_order in s_cancelled_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        s_cancelled_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"order_price":a_order.order_amount,"del_satus":"Cancelled","order_id":a_order.order_no})
                    try:
                        active_per = round(float(len(s_active_orders_detls)/total_orders)*100,2)
                    except:
                        active_per = 0
                    try:
                        delivered_per = userDetails.avg_delivery_time
                    except:
                        delivered_per = 0
                    try:
                        completed_per = round(float(len(s_completed_orders_detls)/total_orders)*100,2)
                    except:
                        completed_per = 0
                    return render(request , 'Dashboard/seller_dashboard.html',{"active_orders":s_active_orders,"delivered_orders":s_delivered_orders,"completed_orders":s_completed_orders,"cancelled_orders":s_cancelled_orders,"Active_earning":active_earnings,"resp_time":userDetails.avg_respons,"this_earning":userDetails.current_month_earning,"active_per":active_per,"delivered_per":delivered_per,"completed_per":completed_per})
                else:
                    return redirect('account_settings') 
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class offers_view(View):
    return_url = None
    def get(self , request,username='',req_id=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    buyer_offers_li = []
                    buyer_request = Buyer_Post_Request.objects.get(buyer_request_id= req_id)
                    buyer_offers = Request_Offers.objects.filter(buyer_request= buyer_request, offer_type= "request", offer_status_by_buyer='active')
                    for b_o in buyer_offers:
                        gig_details = UserGigs.objects.get(gig_title = b_o.gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        seller_reviews = Seller_Reviews.objects.filter(package_gig_name= gig_details)
                        seller_count = 0
                        for s_review in seller_reviews:
                            seller_count = seller_count + float(s_review.average_val)
                        try:
                            seller_count = round(float(round(seller_count/len(seller_reviews),0)))
                        except:
                            seller_count = 0
                        user_details_off = User.objects.get(username = b_o.user_id.username)
                        seller_levl = str(user_details_off.user_level.level_name)
                        json_data = ''
                        if(len(b_o.extra_parameters)):
                            json_data = json.loads(b_o.extra_parameters)
                        else:
                            json_data = ''
                        buyer_offers_li.append({"buyer_username":b_o.user_id.username,"buyer_image":b_o.user_id.avatar,"gig_id":b_o.gig_name.id,"gig_title":b_o.gig_name.gig_title ,"gig_image":gig_image_url,"seller_reviews":seller_count,"offer_desc":b_o.offer_desc,"offer_price":b_o.offer_budget,"offer_time":b_o.offer_time,"seller_level":seller_levl,"offer_date":str(b_o.offer_date),"offer_id":b_o.id,"offer_data":json_data})
                    return render(request , 'Dashboard/offers.html',{"buyer_request":buyer_request,"offers":buyer_offers_li})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
    
class payments_view(View):
    return_url = None
    def get(self , request,req_id='',offer_id=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                gigdetails_list = []
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                buyer_req_details = []
                service_fees_perc = 0
                service_fees_flat = 0
                try:
                    buyer_req_details = Buyer_Post_Request.objects.get(buyer_request_id= req_id)
                except: 
                    buyer_req_details = []
                offer_details = Request_Offers.objects.get(pk= offer_id)
                service_fees = 0
                gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
                imp_gig_image_url = ''
                imp_gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                if(imp_gig_image != None):
                    imp_gig_image_url = imp_gig_image.gig_image 
                service_fees_price = 0
                serv_fees_type = ''
                serv_fees_val = ''
                service_fees_params = Payment_Parameters.objects.filter(Q(parameter_name="Buyer service Fees"))
                for s_p in service_fees_params:
                    if(s_p.service_amount == "40"):
                        service_fees_flat = s_p.service_fees
                    elif(s_p.service_amount == "41"):
                        service_fees_perc = s_p.service_fees
                if(int(offer_details.offer_budget) < 40):
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Buyer service Fees", service_amount="40"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  int(serv_fees_val)
                        else:
                            perceof_budg = float((int(offer_details.offer_budget)* int(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                else:
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Buyer service Fees", service_amount="41"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  int(serv_fees_val)
                        else:
                            perceof_budg = float((int(offer_details.offer_budget)* int(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                gigdetails_list.append({"gig_title":gig_details.gig_title,"gig_image":imp_gig_image_url,"offer_price": round(float(offer_details.offer_budget),2),"offer_revisions":offer_details.no_revisions,"offer_time":offer_details.offer_time,"service_fees":service_fees_price,"total_amount":round(float((float(offer_details.offer_budget)+ float(service_fees_price))),2),"tax_ref_name":gig_details.user_id.username + "_ref_user","pay_to_user":gig_details.user_id.username,"pay_to_user_email":gig_details.user_id.email,"offer_id":offer_details.id,"serv_fees_type":serv_fees_type,"serv_fees_val":serv_fees_val})
                base_url = request.build_absolute_uri("/")
                extra_gigs = UserExtra_gigs.objects.filter(package_gig_name=gig_details)
                extra_delivery_pack_name = ""
                package_priceList = []
                gig_packages = UserGigPackages.objects.filter(package_gig_name=gig_details)
                if(UserGigPackages.objects.filter(package_gig_name=gig_details).count() > 1):
                    for g_pack in gig_packages:
                        pack_price = int(g_pack.package_price)
                        package_priceList.append(pack_price)
                    bisect_val = bisect.bisect(package_priceList, int(offer_details.offer_budget)) 
                    if(int(bisect_val) == 1):
                        extra_delivery_pack_name = "basic" 
                    elif(int(bisect_val) == 2):
                        extra_delivery_pack_name = "standard" 
                    elif(int(bisect_val) == 3):
                        extra_delivery_pack_name = "enterprise" 
                    elif(int(bisect_val) == 0):
                        extra_delivery_pack_name = "basic"                                   
                else:
                    extra_delivery_pack_name = "basic"
                extra_delivery_dDetails= ''
                try:
                    extra_delivery_dDetails = UserGig_Extra_Delivery.objects.get(package_type=extra_delivery_pack_name,package_gig_name=gig_details)
                except:
                    extra_delivery_dDetails = ''
                api_details = Api_keys.objects.filter(Q(api_name="paypal") | Q(api_name= "flutterwave"))
                paypal_client_id = ''
                flutter_client_id = ''
                for api in api_details:
                    if(api.api_name == "paypal"):
                        paypal_client_id = api.private_key
                    elif(api.api_name == "flutterwave"):
                        flutter_client_id = api.private_key
                available_credit = float(float(userDetails.avail_bal) + float(userDetails.availcredit_bal))
                return render(request , 'Dashboard/payments.html',{"buyer_req_id":req_id,"offer_details":offer_details,"gig_details":gigdetails_list,"base_url":base_url,"extra_gigs":extra_gigs,"flutterwave_client_id":flutter_client_id,"paypal_client_id":paypal_client_id,"available_credit":available_credit,"service_fees_per":service_fees_perc, "service_fees_flat":service_fees_flat,"gig_extra_delivery":extra_delivery_dDetails})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
                        
        
    
class requirements_p_view(View):
    return_url = None
    def get(self , request,offer_id="",pay_id="",pay_email="",trans_id="",pay_status="",base_price=0,total_price=0,service_fee=0,pay_to='',extra_gig='',credits_used=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                pay_user = User.objects.get(username = pay_to)
                try:
                    offer_details = Request_Offers.objects.get(id= offer_id ,user_id = pay_user )
                except:
                    offer_details = Request_Offers.objects.get(id= offer_id ,custom_user = pay_user )
                gig_requirements = []
                charcterlimits = []
                gig_details = []
                gig_req_ans_char = 0
                gig_id_str = 0
                if(offer_details.ask_requirements == True):
                    gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
                    gig_id_str = int(gig_details.id)
                    userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                    gig_requirements = Usergig_requirement.objects.filter(package_gig_name=gig_details )
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "gig_requirements_ans"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "gig_requirements_ans"):
                            gig_req_ans_char = c.Max_No_of_char_allowed           
                else:
                    gig_id_str = 0
                return render(request , 'Dashboard/get_requirements_paypal.html',{"offer_id":offer_id,"gig_requirements":gig_requirements,"req_ans_char":gig_req_ans_char,"gig_id":gig_id_str})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class requirements_f_view(View):
    return_url = None
    def get(self , request,offer_id="",base_price=0,total_price=0,service_fee=0,pay_to='',extra_gig=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                pay_user = User.objects.get(username = pay_to)
                try:
                    offer_details = Request_Offers.objects.get(id= offer_id ,user_id = pay_user )
                except:
                    offer_details = Request_Offers.objects.get(id= offer_id ,custom_user = pay_user )
                gig_requirements = []
                charcterlimits = []
                gig_details = []
                gig_req_ans_char = 0
                gig_id_str = 0
                if(offer_details.ask_requirements == True):
                    gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
                    gig_id_str = int(gig_details.id)
                    userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                    gig_requirements = Usergig_requirement.objects.filter(package_gig_name=gig_details)
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "gig_requirements_ans"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "gig_requirements_ans"):
                            gig_req_ans_char = c.Max_No_of_char_allowed
                else:
                    gig_id_str = 0
                return render(request , 'Dashboard/get_requirements_flutter.html',{"offer_id":offer_id,"base_price":base_price,"total_price":total_price,"service_fee":service_fee,"gig_requirements":gig_requirements,"req_ans_char":gig_req_ans_char,"gig_id":gig_id_str})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')



class requirements_c_view(View):
    return_url = None
    def get(self , request,offer_id="",base_price=0,total_price=0,fees=0,extra_gigs='',used_credits='',pay_to='',pay_by=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                pay_user = User.objects.get(username = pay_to)
                try:
                    offer_details = Request_Offers.objects.get(id= offer_id ,user_id = pay_user )
                except:
                    offer_details = Request_Offers.objects.get(id= offer_id ,custom_user = pay_user )
                gig_requirements = []
                charcterlimits = []
                gig_details = []
                gig_req_ans_char = 0
                gig_id_str = 0
                if(offer_details.ask_requirements == True):
                    gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
                    gig_id_str = int(gig_details.id)
                    userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                    gig_requirements = Usergig_requirement.objects.filter(package_gig_name=gig_details)
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "gig_requirements_ans"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "gig_requirements_ans"):
                            gig_req_ans_char = c.Max_No_of_char_allowed
                else:
                    gig_id_str = 0
                return render(request , 'Dashboard/get_requirements_credit.html',{"offer_id":offer_id,"base_price":base_price,"total_price":total_price,"service_fee":fees,"gig_requirements":gig_requirements,"req_ans_char":gig_req_ans_char,"gig_id":gig_id_str})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class Manage_request_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    active_request = []
                    pending_request = []
                    rejected_request = []
                    paused_request = []
                    active_request_obj = Buyer_Post_Request.objects.filter(service_status="active", user_id=userDetails,service_type='all')
                    pending_request_obj = Buyer_Post_Request.objects.filter(service_status="pending", user_id=userDetails,service_type='all')
                    paused_request_obj = Buyer_Post_Request.objects.filter(service_status="paused", user_id=userDetails,service_type='all')
                    rejected_request_obj = Buyer_Post_Request.objects.filter(service_status="rejected" , user_id=userDetails,service_type='all')
                    for a_req in active_request_obj:
                        acti_offers_count = Request_Offers.objects.filter(buyer_request=a_req, offer_status_by_buyer='active').count()
                        service_time_str= ''
                        if(a_req.service_time== "24hours"):
                            service_time_str = "24 Hours"
                        elif(a_req.service_time== "3days"):
                            service_time_str = "3 Days"
                        elif(a_req.service_time== "7days"):
                            service_time_str = "7 Days"
                        elif(a_req.service_time== "other"):
                            service_time_str = "Other"
                        active_request.append({"service_desc":a_req.service_desc,"service_images":a_req.service_images,"service_time":service_time_str,"service_budget":a_req.service_budget,"service_date":a_req.service_date,"offers_count":acti_offers_count,"buyer_req_id":a_req.buyer_request_id,"req_id":a_req.pk})
                    for a_req in pending_request_obj:
                        service_time_str= ''
                        if(a_req.service_time== "24hours"):
                            service_time_str = "24 Hours"
                        elif(a_req.service_time== "3days"):
                            service_time_str = "3 Days"
                        elif(a_req.service_time== "7days"):
                            service_time_str = "7 Days"
                        elif(a_req.service_time== "other"):
                            service_time_str = "Other"
                        acti_offers_count = Request_Offers.objects.filter(buyer_request=a_req, offer_status_by_buyer='active').count()
                        pending_request.append({"service_desc":a_req.service_desc,"service_images":a_req.service_images,"service_time":service_time_str,"service_budget":a_req.service_budget,"service_date":a_req.service_date,"offers_count":acti_offers_count,"buyer_req_id":a_req.buyer_request_id,"req_id":a_req.pk})
                    for a_req in paused_request_obj:
                        service_time_str= ''
                        if(a_req.service_time== "24hours"):
                            service_time_str = "24 Hours"
                        elif(a_req.service_time== "3days"):
                            service_time_str = "3 Days"
                        elif(a_req.service_time== "7days"):
                            service_time_str = "7 Days"
                        elif(a_req.service_time== "other"):
                            service_time_str = "Other"
                        acti_offers_count = Request_Offers.objects.filter(buyer_request=a_req, offer_status_by_buyer='active').count()
                        paused_request.append({"service_desc":a_req.service_desc,"service_images":a_req.service_images,"service_time":service_time_str,"service_budget":a_req.service_budget,"service_date":a_req.service_date,"offers_count":acti_offers_count,"buyer_req_id":a_req.buyer_request_id,"req_id":a_req.pk})
                    for a_req in rejected_request_obj:
                        service_time_str= ''
                        if(a_req.service_time== "24hours"):
                            service_time_str = "24 Hours"
                        elif(a_req.service_time== "3days"):
                            service_time_str = "3 Days"
                        elif(a_req.service_time== "7days"):
                            service_time_str = "7 Days"
                        elif(a_req.service_time== "other"):
                            service_time_str = "Other"
                        acti_offers_count = Request_Offers.objects.filter(buyer_request=a_req, offer_status_by_buyer='active').count()
                        rejected_request.append({"service_desc":a_req.service_desc,"service_images":a_req.service_images,"service_time":service_time_str,"service_budget":a_req.service_budget,"service_date":a_req.service_date,"offers_count":acti_offers_count,"buyer_req_id":a_req.buyer_request_id,"req_id":a_req.pk})
                    active_request.sort(key=operator.itemgetter('service_date'),reverse=True)
                    pending_request.sort(key=operator.itemgetter('service_date'),reverse=True)
                    paused_request.sort(key=operator.itemgetter('service_date'),reverse=True)
                    rejected_request.sort(key=operator.itemgetter('service_date'),reverse=True)
                    return render(request , 'Dashboard/manage_request.html',{"active_request":active_request,"pending_request":pending_request,"rejected_request":rejected_request,"paused_request":paused_request})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class post_request_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "post_request_desc"))
                    available_char = 0
                    post_request_char = 0
                    min_selling_price = 0
                    for c in charcterlimits:
                        if(c.Char_category_Name == "post_request_desc"):
                            post_request_char = c.Max_No_of_char_allowed
                    categories = Categories.objects.all()
                    resolution_ext = Addon_Parameters.objects.filter(Q(parameter_name="min_starting_price") )
                    for ext in resolution_ext:
                        if(ext.parameter_name == "min_starting_price"):
                            min_selling_price = ext.no_of_days
                    return render(request , 'Dashboard/post_request.html',{"character_post_request":int(post_request_char),"categories":categories,"minimum_selling_price":min_selling_price})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        

class billing_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                user_trans = User_Transactions.objects.filter(paid_by=userDetails)
                category_list = []
                category_Names = []
                for tran in user_trans:
                    if str(tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name).strip() not in category_Names:
                        category_Names.append(str(tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name).strip())
                        category_list.append({"cat_id":tran.offer_id.gig_name.gig_sub_category.id,"cat_name":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name})
                all_withdrawals = Withdrwal_initiated.objects.filter(user_id = userDetails)
                return render(request , 'Dashboard/billing.html',{"avail_bal": int(round(float(userDetails.availcredit_bal))),"earning_bal": round(float((float(userDetails.avail_bal))),2),"cancel_bal": round(float((float(userDetails.cancelled_earning))),2),"cat_lists":category_list,"balance_used":round(float((float(userDetails.refund_credits_used_amount))),2),"withdrawal_list":all_withdrawals})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class inbox_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                all_conversations = Conversation.objects.filter(Q(initiator=userDetails) | Q(receiver= userDetails))
                conversation_lists = []
                for all_c in all_conversations:
                    receiver_name = ''
                    last_messages = Message.objects.filter(conversation_id= all_c).last()
                    if(last_messages != None):
                        lastmessage_str = last_messages.text
                        last_message_sender = last_messages.sender.username
                        last_message_receiver = last_messages.receiver.username
                    else:
                        lastmessage_str = ''
                        last_message_sender = ''
                        last_message_receiver = ''
                    if(all_c.convers_type == "active"):
                        if(userDetails.username == all_c.initiator.username):
                            conversation_lists.append({"user_Name":all_c.receiver.username,'user_receName':all_c.initiator.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.receiver.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_receiver":last_message_receiver})
                        else:
                            conversation_lists.append({"user_Name":all_c.initiator.username,'user_receName':all_c.receiver.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.initiator.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_receiver":last_message_receiver})
                inbox_char = 0
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "inbox_message"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "inbox_message"):
                        inbox_char = c.Max_No_of_char_allowed  
                chat_words = list(ChatWords.objects.order_by().values_list('name').distinct())
                chat_words_5_words = list(ChatWords.objects.order_by().values_list('name').distinct())[:5]
                delivery_time = Parameter.objects.filter(Q(parameter_name="delivery_time"))
                no_revisions = Parameter.objects.filter(Q(parameter_name="no_revisions"))
                offer_description = 0
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="offer_description"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "offer_description"):
                        offer_description = c.Max_No_of_char_allowed 
                min_selling_price = 0
                resolution_ext = Addon_Parameters.objects.filter(Q(parameter_name="min_starting_price") )
                for ext in resolution_ext:
                    if(ext.parameter_name == "min_starting_price"):
                        min_selling_price = ext.no_of_days
                return render(request , 'Dashboard/chat.html',{"all_contacts":conversation_lists,"inbox_char":inbox_char,"chat_words":json.dumps(chat_words),"five_chat_words":json.dumps(chat_words_5_words),"delivery_time":delivery_time, "no_revisions":no_revisions,"offer_description":offer_description,"min_price":min_selling_price})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
    
class buyer_review_view(View):
    return_url = None
    def get(self , request,order_no=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                previous_page = request.META.get('HTTP_REFERER')
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "buyer_review"))
                buyer_char = 0
                for c in charcterlimits:
                    if(c.Char_category_Name == "buyer_review"):
                        buyer_char = c.Max_No_of_char_allowed
                order_details = User_orders.objects.get(order_no= order_no)
                return render(request , 'Dashboard/buyer_review.html',{"previous_page":previous_page,"order_no":order_no,"buyer_descp_count":buyer_char,"order_details":order_details})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class seller_review_view(View):
    return_url = None
    def get(self , request,order_no=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                previous_page = request.META.get('HTTP_REFERER')
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "seller_review"))
                seller_char = 0
                for c in charcterlimits:
                    if(c.Char_category_Name == "seller_review"):
                        seller_char = c.Max_No_of_char_allowed
                serv_fees_val = ''
                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Buyer Fees")).first()
                serv_fees_val = payment_parameters.service_fees
                api_details = Api_keys.objects.filter(Q(api_name="paypal") | Q(api_name= "flutterwave"))
                paypal_client_id = ''
                flutter_client_id = ''
                for api in api_details:
                    if(api.api_name == "paypal"):
                        paypal_client_id = api.private_key
                    elif(api.api_name == "flutterwave"):
                        flutter_client_id = api.private_key
                available_credit = float(float(userDetails.avail_bal) + float(userDetails.availcredit_bal))
                order_details = User_orders.objects.get(order_no= order_no)
                base_url = request.build_absolute_uri('/ref')
                return render(request , 'Dashboard/seller_review.html',{"previous_page":previous_page,"order_no":order_no,"seller_descp_count":seller_char,"serv_fees_val":serv_fees_val,"paypal_client_id":paypal_client_id,"flutterwave_client_id":flutter_client_id,"userDetails":userDetails,"available_credit":available_credit,"order_details":order_details,"base_url":base_url})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
    
class warning_review_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                get_warning = User_warning.objects.get(user_id = userDetails , confirmed_status= False)
                warning_count =  User_warning.objects.filter(user_id = userDetails).count()
                previous_page = request.META.get('HTTP_REFERER')
                warning_count_text = ""
                if(warning_count == 4):
                    userDetails.profile_status = "blocked"
                    userDetails.save()
                    return render(request , 'Dashboard/blocked.html',{"username":username})
                else:
                    if(warning_count == 2):
                        warning_count_text = "Second"
                    elif(warning_count == 1):
                        warning_count_text = "First"
                    elif(warning_count == 3):
                        warning_count_text = "Third"
                    return render(request , 'Dashboard/warning.html',{"warning_details":get_warning,"warning_count":warning_count_text,"previous_page":previous_page})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
        
        
class flutter_thank_you_tip_view(View):
    return_url = None
    def get(self , request,username='',orderid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                order_details = User_orders.objects.get(order_no = orderid)
                offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                ordered_by_user = User.objects.get(id= order_details.order_by.id)
                ordered_to_user = User.objects.get(id= order_details.order_to.id)
                extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                current_user = ''
                if(userDetails.username.strip() == ordered_by_user.username.strip()):
                    current_user = "Buyer"
                else:
                    current_user = "Seller"
                seller_gig_details = UserGigs.objects.get(id= order_details.package_gig_name.id)
                s_gig_list = []
                imp_gig_image_url = ''
                imp_gig_image = Usergig_image.objects.filter(package_gig_name=seller_gig_details).first() 
                if(imp_gig_image != None):
                    imp_gig_image_url = imp_gig_image.gig_image 
                order_status = ''
                due_in_str = ''
                due_date = ''
                d_days = ''
                d_hours = ''
                d_minutes = ''
                d_seconds = ''
                due_date_format = ''
                if(str(order_details.order_status) == "active"):
                    try:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(due_date_format, end_date)
                    order_due_date = order_details.due_date
                    formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                    num = int(diff.days)
                    num1 = int(diff.hours)
                    if num > 0:
                        order_status = "progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        if(num1 > 0):
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        else:
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                            order_status = "late"
                            formatted_due_date = "failed"
                    d_days = str(abs(diff.days))
                    d_hours = str(abs(diff.hours))
                    d_minutes = str(abs(diff.minutes))
                    d_seconds = str(abs(diff.seconds))
                else:
                    order_status = str(order_details.order_status)
                    d_days = 00
                    d_hours = 00
                    d_minutes = 00
                    d_seconds = 00
                    formatted_due_date = "failed"
                json_data = ''
                if(len(offer_details.extra_parameters)):
                    json_data = json.loads(offer_details.extra_parameters)
                else:
                    json_data = ''
                s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date,"offer_extra":json_data,"order_revisions":offer_details.no_revisions,"order_date":order_details.order_date})
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "resolution_text"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "resolution_text"):
                        res_char = c.Max_No_of_char_allowed
                extra_days = Parameter.objects.filter(Q(parameter_name="res_days"))
                return render(request , 'Dashboard/thankyoutip.html',{"seller_gig_details":s_gig_list,"resolution_char":res_char,"extra_days":extra_days,"seller_username":ordered_to_user.username})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')



class paypal_thank_you_tip_view(View):
    return_url = None
    def get(self , request,username='',orderid=0,payer_id='',payer_email='',transaction_id='',trans_status='',base_price='',service_fees='',total_price='',credit_used=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                order_details = User_orders.objects.get(order_no = orderid)
                offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                ordered_by_user = User.objects.get(id= order_details.order_by.id)
                ordered_to_user = User.objects.get(id= order_details.order_to.id)
                extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                current_user = ''
                if(userDetails.username == ordered_by_user.username):
                    current_user = "Buyer"
                else:
                    current_user = "Seller"
                seller_gig_details = UserGigs.objects.get(id= order_details.package_gig_name.id)
                s_gig_list = []
                imp_gig_image_url = ''
                imp_gig_image = Usergig_image.objects.filter(package_gig_name=seller_gig_details).first() 
                if(imp_gig_image != None):
                    imp_gig_image_url = imp_gig_image.gig_image 
                order_status = ''
                due_in_str = ''
                due_date = ''
                d_days = ''
                d_hours = ''
                d_minutes = ''
                d_seconds = ''
                due_date_format = ''
                if(str(order_details.order_status) == "active"):
                    try:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(due_date_format, end_date)
                    order_due_date = order_details.due_date
                    formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                    num = int(diff.days)
                    num1 = int(diff.hours)
                    if num > 0:
                        order_status = "progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        if(num1 > 0):
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        else:
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                            order_status = "late"
                            formatted_due_date = "failed"
                    d_days = str(abs(diff.days))
                    d_hours = str(abs(diff.hours))
                    d_minutes = str(abs(diff.minutes))
                    d_seconds = str(abs(diff.seconds))
                else:
                    order_status = str(order_details.order_status)
                    d_days = 00
                    d_hours = 00
                    d_minutes = 00
                    d_seconds = 00
                    formatted_due_date = "failed"
                json_data = ''
                if(len(offer_details.extra_parameters)):
                    json_data = json.loads(offer_details.extra_parameters)
                else:
                    json_data = ''
                s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date,"offer_extra":json_data,"order_revisions":offer_details.no_revisions,"order_date":order_details.order_date})
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "resolution_text"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "resolution_text"):
                        res_char = c.Max_No_of_char_allowed
                extra_days = Parameter.objects.filter(Q(parameter_name="res_days"))
                return render(request , 'Dashboard/thankyoutip.html',{"seller_gig_details":s_gig_list,"resolution_char":res_char,"extra_days":extra_days,"seller_username":ordered_to_user.username})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class tips_view(View):
    return_url = None
    def get(self , request,username='',orderid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                order_details = User_orders.objects.get(order_no = orderid)
                offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                ordered_by_user = User.objects.get(id= order_details.order_by.id)
                ordered_to_user = User.objects.get(id= order_details.order_to.id)
                extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                current_user = ''
                if(userDetails.username == ordered_by_user.username):
                    current_user = "Buyer"
                else:
                    current_user = "Seller"
                seller_gig_details = UserGigs.objects.get(id= order_details.package_gig_name.id)
                s_gig_list = []
                imp_gig_image_url = ''
                imp_gig_image = Usergig_image.objects.filter(package_gig_name=seller_gig_details).first() 
                if(imp_gig_image != None):
                    imp_gig_image_url = imp_gig_image.gig_image 
                order_status = ''
                due_in_str = ''
                due_date = ''
                d_days = ''
                d_hours = ''
                d_minutes = ''
                d_seconds = ''
                due_date_format = ''
                if(str(order_details.order_status) == "active"):
                    try:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(due_date_format, end_date)
                    order_due_date = order_details.due_date
                    formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                    num = int(diff.days)
                    num1 = int(diff.hours)
                    if num > 0:
                        order_status = "progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        if(num1 > 0):
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        else:
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                            order_status = "late"
                            formatted_due_date = "failed"
                    d_days = str(abs(diff.days))
                    d_hours = str(abs(diff.hours))
                    d_minutes = str(abs(diff.minutes))
                    d_seconds = str(abs(diff.seconds))
                else:
                    order_status = str(order_details.order_status)
                    d_days = 00
                    d_hours = 00
                    d_minutes = 00
                    d_seconds = 00
                    formatted_due_date = "failed"
                json_data = ''
                if(len(offer_details.extra_parameters)):
                    json_data = json.loads(offer_details.extra_parameters)
                else:
                    json_data = ''
                s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date,"offer_extra":json_data,"order_revisions":offer_details.no_revisions,"order_date":order_details.order_date})
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "resolution_text"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "resolution_text"):
                        res_char = c.Max_No_of_char_allowed
                extra_days = Parameter.objects.filter(Q(parameter_name="res_days"))
                previous_page = request.META.get('HTTP_REFERER')
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "seller_review"))
                seller_char = 0
                for c in charcterlimits:
                    if(c.Char_category_Name == "seller_review"):
                        seller_char = c.Max_No_of_char_allowed
                serv_fees_val = ''
                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Buyer Fees")).first()
                serv_fees_val = payment_parameters.service_fees
                api_details = Api_keys.objects.filter(Q(api_name="paypal") | Q(api_name= "flutterwave"))
                paypal_client_id = ''
                flutter_client_id = ''
                for api in api_details:
                    if(api.api_name == "paypal"):
                        paypal_client_id = api.private_key
                    elif(api.api_name == "flutterwave"):
                        flutter_client_id = api.private_key
                available_credit = float(float(userDetails.avail_bal) + float(userDetails.availcredit_bal))
                base_url = request.build_absolute_uri('/')
                return render(request , 'Dashboard/tips.html',{"seller_gig_details":s_gig_list,"resolution_char":res_char,"extra_days":extra_days,"seller_username":ordered_to_user.username,"previous_page":previous_page,"order_no":orderid,"seller_descp_count":seller_char,"serv_fees_val":serv_fees_val,"paypal_client_id":paypal_client_id,"flutterwave_client_id":flutter_client_id,"userDetails":userDetails,"available_credit":available_credit,"order_details":order_details,"base_url":base_url})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class credit_thank_you_tip_view(View):
    return_url = None
    def get(self , request,username='',orderid=0,payer_id='',base_price='',service_fees='',total_price='',credit_used=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                order_details = User_orders.objects.get(order_no = orderid)
                offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                ordered_by_user = User.objects.get(id= order_details.order_by.id)
                ordered_to_user = User.objects.get(id= order_details.order_to.id)
                extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                current_user = ''
                if(userDetails.username == ordered_by_user.username):
                    current_user = "Buyer"
                else:
                    current_user = "Seller"
                seller_gig_details = UserGigs.objects.get(id= order_details.package_gig_name.id)
                s_gig_list = []
                imp_gig_image_url = ''
                imp_gig_image = Usergig_image.objects.filter(package_gig_name=seller_gig_details).first() 
                if(imp_gig_image != None):
                    imp_gig_image_url = imp_gig_image.gig_image 
                order_status = ''
                due_in_str = ''
                due_date = ''
                d_days = ''
                d_hours = ''
                d_minutes = ''
                d_seconds = ''
                due_date_format = ''
                if(str(order_details.order_status) == "active"):
                    try:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(due_date_format, end_date)
                    order_due_date = order_details.due_date
                    formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                    num = int(diff.days)
                    num1 = int(diff.hours)
                    if num > 0:
                        order_status = "progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        if(num1 > 0):
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        else:
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                            order_status = "late"
                            formatted_due_date = "failed"
                    d_days = str(abs(diff.days))
                    d_hours = str(abs(diff.hours))
                    d_minutes = str(abs(diff.minutes))
                    d_seconds = str(abs(diff.seconds))
                else:
                    order_status = str(order_details.order_status)
                    d_days = 00
                    d_hours = 00
                    d_minutes = 00
                    d_seconds = 00
                    formatted_due_date = "failed"
                extraparameters = ''
                if(len(offer_details.extra_parameters.strip()) != 0):
                    extraparameters = json.loads(offer_details.extra_parameters)
                s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date,"offer_extra":extraparameters,"order_revisions":offer_details.no_revisions,"order_date":order_details.order_date})
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "resolution_text"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "resolution_text"):
                        res_char = c.Max_No_of_char_allowed
                extra_days = Parameter.objects.filter(Q(parameter_name="res_days"))
                return render(request , 'Dashboard/thankyoutip.html',{"seller_gig_details":s_gig_list,"resolution_char":res_char,"extra_days":extra_days,"seller_username":ordered_to_user.username,"seller_username":ordered_to_user.username})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
class blocked_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    return render(request , 'Dashboard/blocked.html')
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

                


class favourites_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                fav_lists = Gig_favourites.objects.filter(user_id=userDetails)
                fav_lists_data = []
                for gig in fav_lists:
                    user_gig = UserGigs.objects.exclude(user_id__profile_status="blocked").get(gig_title= str(gig.gig_name))
                    if(user_gig != None):
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=user_gig).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        start_price = 0
                        userpack= UserGigPackages.objects.filter(package_gig_name=user_gig, package_type= 'basic').first() 
                        if(userpack != None):
                            start_price = userpack.package_price
                        else:
                            start_price = 0 
                        seller_reviews = Seller_Reviews.objects.filter(package_gig_name= user_gig)
                        seller_count = 0
                        for s_review in seller_reviews:
                            seller_count = seller_count + float(s_review.average_val)
                        try:
                            seller_count = round(float(seller_count/len(seller_reviews)))
                        except:
                            seller_count = 0  
                        fav_lists_data.append({"gig_title":gig.gig_name.gig_title, "gig_img_url":gig_image_url,"start_price":start_price,"seller_count":seller_count,"review_count":len(seller_reviews),"gig_username":user_gig.user_id.username, "gig_gig_img":user_gig.user_id.avatar,"gig_seller_level":user_gig.user_id.user_level.level_name})
                return render(request , 'Dashboard/favourites.html',{"favourite_lists":fav_lists_data})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class create_gig_view(View):
    return_url = None
    def get(self , request,username='',gigid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="gig_title") | Q(Char_category_Name= "gig_package_title") | Q(Char_category_Name= "gig_package_description")  | Q(Char_category_Name= "gig_extra_title") | Q(Char_category_Name= "gig_extra_description")  | Q(Char_category_Name= "gig_description")  | Q(Char_category_Name= "gig_faq_question")  | Q(Char_category_Name= "gig_faq_answer")  | Q(Char_category_Name= "gig_requirements_ques") | Q(Char_category_Name= "gig_requirements_ans"))
                    gig_title_char = ''
                    gig_package_title_char = ''
                    gig_package_description_char = ''
                    gig_extra_description_char = ''
                    gig_extra_title_char = ''
                    gig_description_char = ''
                    gig_faq_question_char = ''
                    gig_faq_answer_char = ''
                    gig_requirements_ques_char = ''
                    gig_requirements_ans_char = ''
                    for c in charcterlimits:
                        if(c.Char_category_Name.strip() == "gig_title"):
                            gig_title_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_package_title"):
                            gig_package_title_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_package_description"):
                            gig_package_description_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_extra_description"):
                            gig_extra_description_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_extra_title"):
                            gig_extra_title_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_description"):
                            gig_description_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_faq_question"):
                            gig_faq_question_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_faq_answer"):
                            gig_faq_answer_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_requirements_ques"):
                            gig_requirements_ques_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name.strip() == "gig_requirements_ans"):
                            gig_requirements_ans_char = c.Max_No_of_char_allowed
                        categorieslist = Categories.objects.all() 
                        delivery_time = []      
                        no_revisions = []   
                        extra_days = [] 
                        extra_time = []
                        delivery_time = Parameter.objects.filter(Q(parameter_name="delivery_time"))
                        no_revisions = Parameter.objects.filter(Q(parameter_name="no_revisions"))
                        extra_days = Parameter.objects.filter(Q(parameter_name="extra_days"))
                        extra_time = Parameter.objects.filter(Q(parameter_name="extra_time"))
                    min_selling_price = 0
                    resolution_ext = Addon_Parameters.objects.filter(Q(parameter_name="min_starting_price") )
                    for ext in resolution_ext:
                        if(ext.parameter_name == "min_starting_price"):
                            min_selling_price = ext.no_of_days
                    return render(request , 'Dashboard/create_gig.html',{"category":categorieslist,"Delivery_Time":delivery_time,"No_Revisions":no_revisions,"Extra_Days":extra_days,"Extra_Time":extra_time,"gig_title_char":gig_title_char,"gig_package_title_char":gig_package_title_char,"gig_package_description_char":gig_package_description_char,"gig_extra_description_char":gig_extra_description_char,"gig_extra_title_char":gig_extra_title_char,"gig_description_char":gig_description_char,"gig_faq_question_char":gig_faq_question_char,"gig_faq_answer_char":gig_faq_answer_char,"gig_requirements_ques_char":gig_requirements_ques_char,"gig_requirements_ans_char":gig_requirements_ans_char,"min_price":min_selling_price})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
class buyer_manage_orders_view(View):
    return_url = None
    def get(self , request,username='',gigid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                active_orders = []
                delivered_orders = []
                completed_orders = []
                cancelled_orders = []
                active_request_obj = User_orders.objects.filter(order_status="active", order_by=userDetails)
                delivered_request_obj = User_orders.objects.filter(order_status="delivered", order_by=userDetails)
                completed_request_obj = User_orders.objects.filter(order_status="completed", order_by=userDetails)
                cancelled_request_obj = User_orders.objects.filter(order_status="cancel" , order_by=userDetails)
                for a_req in active_request_obj:
                    gig_details = UserGigs.objects.get(gig_title = a_req.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    active_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"order_id":a_req.order_no,"gig_image":gig_image_url,"order_date":a_req.order_date,"order_due_date":a_req.due_date,"order_amout":a_req.order_amount,"order_status":a_req.order_status,"gig_username":gig_details.user_id.username})
                for d_req in delivered_request_obj:
                    gig_details = UserGigs.objects.get(gig_title = d_req.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    delivered_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image":gig_image_url,"order_id":d_req.order_no,"order_date":d_req.order_date,"order_due_date":d_req.due_date,"order_amout":d_req.order_amount,"order_status":d_req.order_status,"gig_username":gig_details.user_id.username})
                for c_req in completed_request_obj:
                    gig_details = UserGigs.objects.get(gig_title = c_req.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    completed_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image":gig_image_url,"order_id":c_req.order_no,"order_date":c_req.order_date,"order_due_date":c_req.due_date,"order_amout":c_req.order_amount,"order_status":c_req.order_status,"gig_username":gig_details.user_id.username})
                for ca_req in cancelled_request_obj:
                    gig_details = UserGigs.objects.get(gig_title = ca_req.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    cancelled_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image":gig_image_url,"order_id":ca_req.order_no,"order_date":ca_req.order_date,"order_due_date":ca_req.due_date,"order_amout":ca_req.order_amount,"order_status":ca_req.order_status,"gig_username":gig_details.user_id.username})
                return render(request , 'Dashboard/buyermanage_orders.html',{"active_orders":active_orders,"completed_orders":completed_orders,"delivered_orders":delivered_orders,"cancelled_orders":cancelled_orders,"resp_time":userDetails.avg_respons})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class seller_manage_orders_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"seller"
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    s_active_orders = []
                    s_delivered_orders = []
                    s_completed_orders = []
                    s_cancelled_orders = []
                    active_earnings = 0
                    active_rate = 0
                    delivered_rate = 0
                    completed_rate = 0
                    total_orders = User_orders.objects.filter(order_to = userDetails).count()
                    s_active_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "active")
                    s_delivered_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "delivered")
                    s_completed_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "completed")
                    s_cancelled_orders_detls = User_orders.objects.filter(order_to = userDetails,order_status= "cancel")
                    for a_order in s_active_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        order_status = ''
                        due_in_str = ''
                        active_earnings = float(active_earnings) + float(a_order.order_amount)
                        due_date = ''
                        try:
                            due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S.%f")
                        except:
                            due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S")
                        end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        diff = relativedelta.relativedelta(due_date, end_date)
                        num = int(diff.days)
                        num1 = int(diff.hours)
                        if num > 0:
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        elif num == 0:
                            if(num1 > 0):
                                order_status = "progress"
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                            else:
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                                order_status = "late"
                                formatted_due_date = "failed"
                        order_act_lists = []
                        orderactivities = User_Order_Activity.objects.filter(order_no=a_order,activity_type="active")
                        ordercancel = User_Order_Activity.objects.filter(order_no=a_order,activity_type="cancel").last()
                        ordercomplete = User_Order_Activity.objects.filter(order_no=a_order,activity_type="completed").last()
                        orderdelivered = User_Order_Activity.objects.filter(order_no=a_order,activity_type="delivered").last()
                        for o_act in orderactivities:
                            order_amount = 0
                            if(o_act.order_amount != None):
                                order_amount = o_act.order_amount 
                            order_act_lists.append({"order_message":o_act.order_message,"order_amount":order_amount})
                        if(orderdelivered != None):
                            order_amount = 0
                            if(orderdelivered.order_amount != None):
                                order_amount = orderdelivered.order_amount 
                            order_act_lists.append({"order_message":orderdelivered.order_message,"order_amount":0})
                        if(ordercancel != None):
                            order_amount = 0
                            if(ordercancel.order_amount != None):
                                order_amount = ordercancel.order_amount 
                            order_act_lists.append({"order_message":ordercancel.order_message,"order_amount":0})
                        if(ordercomplete != None):
                            order_amount = 0
                            if(ordercomplete.order_amount != None):
                                order_amount = ordercomplete.order_amount 
                            order_act_lists.append({"order_message":ordercomplete.order_message,"order_amount":0})       
                        s_active_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar,"due_date":a_order.due_date, "buyer_username":a_order.order_by.username, "seller_username":a_order.order_to.username,"order_price":a_order.order_amount,"delivery_time":due_in_str,"del_satus":order_status,"order_id":a_order.order_no,"order_activity":order_act_lists})
                    for a_order in s_delivered_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        order_act_lists = []
                        orderactivities = User_Order_Activity.objects.filter(order_no=a_order,activity_type="active")
                        ordercancel = User_Order_Activity.objects.filter(order_no=a_order,activity_type="cancel").last()
                        ordercomplete = User_Order_Activity.objects.filter(order_no=a_order,activity_type="completed").last()
                        orderdelivered = User_Order_Activity.objects.filter(order_no=a_order,activity_type="delivered").last()
                        for o_act in orderactivities:
                            order_amount = 0
                            if(o_act.order_amount != None):
                                order_amount = o_act.order_amount 
                            order_act_lists.append({"order_message":o_act.order_message,"order_amount":order_amount})
                        if(orderdelivered != None):
                            order_amount = 0
                            if(orderdelivered.order_amount != None):
                                order_amount = orderdelivered.order_amount 
                            order_act_lists.append({"order_message":orderdelivered.order_message,"order_amount":0})
                        if(ordercancel != None):
                            order_amount = 0
                            if(ordercancel.order_amount != None):
                                order_amount = ordercancel.order_amount 
                            order_act_lists.append({"order_message":ordercancel.order_message,"order_amount":0})
                        if(ordercomplete != None):
                            order_amount = 0
                            if(ordercomplete.order_amount != None):
                                order_amount = ordercomplete.order_amount 
                            order_act_lists.append({"order_message":ordercomplete.order_message,"order_amount":0})
                        s_delivered_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar,"due_date":a_order.due_date, "buyer_username":a_order.order_by.username, "seller_username":a_order.order_to.username,"order_price":a_order.order_amount,"del_satus":"Delivered","order_id":a_order.order_no,"order_activity":order_act_lists})
                    for a_order in s_completed_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        order_act_lists = []
                        orderactivities = User_Order_Activity.objects.filter(order_no=a_order,activity_type="active")
                        ordercancel = User_Order_Activity.objects.filter(order_no=a_order,activity_type="cancel").last()
                        ordercomplete = User_Order_Activity.objects.filter(order_no=a_order,activity_type="completed").last()
                        orderdelivered = User_Order_Activity.objects.filter(order_no=a_order,activity_type="delivered").last()
                        for o_act in orderactivities:
                            order_amount = 0
                            if(o_act.order_amount != None):
                                order_amount = o_act.order_amount 
                            order_act_lists.append({"order_message":o_act.order_message,"order_amount":order_amount})
                        if(orderdelivered != None):
                            order_amount = 0
                            if(orderdelivered.order_amount != None):
                                order_amount = orderdelivered.order_amount 
                            order_act_lists.append({"order_message":orderdelivered.order_message,"order_amount":0})
                        if(ordercancel != None):
                            order_amount = 0
                            if(ordercancel.order_amount != None):
                                order_amount = ordercancel.order_amount 
                            order_act_lists.append({"order_message":ordercancel.order_message,"order_amount":0})
                        if(ordercomplete != None):
                            order_amount = 0
                            if(ordercomplete.order_amount != None):
                                order_amount = ordercomplete.order_amount 
                            order_act_lists.append({"order_message":ordercomplete.order_message,"order_amount":0})
                        s_completed_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url, "seller_username":a_order.order_to.username,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"due_date":a_order.due_date,"order_price":a_order.order_amount,"del_satus":"Completed","order_id":a_order.order_no,"order_activity":order_act_lists})
                    for a_order in s_cancelled_orders_detls:
                        gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                        gig_image_url = ''
                        gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        order_act_lists = []
                        orderactivities = User_Order_Activity.objects.filter(order_no=a_order,activity_type="active")
                        ordercancel = User_Order_Activity.objects.filter(order_no=a_order,activity_type="cancel").last()
                        ordercomplete = User_Order_Activity.objects.filter(order_no=a_order,activity_type="completed").last()
                        orderdelivered = User_Order_Activity.objects.filter(order_no=a_order,activity_type="delivered").last()
                        for o_act in orderactivities:
                            order_amount = 0
                            if(o_act.order_amount != None):
                                order_amount = o_act.order_amount 
                            order_act_lists.append({"order_message":o_act.order_message,"order_amount":order_amount})
                        if(orderdelivered != None):
                            order_amount = 0
                            if(orderdelivered.order_amount != None):
                                order_amount = orderdelivered.order_amount 
                            order_act_lists.append({"order_message":orderdelivered.order_message,"order_amount":0})
                        if(ordercancel != None):
                            order_amount = 0
                            if(ordercancel.order_amount != None):
                                order_amount = ordercancel.order_amount 
                            order_act_lists.append({"order_message":ordercancel.order_message,"order_amount":0})
                        if(ordercomplete != None):
                            order_amount = 0
                            if(ordercomplete.order_amount != None):
                                order_amount = ordercomplete.order_amount 
                            order_act_lists.append({"order_message":ordercomplete.order_message,"order_amount":0})
                        s_cancelled_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title, "seller_username":a_order.order_to.username,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"due_date":a_order.due_date,"order_price":a_order.order_amount,"del_satus":"Cancelled","order_id":a_order.order_no,"order_activity":order_act_lists})
                    try:
                        active_per = round(float(len(s_active_orders_detls)/total_orders)*100,2)
                    except:
                        active_per = 0
                    try:
                        delivered_per = round(float(len(s_delivered_orders_detls)/total_orders)*100,2)
                    except:
                        delivered_per = 0
                    try:
                        completed_per = round(float(len(s_completed_orders_detls)/total_orders)*100,2)
                    except:
                        completed_per = 0
                    return render(request , 'Dashboard/seller_manage_orders.html',{"active_orders":s_active_orders,"delivered_orders":s_delivered_orders,"completed_orders":s_completed_orders,"cancelled_orders":s_cancelled_orders,"Active_earning":active_earnings,"resp_time":userDetails.avg_respons,"this_earning":userDetails.current_earning,"active_per":active_per,"delivered_per":delivered_per,"completed_per":completed_per})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class buyer_request_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                all_categories = []
                seller_level_offer = 0
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id) 
                seller_lvel = SellerLevels4.objects.get(level_slug= userDetails.user_level.level_slug)
                UserGigCategory = UserGigs.objects.filter(user_id= userDetails , gig_status= "active").values("gig_category").distinct()
                for g_c in UserGigCategory:
                    if(g_c["gig_category"] != None):
                        category_d = Categories.objects.get(id = g_c["gig_category"])
                        all_categories.append({"cat_Name":category_d.category_Name})
                delivery_time = []
                no_revisions = []
                delivery_time = Parameter.objects.filter(Q(parameter_name="delivery_time"))
                no_revisions = Parameter.objects.filter(Q(parameter_name="no_revisions"))
                offer_description = 0
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="offer_description"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "offer_description"):
                        offer_description = c.Max_No_of_char_allowed
                offers_sent_list = []
                offers_sent = Request_Offers.objects.filter(user_id= userDetails,offer_type='request')
                min_selling_price = 0
                resolution_ext = Addon_Parameters.objects.filter(Q(parameter_name="min_starting_price") )
                for ext in resolution_ext:
                    if(ext.parameter_name == "min_starting_price"):
                        min_selling_price = ext.no_of_days
                for off in offers_sent:
                    if(off != None):
                        service_time_str = ''
                        if(off.buyer_request.service_time== "24hours"):
                            service_time_str = "24 Hours"
                        elif(off.buyer_request.service_time== "3days"):
                            service_time_str = "3 Days"
                        elif(off.buyer_request.service_time== "7days"):
                            service_time_str = "7 Days"
                        elif(off.buyer_request.service_time== "other"):
                            service_time_str = "Other"
                        offers_sent_list.append({"gig_title":off.gig_name.gig_title,"offer_desc":off.offer_desc,"duration":off.offer_time,"price":off.offer_budget,"buyer_img":off.buyer_request.user_id.avatar,"buyer_name":off.buyer_request.user_id.username,"buyer_req_desc":off.buyer_request.service_desc,"buyer_delivery_time":service_time_str, "buyer_price":off.buyer_request.service_budget})
                return render(request , 'Dashboard/buyer_request.html',{"user_details":userDetails,"max_offers":seller_lvel.No_of_offers,"all_categories":all_categories,"delivery_time":delivery_time, "no_revisions":no_revisions,"offer_description":offer_description,"offer_sent_req":offers_sent_list,"min_price":min_selling_price})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html') 

class manage_gigs_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:    
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    activegigs = []
                    pendinggigs = []
                    modifgigs = []
                    drafgigs = []
                    deniedgigs = []
                    pausedgigs = []
                    user_gigs_details = UserGigs.objects.filter(user_id=userDetails)
                    for u_gig in user_gigs_details:
                        gig_image = Usergig_image.objects.filter(user_id=userDetails,package_gig_name=u_gig).first() 
                        if(gig_image != None):
                            gig_image_url = gig_image.gig_image
                        else:
                            gig_image_url = ''
                        last_month = datetime.today() - timedelta(days=60)
                        ugig_impressions = UserGigsImpressions.objects.filter(user_id=userDetails,gig_name=u_gig,impress_date__gte=last_month).count()
                        user_order_details = User_orders.objects.filter(order_to=userDetails,package_gig_name=u_gig).count()
                        cancelled_orders =  User_orders.objects.filter(order_to=userDetails,package_gig_name=u_gig, order_status= 'cancel').count()
                        try:
                            cancel_perc = int((cancelled_orders * 100) / (user_order_details))
                        except:
                            cancel_perc = 0
                        if(u_gig.gig_status == "active"):
                            activegigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_share_Link":u_gig.gig_share_link,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                        elif(u_gig.gig_status == "pending"):
                            pendinggigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_share_Link":u_gig.gig_share_link,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                        elif(u_gig.gig_status == "modification"):
                            modifgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_share_Link":u_gig.gig_share_link,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                        elif(u_gig.gig_status == "draft"):
                            drafgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_share_Link":u_gig.gig_share_link,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                        elif(u_gig.gig_status == "denied"):
                            deniedgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_share_Link":u_gig.gig_share_link,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                        elif(u_gig.gig_status == "paused"):
                            pausedgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_share_Link":u_gig.gig_share_link,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    return render(request , 'Dashboard/manage_gigs.html',{"active_gigs":activegigs,"pending_gigs":pendinggigs,"require_modif":modifgigs,"draft_gigs":drafgigs,"denied_gigs":deniedgigs,"paused_gigs":pausedgigs})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class earnings_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    order_details_list =  User_orders.objects.filter(Q(order_status="active" , order_to= userDetails) | Q(order_status="delivered" , order_to= userDetails))
                    earning_val = 0
                    for order_details in order_details_list:
                        if(round(float(order_details.order_amount)) < 40):
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
                    number_of_years = []
                    todays_date =  datetime.today()
                    current_year = todays_date.year
                    prev_year = int(current_year)-1
                    number_of_years.append({"year":prev_year})
                    number_of_years.append({"year":current_year})
                    mini_withdrawal = 0
                    resolution_ext = Addon_Parameters.objects.filter(Q(parameter_name="min_withdrawal_limit") )
                    for ext in resolution_ext:
                        if(ext.parameter_name == "min_withdrawal_limit"):
                            mini_withdrawal = ext.no_of_days
                    already_iniated = ""
                    initiate_count = Withdrwal_initiated.objects.filter(user_id=userDetails , initiated_type="earnings").exclude(Q(withdrawan_status="sucess")).count()
                    if(initiate_count > 0):
                        already_iniated = "yes"
                    else:
                        already_iniated = "no"
                    return render(request , 'Dashboard/earnings.html',{"user_details":userDetails,"earning_val":earning_val,"number_of_years":number_of_years,"mini_withdrawal":round(float(mini_withdrawal),2),"avail_withdrawal":round(float(userDetails.avail_bal),2),"already_initiated":already_iniated})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class order_activities_view(View):
    return_url = None
    def get(self , request,username='',orderid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                delivery  = ''
                delivery_details_list = []
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username):
                    order_details = User_orders.objects.get(order_no = orderid)
                    offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                    transaction_details = User_Transactions.objects.get(offer_id = offer_details,order_no= order_details,paid_for="order")
                    ordered_by_user = User.objects.get(id= order_details.order_by.id)
                    ordered_to_user = User.objects.get(id= order_details.order_to.id)
                    extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                    current_user = ''
                    buyer_user_name = ''
                    seller_user_name = ''
                    Order_Message.objects.filter(receiver=userDetails,is_read=False).update(is_read=True)
                    if(userDetails.username == ordered_by_user.username):
                        current_user = "Buyer"
                        buyer_price = round(float(float(transaction_details.offer_amount) + float(transaction_details.processing_fees)),2)
                        buyer_user_name = str(ordered_by_user.username)
                        seller_user_name = str(ordered_to_user.username) 
                    else:
                        current_user = "Seller"
                        buyer_price = str(transaction_details.offer_amount)
                        buyer_user_name = str(ordered_by_user.username)
                        seller_user_name = str(ordered_to_user.username)
                    seller_gig_details = UserGigs.objects.get(id= order_details.package_gig_name.id)
                    s_gig_list = []
                    imp_gig_image_url = ''
                    imp_gig_image = Usergig_image.objects.filter(package_gig_name=seller_gig_details).first() 
                    if(imp_gig_image != None):
                        imp_gig_image_url = imp_gig_image.gig_image 
                    order_status = ''
                    due_in_str = ''
                    due_date = ''
                    d_days = ''
                    d_hours = ''
                    d_minutes = ''
                    d_seconds = ''
                    due_date_format = ''
                    if(str(order_details.order_status) == "active" or str(order_details.order_status) == "delivered" ):
                        try:
                            due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                            due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                        except:
                            due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                            due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                        end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        diff = relativedelta.relativedelta(due_date_format, end_date)
                        order_due_date = order_details.due_date
                        formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                        num = int(diff.days)
                        num1 = int(diff.hours)
                        if num > 0:
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        elif num == 0:
                            if(num1 > 0):
                                order_status = "progress"
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                            else:
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                                order_status = "late"
                                formatted_due_date = "failed"                        
                        d_days = str(abs(diff.days))
                        d_hours = str(abs(diff.hours))
                        d_minutes = str(abs(diff.minutes))
                        d_seconds = str(abs(diff.seconds))
                    else:
                        order_status = str(order_details.order_status)
                        d_days = 00
                        d_hours = 00
                        d_minutes = 00
                        d_seconds = 00
                        formatted_due_date = "failed"
                    if(User_Order_Resolution.objects.filter(order_no=order_details,resolution_status="pending").exists() == True):
                        order_status = "resolution"
                    delivered = ''
                    delivery_status = ''
                    if(str(order_details.order_status) == "delivered" or str(order_details.order_status) == "completed"):
                        if(Order_Delivery.objects.filter(order_no=order_details).exists() == True):
                            delivered = "yes"
                            delivery_details = Order_Delivery.objects.filter(order_no=order_details).first()
                            if(delivery_details.delivery_status == "delivered"):
                                delivery_status = "delivered"
                            elif(delivery_details.delivery_status == "completed"):
                                delivery_status = "completed"
                            del_doc_lists = []
                            if((delivery_details.attachment) == None):
                                del_doc_lists = []
                            else:
                                img_fm = [".tif", ".tiff", ".jpg", ".jpeg", ".gif", ".png", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2", ".bmp", ".ppm", ".heif"]
                                del_doc_lists_split = delivery_details.attachment.split(",")
                                for doc in del_doc_lists_split:
                                    if(len(doc.strip()) != 0):
                                        extype = ''
                                        extension = Path(doc).suffix
                                        if(extension in img_fm):
                                            extype = "image"
                                        elif(extension == ".pdf"):
                                            extype = "pdf"
                                        elif(extension == ".zip"):
                                            extype = "zip"
                                        elif(extension == ".rar"):
                                            extype = "rar"
                                        else:
                                            extype = "doc"
                                        del_doc_lists.append({"doc":doc,"ext_type":extype,"ext":extension})
                            delivery_details_list.append({"delivery_message":delivery_details.delivery_message,"delivery_date":delivery_details.delivery_date,"delivered_by_user":delivery_details.delivered_by.username,"del_documents":del_doc_lists})
                        else:
                            delivered = "no"
                    if(str(order_details.order_status) == "delivered"):
                        order_status = "delivered"       
                    if(str(order_details.order_status) == "completed"):
                        order_status = "completed"
                    s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date})
                    requirements_lists = []
                    try:
                        conversation = Order_Conversation.objects.get(initiator=ordered_by_user,receiver=ordered_to_user)
                    except:
                        try:
                            conversation = Order_Conversation.objects.get(initiator=ordered_to_user,receiver=ordered_by_user)
                        except:
                            conv_obj = Order_Conversation(initiator=ordered_by_user,receiver=ordered_to_user,order_no=order_details)
                            conv_obj.save()
                            conversation = Order_Conversation.objects.get(initiator=ordered_by_user,receiver=ordered_to_user)
                    if(offer_details.ask_requirements == True):
                        requirements = "yes"
                        requirements_l = Buyer_Requirements.objects.filter(order_no= order_details)
                        for req_det in requirements_l:
                            doc_lists = []
                            if(len(req_det.req_documents.strip()) == 0):
                                doc_lists = []
                            else:
                                img_fm = [".tif", ".tiff", ".jpg", ".jpeg", ".gif", ".png", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2", ".bmp", ".ppm", ".heif"]
                                doc_lists_split = req_det.req_documents.split(",")
                                for doc in doc_lists_split:
                                    if(len(doc.strip()) != 0):
                                        extype = ''
                                        extension = Path(doc).suffix
                                        if(extension in img_fm):
                                            extype = "image"
                                        elif(extension == ".pdf"):
                                            extype = "pdf"
                                        else:
                                            extype = "doc"
                                        doc_lists.append({"doc":doc.replace("/media/buyer_requirements/",""),"ext_type":extype,"ext":extension})
                            requirements_lists.append({"requirement_ques":req_det.requirement_ques,"requirement_ans":req_det.requirement_ans,"default_req":req_det.default_req,"req_documents":doc_lists})
                    else:
                        requirements = "no"
                    message_char = ''  
                    delivery_char = ''
                    cancel_char = ''  
                    seller_res_char = ''
                    buyer_char = 0  
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="order_message") | Q(Char_category_Name= "delivery_description") | Q(Char_category_Name= "resolution_cancel_text") | Q(Char_category_Name= "seller_response")  | Q(Char_category_Name= "buyer_review"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "order_message"):
                            message_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name == "delivery_description"):
                            delivery_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name == "resolution_cancel_text"):
                            cancel_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name == "seller_response"):
                            seller_res_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name == "buyer_review"):
                            buyer_char = c.Max_No_of_char_allowed
                    chat_words = list(ChatWords.objects.order_by().values_list('name').distinct())
                    chat_words_5_words = list(ChatWords.objects.order_by().values_list('name').distinct())[:5]
                    buyer_review = []
                    seller_review = []
                    if(Buyer_Reviews.objects.filter(b_review_from=ordered_to_user,b_review_to=ordered_by_user,order_no=order_details).exists() == True):
                        buyer_review_det = Buyer_Reviews.objects.get(b_review_from=ordered_to_user,b_review_to=ordered_by_user,order_no=order_details)
                        average_list = []
                        for a in range(0,round(float(buyer_review_det.rating_val))):
                            average_list.append(a)
                        buyer_review.append({"review_id":buyer_review_det.id,"review_message":buyer_review_det.review_message,"average_val":average_list,"b_review_from_username":buyer_review_det.b_review_from.username,"b_review_from_img":buyer_review_det.b_review_from.avatar,"review_date":buyer_review_det.review_date,"b_review_to_username":buyer_review_det.b_review_to.username,"b_review_to_img":buyer_review_det.b_review_to.avatar})
                    else:
                        buyer_review = []
                    if(Seller_Reviews.objects.filter(s_review_from=ordered_by_user,s_review_to=ordered_to_user,order_no=order_details).exists() == True):
                        seller_review_det = Seller_Reviews.objects.get(s_review_from=ordered_by_user,s_review_to=ordered_to_user,order_no=order_details)
                        average_list = []
                        comm_list = []
                        recomm_list = []
                        serv_list = []
                        for a in range(0,round(float(seller_review_det.average_val))):
                            average_list.append(a)
                        for c in range(0,round(float(seller_review_det.communication))):
                            comm_list.append(c)
                        for r in range(0,round(float(seller_review_det.recommendation))):
                            recomm_list.append(r)
                        for s in range(0,round(float(seller_review_det.service))):
                            serv_list.append(s)
                        seller_review.append({"review_id":seller_review_det.id,"review_message":seller_review_det.review_message,"average_val":average_list,"communication":comm_list,"recommendation":recomm_list,"service":serv_list,"seller_response":seller_review_det.seller_response,"s_review_from_username":seller_review_det.s_review_from.username,"s_review_from_img":seller_review_det.s_review_from.avatar,"review_date":seller_review_det.review_date,"s_review_to_username":seller_review_det.s_review_to.username,"s_review_to_img":seller_review_det.s_review_to.avatar})
                    else:
                        seller_review = []
                    extraparameters = ''
                    if(len(offer_details.extra_parameters.strip()) != 0):
                        extraparameters = json.loads(offer_details.extra_parameters)
                    return render(request , 'Dashboard/order_activity.html',{'req_check': requirements,"delivery":delivered,"order_by":ordered_by_user,"order_to":ordered_to_user,"requirements":requirements_lists,"conversation":conversation,"seller_gig":s_gig_list,"order_details":order_details,"delivery_status":delivery_status,"current_user":current_user,"offer_details":offer_details,"delivery_details":delivery_details_list,"message_char":message_char,"delivery_char":delivery_char,"cancel_char":cancel_char,"seller_resp_char":seller_res_char,"extra_offer":extra_offer,"buyer_user_name":buyer_user_name,"seller_user_name":seller_user_name,"conversation_id":str(conversation.id),"chat_words":json.dumps(chat_words),"five_chat_words":json.dumps(chat_words_5_words),"buyer_review":buyer_review,"seller_review":seller_review,"buyer_price":buyer_price,"offer_extra":extraparameters,"buyer_descp_count":buyer_char})
                else:
                    return render(request, "404_error.html")
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
class resolution_view(View):
    return_url = None
    def get(self , request,username='',orderid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                if(username.strip() == userDetails.username.strip()):
                    order_details = User_orders.objects.get(order_no = orderid)
                    offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                    ordered_by_user = User.objects.get(id= order_details.order_by.id)
                    ordered_to_user = User.objects.get(id= order_details.order_to.id)
                    extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                    current_user = ''
                    if(userDetails.username == ordered_by_user.username):
                        current_user = "Buyer"
                    else:
                        current_user = "Seller"
                    seller_gig_details = UserGigs.objects.get(id= order_details.package_gig_name.id)
                    s_gig_list = []
                    imp_gig_image_url = ''
                    imp_gig_image = Usergig_image.objects.filter(package_gig_name=seller_gig_details).first() 
                    if(imp_gig_image != None):
                        imp_gig_image_url = imp_gig_image.gig_image 
                    order_status = ''
                    due_in_str = ''
                    due_date = ''
                    d_days = ''
                    d_hours = ''
                    d_minutes = ''
                    d_seconds = ''
                    due_date_format = ''
                    if(str(order_details.order_status) == "active"):
                        try:
                            due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                            due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                        except:
                            due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                            due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                        end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        diff = relativedelta.relativedelta(due_date_format, end_date)
                        order_due_date = order_details.due_date
                        formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                        num = int(diff.days)
                        num1 = int(diff.hours)
                        if num > 0:
                            order_status = "progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        elif num == 0:
                            if(num1 > 0):
                                order_status = "progress"
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                            else:
                                due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                                order_status = "late"
                                formatted_due_date = "failed"
                        d_days = str(abs(diff.days))
                        d_hours = str(abs(diff.hours))
                        d_minutes = str(abs(diff.minutes))
                        d_seconds = str(abs(diff.seconds))
                    else:
                        order_status = str(order_details.order_status)
                        d_days = 00
                        d_hours = 00
                        d_minutes = 00
                        d_seconds = 00
                        formatted_due_date = "failed"
                    extraparameters = ''
                    if(len(offer_details.extra_parameters.strip()) != 0):
                        extraparameters = json.loads(offer_details.extra_parameters)
                    s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_by_username":ordered_by_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date,"offer_extra":extraparameters,"order_revisions":offer_details.no_revisions,"order_date":order_details.order_date})
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "resolution_text"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "resolution_text"):
                            res_char = c.Max_No_of_char_allowed
                    extra_days = Parameter.objects.filter(Q(parameter_name="res_days"))
                    current_user = ''
                    if(userDetails.username.strip() == ordered_by_user.username.strip()):
                        current_user = "Buyer"
                    else:
                        current_user = "Seller"
                    return render(request , 'Dashboard/resolution.html',{"seller_gig_details":s_gig_list,"resolution_char":res_char,"extra_days":extra_days,"current_user":current_user})
                else:
                    return render(request ,'404_error.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class account_settings_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
                userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                userlang = []
                english_profi = ''
                userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                for lang in userlanguages:
                    if(lang.language_name.lng_Name == "English"):
                        english_profi = lang.lang_prof
                    userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})                  
                categories = Categories.objects.all()
                countrylist =[]
                for code, name in list(countries):
                    countrylist.append({"name":name,"code":code})
                characters = []
                title_char=0
                overview_char = 0
                frontend_url = request.META.get('HTTP_REFERER')
                url1 = urlparse(frontend_url)
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="account_professional_overview") | Q(Char_category_Name= "account_title"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "account_title"):
                        title_char = c.Max_No_of_char_allowed
                    elif(c.Char_category_Name == "account_professional_overview"):
                        overview_char = c.Max_No_of_char_allowed
                return render(request , 'Dashboard/account_settings.html',{"Countrylist":countrylist,"languages":languages,"profile_Details":userProfileDetails,"userlanguages":userlang,"title_char":title_char,"overview_char":overview_char,"UserDetails":userDetails,"Categories":categories,'userlangs':json.dumps(userlang),"english_prof":english_profi,"current_url":str(str(url1.scheme) +"://"  + str(url1.netloc) )})
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)            
                truefactor = ''
                try:
                    if(len(userDetails.profile_type) == 0):
                        truefactor = 'true'
                    elif(userDetails.profile_type == None):
                        truefactor = 'true'
                except:
                    truefactor = 'true'
                
                if(truefactor == 'true'):
                    ipAddress = ''
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ipAddress = x_forwarded_for.split(',')[0]
                    if(Referral_Users.objects.filter(ip_address=str(ipAddress),refferal_user=None).exists() == True):
                        user_referral = Referral_Users.objects.get(ip_address=str(ipAddress),refferal_user=None)
                        user_referral.refferal_user = userDetails 
                        user_referral.save()
                    languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
                    userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                    userlang = []
                    english_profi = ''
                    userlanguages = UserLanguages.objects.filter(user_id=userDetails)
                    for lang in userlanguages:
                        if(lang.language_name.lng_Name == "English"):
                            english_profi = lang.lang_prof
                        userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof})                  
                    categories = Categories.objects.all()
                    countrylist =[]
                    for code, name in list(countries):
                        countrylist.append({"name":name,"code":code})
                    characters = []
                    title_char=0
                    overview_char = 0
                    frontend_url = request.META.get('HTTP_REFERER')
                    url1 = urlparse(frontend_url)
                    charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="account_professional_overview") | Q(Char_category_Name= "account_title"))
                    for c in charcterlimits:
                        if(c.Char_category_Name == "account_title"):
                            title_char = c.Max_No_of_char_allowed
                        elif(c.Char_category_Name == "account_professional_overview"):
                            overview_char = c.Max_No_of_char_allowed
                    request.session['userpage'] =	"seller"
                    return render(request , 'Dashboard/account_settings.html',{"Countrylist":countrylist,"languages":languages,"profile_Details":userProfileDetails,"userlanguages":userlang,"title_char":title_char,"overview_char":overview_char,"UserDetails":userDetails,"Categories":categories,'userlangs':json.dumps(userlang),"english_prof":english_profi,"current_url":str(str(url1.scheme) +"://"  + str(url1.netloc) )})
                elif(userDetails.profile_type== "Buyer"):
                    return redirect('buyer')
                elif(userDetails.profile_type== "Seller"):
                    return redirect('seller')
                else:
                    return render(request , 'register.html')
            except:
                return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
@csrf_exempt
def save_content_view(request):
    if request.method == 'POST':
        data = ''
        try:
            ucontent = request.POST.get("ucontent")
            upageName = request.POST.get("upageName")
            htmlcontent = ''
            with open("/home/kworkuser/myprojectdir/kworkapp/templates/"+upageName + '.html', 'r') as f:
                htmlcontent = f.read()
            soup=BeautifulSoup(htmlcontent,'html.parser')
            soup.find('div',attrs={"class":"all_page"}).replace_with(ucontent)
            with open("/home/kworkuser/myprojectdir/kworkapp/templates/"+upageName + '.html', "w", encoding = 'utf-8') as file:
                file.write(html.unescape(str(soup.prettify()).replace("&lt;","<").replace("&gt;",">").replace("&nbsp;"," ").replace("&amp;","&").replace("&quot;",'"').replace("&apos;","'").replace("&cent;","¢").replace("&pound;","£").replace("&yen;","¥").replace("&euro;","€").replace("&copy;","©").replace("&reg;","®").replace("a&#769;","`").replace("a&#770;","^").replace("a&#771;","~").replace("a&#771;","~")))
            data = "sucess"
            
        except Exception as e:
            data = (str(type(e)) + str(e))
        return HttpResponse(data)


@csrf_exempt
def Imgupload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files") 
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/images/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/images/'+file_path
                urls.append(url)
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)

@csrf_exempt
def get_menus_view(request):
    if request.method == 'GET':
        umenuname = request.GET['umenuname']
        data = []
        if(umenuname == "start"):
            menulist = supportTopic.objects.filter(topic_category=None)
            for m in menulist:
                data.append({"title":str(m.support_topic_Name),"slug_name":str(m.slug),"has_child":1})
        else:
            
            suport_topic = supportTopic.objects.get(slug = umenuname)
            menulist = list(supportMapping.objects.filter(suport_topic = suport_topic))
            for m in menulist:
                child = ''
                child_topic = supportTopic.objects.get(support_topic_Name = m.map_to.support_topic_Name)
                childlist = list(supportMapping.objects.filter(suport_topic = child_topic))
                if(len(childlist) > 0):
                    child = "1"
                else:
                    child = "0"
                title_name = ''
                if str(m.map_to.support_topic_Name).find("- ") == -1:
                    title_name = m.map_to.support_topic_Name
                else:
                    title_namelist = m.map_to.support_topic_Name.split("-")
                    title_name = title_namelist[1].strip()
                data.append({"title":title_name,"slug_name":m.map_to.slug,"has_child":child})
        data.sort(key=operator.itemgetter('title'))
        return JsonResponse(data,safe=False)


@csrf_exempt
def get_menus_data_view(request):
    if request.method == 'GET':
        umenuname = request.GET['umenuname']
        data_contents = []
        try:
            suport_topic = supportTopic.objects.get(slug = umenuname)
            data1 = TopicDetails.objects.filter(topic_Name = suport_topic)
            for d in data1:
                data_contents.append({"title":d.topic_Name.support_topic_Name,"contents":d.topic_Desc})
        except:
            data_contents = []
        return JsonResponse(data_contents,safe=False)

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

@csrf_exempt
def post_contact_support_view(request):
    if request.method == 'GET':
        uemail_address = request.GET['uemail_address']
        uform_message = request.GET['uform_message']
        contact_us = Contactus(email=uemail_address,message=uform_message)
        contact_us.save()
        a_logging = AdminLogging(username="Contact User",reqst_message="Received an Contact Request from " + str(uemail_address),reqst_details=str(contact_us.pk),mail_address=uemail_address,log_type="support")
        a_logging.save()
        ticket = contact_us.id
        mail_content = """
<!doctype html>
<html lang="en-US">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>Let'sworkbedone - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
    <style type="text/css">
        a:hover {text-decoration: underline !important;}
    </style>
</head>

<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                          <a href="https://letworkbedone.com/" title="logo" target="_blank">
                            <img width="250" src="https://i.ibb.co/2ghjzv2/logo.png" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="text-align:center;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Letsworkbedone Support</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:15px;text-align:justify;">Thank you for contacting Letsworkbedone Support. Your request ("""+ticket+""") has been received and will be reviewed by our support staff.</span>
    <span style="display:inline-block; vertical-align:middle; Padding:15px;text-align:justify;"> Kindly note that our email support hours are from 8:00AM to 7:00PM (Saturday to Thursday) and we will attempt to get back to you as soon as possible during business hours.</span>
	  <span style="display:inline-block; vertical-align:middle; Padding:15px;text-align:justify;"> You can add additional comments to your request by replying to this email.</span>
	    
  </td> 
                                </tr>
							<tr style="text-align:left;">
                                   <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-bottom:5px;">Thanks,</span>
								</tr>
								<tr style="text-align:left;">
                               <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top:0px;">The Letworkbedone Team</span>
								</tr>
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:18px; margin:0 0 0;">&copy; <strong>www.letsworkbedone.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body></html>"""

        mail_contentAdmin = """
<!doctype html>
<html lang="en-US">

<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>Let'sworkbedone - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
    <style type="text/css">
        a:hover {text-decoration: underline !important;}
    </style>
</head>

<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,600|Open+Sans:300,400,600,600); font-family: 'Open Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                          <a href="https://letworkbedone.com/" title="logo" target="_blank">
                            <img width="250" src="https://i.ibb.co/2ghjzv2/logo.png" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 14px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 14px 0 rgba(0,0,0,.06);box-shadow:0 6px 14px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="text-align:center;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Contact Received From:</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style=""><span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Ticket Number :</span> """+ticket+"""</span></td> 
                                </tr>
                                <tr style="text-align:left;">
                                 <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Email Address :</span> """+uemail_address+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Message :</span> """+uform_message.capitalize()+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;">Thank you.</span>
								</tr>
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:14px; margin:0 0 0;">&copy; <strong>www.letsworkbedone.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>"""
        SendEmailAct(uemail_address,mail_content,"Letworkbedone - Contact Received")
        SendEmailAct("info@letworkbedone.com",mail_contentAdmin,"Letworkbedone - Contact Received")
        return HttpResponse('success')

def get_articles_view(request):
    if request.method == 'GET':
        data = []
        support_list = []
        article_name = request.GET['article_name']
        try:
            suport_topic = supportTopic.objects.filter(support_topic_Name__contains=article_name)
            pathlists = []
            for support in suport_topic: 
                suport_topic = supportTopic.objects.get(support_topic_Name = support.support_topic_Name)
                try:
                    data1 = TopicDetails.objects.get(topic_Name = suport_topic)
                    support_list.append(support.support_topic_Name)
                    data.append({"slug_name":support.slug,"title":data1.topic_Name.support_topic_Name,"contents":data1.topic_Desc})
                except:
                    support_list.append(support.support_topic_Name)
        except:
            data = []
            support_list = []
        return JsonResponse(data,safe=False)

def subcategories_for_category_view(request):
    if request.method == 'GET':
        category_id = request.GET['category_id']
        category = Categories.objects.get(id = category_id)
        sub_category = SubCategories.objects.filter(category_Name=category)
        tmpJson = serializers.serialize("json",sub_category)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


def post_increase_count_view(request):
    if request.method == 'GET':
        ulesson_id = request.GET['ulesson_id']
        ipAddress = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipAddress = x_forwarded_for.split(',')[0]
        uip_address = str(ipAddress)
        topic_details = LearningTopicDetails.objects.get(pk = ulesson_id)
        num_counts = 0
        if(LearningTopicCounts.objects.filter(topic_name=topic_details,ip_address=uip_address).exists() == False):
            learning_topic = LearningTopicCounts(topic_name=topic_details,ip_address=uip_address)
            learning_topic.save()
        num_counts = LearningTopicCounts.objects.filter(topic_name=topic_details).count()
    return HttpResponse(num_counts)

def get_all_categories_view(request):
    if request.method == 'GET':
        data = []
        main_categories = []
        sub_categories =[]
        all_categories = []
        category_list = Categories.objects.all()
        for category in category_list:
            category_inst = Categories.objects.get(category_Name=category.category_Name)
            main_categories.append({"category":category.category_Name})
            sub_cagetory_list = SubCategories.objects.filter(category_Name = category_inst)
            for sub_category in sub_cagetory_list:
                sub_category_inst = SubCategories.objects.get(category_Name=category_inst, sub_category_Name = sub_category.sub_category_Name)
                sub_sub_cagetory_list = SubSubCategories.objects.filter(category_Name = category_inst,sub_category_Name= sub_category_inst)                    
                for sub_sub_category in sub_sub_cagetory_list:
                    all_categories.append({"category":category.category_Name,"subcategory":sub_category.sub_category_Name,"subsubcategory":sub_sub_category.sub_sub_category_Name})
                sub_categories.append({"category":category.category_Name,"subcategory": sub_category.sub_category_Name,"lengthsubmenu":len(sub_sub_cagetory_list)})
        data = {'main_menu' : json.dumps(main_categories),'sub_menu' : json.dumps(sub_categories),'sub_sub_menu' : json.dumps(all_categories)}
        return JsonResponse(json.dumps(data),safe=False)


def get_sub_categories_view(request):
    if request.method == 'GET':
        data = []
        usub_category = request.GET['sub_category']
        category = Categories.objects.get(category_Name=usub_category)
        sub_categories = SubCategories.objects.filter(category_Name=category)
        for sub_cat in sub_categories:
            data.append({'sub_cat_name':sub_cat.sub_category_Name,'sub_cat_id':sub_cat.id})
        return JsonResponse(data,safe=False)

@csrf_exempt
def Prof_image_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        userid =  request.POST.get("user_id")
        userDetails = User.objects.get(pk=userid)
        frontend_url = request.META.get('HTTP_REFERER')
        url1 = urlparse(frontend_url)
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/profile/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/profile/'+file_path
                urls.append(url)
                userDetails.avatar = url1.scheme +"://"  + url1.netloc  + url
                userDetails.save()
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)
    
@csrf_exempt
def gig_image_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        userid =  request.POST.get("user_id")
        gig_id =  request.POST.get("gig_id")
        userDetails = User.objects.get(pk=userid)
        frontend_url = request.META.get('HTTP_REFERER')
        url1 = urlparse(frontend_url)
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/gig_images/')
                file_path=fs.save(gig_id+"_"+file.name.replace(' ','_'),file) 
                url = '/media/gig_images/'+file_path
                urls.append(url)
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)


def post_user_Details_view(request):
    if request.method == 'GET':
        usercountry = request.GET['usercountry']
        userrole = request.GET['userrole']
        userterms = request.GET['userterms']
        username = request.GET['username']
        userid = request.GET['userid']
        term_val = ''
        if userterms == "true": term_val = True
        else:
            term_val = False
        userDetails = User.objects.get(pk=userid)
        userDetails.country = usercountry
        userDetails.username = username
        userDetails.terms = term_val
        userDetails.profile_type = userrole
        userDetails.save()
    return HttpResponse("success")

def post_useremail_Details_view(request):
    if request.method == 'GET':
        useremail = request.GET['useremail']
        username = request.GET['username']
        usercountry = request.GET['usercountry']
        userrole = request.GET['userrole']
        userterms = request.GET['userterms']
        userid = request.GET['userid']
        term_val = ''
        if userterms == "true": term_val = True
        else:
            term_val = False
        userDetails = User.objects.get(pk=userid)
        userDetails.email = useremail
        userDetails.username = username
        userDetails.country = usercountry
        userDetails.terms = term_val
        userDetails.profile_type = userrole
        userDetails.save()
    return HttpResponse("success")


def post_user_paypal_view(request):
    if request.method == 'GET':
        upaypal = request.GET['upaypal']
        userid = request.GET['userid']
        userDetails = User.objects.get(pk=userid)
        userDetails.pay_pal_mail_id = upaypal
        userDetails.save()
    return HttpResponse("success")


def post_user_category_view(request):
    if request.method == 'GET':
        ucategory = request.GET['ucategory']
        usubcategory = request.GET['usubcategory']
        userid = request.GET['userid']
        userDetails = User.objects.get(pk=userid)
        category_int = Categories.objects.get(id=ucategory)
        sub_category_int = SubCategories.objects.get(id=usubcategory)
        userprofile = UserProfileDetails.objects.get(user_id=userDetails)
        userprofile.main_category = category_int
        userprofile.sub_category = sub_category_int
        userprofile.save()
    return HttpResponse("success")

@csrf_exempt
def post_user_languages_view(request):
    if request.method == 'POST':
        ulanguages = request.POST['ulanguages']
        userid =  request.POST.get("userid")
        userDetails = User.objects.get(pk=userid)
        data = json.loads(ulanguages)
        UserLanguages.objects.filter(user_id=userDetails).delete()
        for d in data:
            name = d['name']
            value = d['value']
            langua_inst = Languages.objects.get(lng_slug=name)
            user_lang = UserLanguages(language_name=langua_inst,lang_prof=value,user_id=userDetails)
            user_lang.save()
    return HttpResponse("success")


def post_user_overview_view(request):
    if request.method == 'GET':
        utitle = request.GET['utitle']
        uoverview = request.GET['uoverview']
        userid = request.GET['userid']
        userDetails = User.objects.get(pk=userid)
        userprofile = UserProfileDetails.objects.get(user_id=userDetails)
        userprofile.profile_title = utitle
        userprofile.profess_overview = uoverview
        userprofile.save()
    return HttpResponse("success")



def post_create_gig_view(request):
    if request.method == 'GET':
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            try:    
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                numberof_gigs = SellerLevels4.objects.get(level_slug=str(userDetails.user_level.level_slug))
                gigs_used = 0
                gig_id = 0
                if(UserGigs.objects.filter(user_id=userDetails).exists() == True):
                    gigs_used = UserGigs.objects.filter(user_id=userDetails).count()
                if(gigs_used == int(numberof_gigs.No_of_gigs)):
                    gig_id = 0
                else:
                    user_gig_obj = UserGigs(user_id=userDetails,gig_title ="New Gig Creation " + str(gigs_used))
                    user_gig_obj.save()
                    get_gig_details = UserGigs.objects.get(pk = user_gig_obj.pk)
                    gig_iamges = Usergig_image(gig_image="	/media/gig_images/blank_gig.png" ,package_gig_name=get_gig_details ,user_id=userDetails)
                    gig_iamges.save()
                    gig_id = int(user_gig_obj.pk)
                return HttpResponse(gig_id)
            except:
                return HttpResponse('error')
        else:
            return HttpResponse('error')
        
        
def post_sub_category_details_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        select_id = request.GET['select_id']
        sub_subcatDetails = []
        try:
            category_inst = Categories.objects.get(id=select_id)
            _subcatDetails = SubSubCategories.objects.filter(category_Name= category_inst)
            for subcat in _subcatDetails:
                sub_subcatDetails.append({"cat_name":subcat.sub_sub_category_Name,"cat_id":subcat.id})
        except:
            pass
        return JsonResponse(sub_subcatDetails,safe=False)



def post_tags_category_details_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        category_id = request.GET['category_id']
        sub_category_id = request.GET['sub_category_id']
        userDetails = User.objects.get(pk=userid)
        taglist = []
        sub_category_inst = SubSubCategories.objects.get(id=sub_category_id)
        for tag in sub_category_inst.tags.all():
            taglist.append({"text":tag.name,"value":tag.name})
        category_packages = []
        extra_category_packages = []
        package_inst = Category_package_Details.objects.filter(category_name=sub_category_inst)
        for pckg in package_inst:
            category_packages.append({"package_name":pckg.display_name,"package_type":pckg.display_type,"helper_txt":pckg.helper_txt})
        extra_package_inst = Category_package_Extra_Service.objects.filter(category_name=sub_category_inst)
        for extra_pckg in extra_package_inst:
            extra_category_packages.append({"e_package_name":extra_pckg.display_name,"e_package_type":extra_pckg.display_type,"e_helper_txt":extra_pckg.helper_txt})
        responseData = {'tagsOPbj':taglist,'pckgObj':category_packages,'extraPckgObj':extra_category_packages}
        return JsonResponse(responseData,safe=False)
    
    
@csrf_exempt
def post_gig_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gigtitle = request.POST.get("u_gigtitle")
        u_gig_category = request.POST.get("u_gig_category")
        u_gig_sub_category = request.POST.get("u_gig_sub_category")
        u_gig_tags = request.POST['u_gig_tags']
        data = json.loads(u_gig_tags)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_title = u_gigtitle
        gigDetails.gig_share_link = u_gigtitle.replace(" ","-")
        gigDetails.gig_category =  Categories.objects.get(pk=u_gig_category)
        gigDetails.gig_sub_category =  SubSubCategories.objects.get(pk=u_gig_sub_category)
        gigDetails.save()
        UserGigsTags.objects.filter(gig_name=gigDetails ,user_id = userDetails).delete()
        for d in data:
            usertags = UserGigsTags(gig_tag_name= d,gig_name=gigDetails ,user_id = userDetails)
            usertags.save()
        return HttpResponse('sucess')



@csrf_exempt
def post_packages_save_view(request):
    if request.method == 'POST':
        try:
            u_gig_id = request.POST.get("u_gig_id")
            u_user_id = request.POST.get("u_user_id")
            u_package_details = request.POST['u_package_details']
            u_package_details1 = request.POST['u_package_details1']
            u_package_details2 = request.POST['u_package_details2']
            u_extra_delivery = request.POST['u_extra_delivery']
            u_extra_package_details = request.POST['u_add_on_package_details']
            u_add_on_gig = request.POST['u_add_on_gig']
            data_package_details = json.loads(u_package_details)
            data_package_details1 = json.loads(u_package_details1)
            data_package_details2 = json.loads(u_package_details2)
            data_extra_delivery = json.loads(u_extra_delivery)
            data_extra_package_details = json.loads(u_extra_package_details)
            data_add_on_gig = json.loads(u_add_on_gig)
            userDetails =  User.objects.get(pk=u_user_id)
            gigDetails =  UserGigs.objects.get(pk=u_gig_id, user_id = userDetails)
            UserGigPackages.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
            UserGigPackage_Extra.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
            UserExtra_gigs.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
            UserGig_Extra_Delivery.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
            pack_data_analysys = data_package_details[0]
            dist_keys = pack_data_analysys.keys()
            package_array = []
            for i,key in enumerate(dist_keys):
                if "pack_data_" in key:
                    package_array.append({"name":pack_data_analysys[key]["name"],"value":pack_data_analysys[key]["value"]})
            for data_packages in data_package_details:
                pack_delivery = Parameter.objects.get(parameter_value =str(data_packages["pack_duration"]),parameter_name="delivery_time")
                pack_revision = Parameter.objects.get(parameter_value =str(data_packages["pack_revision"]),parameter_name="no_revisions")
                user_gig_packages = UserGigPackages(package_type=data_packages["pack_type"],package_title=data_packages["pack_title"],package_description=data_packages["pack_description"],package_delivery=pack_delivery,package_revisions=pack_revision,package_price=data_packages["pack_price"],package_data=str(package_array),package_gig_name= gigDetails,user_id=userDetails)
                user_gig_packages.save()
            if(len(data_package_details1) != 0):
                pack_data_analysys1 = data_package_details1[0]
                dist_keys1 = pack_data_analysys1.keys()
                package_array1 = []
                for i,key in enumerate(dist_keys1):
                    if "pack_data_" in key:
                        package_array1.append({"name":pack_data_analysys1[key]["name"],"value":pack_data_analysys1[key]["value"]})
                for data_packages1 in data_package_details1:
                    pack_delivery1 = Parameter.objects.get(parameter_value =str(data_packages1["pack_duration"]),parameter_name="delivery_time")
                    pack_revision1 = Parameter.objects.get(parameter_value =str(data_packages1["pack_revision"]),parameter_name="no_revisions")
                    user_gig_packages = UserGigPackages(package_type=data_packages1["pack_type"],package_title=data_packages1["pack_title"],package_description=data_packages1["pack_description"],package_delivery=pack_delivery1,package_revisions=pack_revision1,package_price=data_packages1["pack_price"],package_data=str(package_array1),package_gig_name= gigDetails,user_id=userDetails)
                    user_gig_packages.save()
            if(len(data_package_details2) != 0):
                pack_data_analysys2 = data_package_details2[0]
                dist_keys2 = pack_data_analysys2.keys()
                package_array2 = []
                for i,key in enumerate(dist_keys2):
                    if "pack_data_" in key:
                        package_array2.append({"name":pack_data_analysys2[key]["name"],"value":pack_data_analysys2[key]["value"]})
                for data_packages2 in data_package_details2:
                    pack_delivery2 = Parameter.objects.get(parameter_value =str(data_packages2["pack_duration"]),parameter_name="delivery_time")
                    pack_revision2 = Parameter.objects.get(parameter_value =str(data_packages2["pack_revision"]),parameter_name="no_revisions")
                    user_gig_packages = UserGigPackages(package_type=data_packages2["pack_type"],package_title=data_packages2["pack_title"],package_description=data_packages2["pack_description"],package_delivery=pack_delivery2,package_revisions=pack_revision2,package_price=data_packages2["pack_price"],package_data=str(package_array2),package_gig_name= gigDetails,user_id=userDetails)
                    user_gig_packages.save() 
            for extra_delivery in data_extra_delivery:
                extra_days = Parameter.objects.get(parameter_value =str(extra_delivery["days"]),parameter_name="extra_days")
                extra_delivery_gig = UserGig_Extra_Delivery(package_type= extra_delivery["name"],delivery_in= extra_days,extra_price= extra_delivery["price"],package_gig_name= gigDetails,user_id=userDetails)
                extra_delivery_gig.save()
            user_extra_data = UserGigPackage_Extra(package_data= str(data_extra_package_details),package_gig_name= gigDetails,user_id=userDetails)
            user_extra_data.save();
            for ad_on_gig in data_add_on_gig:
                gig_extra_days = Parameter.objects.get(parameter_value =str(ad_on_gig["gig_duration"]),parameter_name="extra_days")
                extra_gig_days = UserExtra_gigs(extra_gig_title= ad_on_gig["gig_title"],extra_gig_description= ad_on_gig["gig_description"],extra_gig_price= ad_on_gig["gig_price"],extra_gig_duration=gig_extra_days,package_gig_name= gigDetails,user_id=userDetails)
                extra_gig_days.save()
            return HttpResponse('sucess')
        except Exception as e:
            return HttpResponse(str(type(e)) + str(e))

@csrf_exempt
def post_gig_desp_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gig_description = request.POST.get("u_gig_description")
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_description = u_gig_description
        gigDetails.save()
        return HttpResponse('sucess')
    
    
@csrf_exempt
def post_gig_des_faq_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_gig_description = request.POST.get("u_gig_description")
        u_gig_faq_ques = request.POST.get("u_gig_faq_ques")
        u_gig_faq_answer = request.POST.get("u_gig_faq_answer")
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        gigDetails.gig_description = u_gig_description
        gigDetails.save()
        Usergig_faq.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        user_gig_faqsobj = Usergig_faq(gig_faq_question=u_gig_faq_ques,gig_faq_answer=u_gig_faq_answer,package_gig_name= gigDetails,user_id=userDetails)
        user_gig_faqsobj.save()
        return HttpResponse('sucess')



@csrf_exempt
def post_rquirements_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_requirements = request.POST['u_requirements']
        data_requirements = json.loads(u_requirements)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        Usergig_requirement.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        for req_question in data_requirements:
            user_gig_req= Usergig_requirement(gig_req_question=req_question['name'],gig_req_ans_type="Free Text",package_gig_name= gigDetails,user_id=userDetails)
            user_gig_req.save()
        return HttpResponse('sucess')


@csrf_exempt
def post_images_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        u_images = request.POST['u_images']
        data_images = json.loads(u_images)
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        Usergig_image.objects.filter(package_gig_name=gigDetails ,user_id = userDetails).delete()
        for gig_img in data_images:
            if(len(gig_img['name'].strip()) != 0):
                user_gig_img= Usergig_image(gig_image=gig_img['name'],package_gig_name= gigDetails,user_id=userDetails)
                user_gig_img.save()
        return HttpResponse('sucess')


@csrf_exempt
def post_publish_save_view(request):
    if request.method == 'POST':
        u_gig_id = request.POST.get("u_gig_id")
        u_user_id = request.POST.get("u_user_id")
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        if(gigDetails.gig_status == "active"):
            gigDetails.gig_status = "active"
            gigDetails.save()
        else:
            gigDetails.gig_status = "pending"
            gigDetails.save()
            a_logging = AdminLogging(username=userDetails.username,reqst_details=str(gigDetails.pk),reqst_message="New Gig is ready for review, Title: " + str(gigDetails.gig_title),mail_address=userDetails.email,log_type="gig_creation")
            a_logging.save()
        return HttpResponse('sucess')

def get_gig_details_view(request):
    if request.method == 'GET':
        data = []
        u_gig_id = request.GET['u_gig_id']
        u_user_id = request.GET['u_user_id']
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=int(u_gig_id.strip()))
        if(gigDetails.gig_category != None):
            data_gig_details = []
            data_gig_details.append({"title":gigDetails.gig_title,"gig_category":str(gigDetails.gig_category.id),"gig_sub_category":str(gigDetails.gig_sub_category.id),"gig_description":gigDetails.gig_description})
            gigTags =  UserGigsTags.objects.filter(gig_name=gigDetails , user_id = userDetails)
            gigTags_tmpJson = serializers.serialize("json",gigTags)
            gigTags_tmpObj = json.loads(gigTags_tmpJson)
            gigPackages =  UserGigPackages.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            package_data = []
            extra_delivery_data = []
            extra_gigs_data = []
            for gig_package in gigPackages:
                package_data.append({"package_type":gig_package.package_type,"package_title":gig_package.package_title,"package_description":gig_package.package_description,"package_delivery":gig_package.package_delivery.parameter_value,"package_revisions":gig_package.package_revisions.parameter_value,"package_data":gig_package.package_data,"package_price":gig_package.package_price})
            gig_extra_delivery =  UserGig_Extra_Delivery.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            for gig_ex_delivery in gig_extra_delivery:
                extra_delivery_data.append({"package_type":gig_ex_delivery.package_type,"delivery_in":gig_ex_delivery.delivery_in.parameter_value,"extra_price":gig_ex_delivery.extra_price})
            gig_extra_pack =  UserGigPackage_Extra.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            gig_extra_pack_tmpJson = serializers.serialize("json",gig_extra_pack)
            gig_extra_pack_tmpObj = json.loads(gig_extra_pack_tmpJson)
            extra_gigs =  UserExtra_gigs.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            for gig_ex in extra_gigs:
                extra_gigs_data.append({"extra_gig_title":gig_ex.extra_gig_title,"extra_gig_description":gig_ex.extra_gig_description,"extra_gig_price":gig_ex.extra_gig_price,"extra_gig_duration":gig_ex.extra_gig_duration.parameter_value})
            gig_faqs =  Usergig_faq.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            gig_faqs_tmpJson = serializers.serialize("json",gig_faqs)
            gig_faqs_tmpObj = json.loads(gig_faqs_tmpJson)
            gig_requirements =  Usergig_requirement.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            gig_requirements_tmpJson = serializers.serialize("json",gig_requirements)
            gig_requirements_tmpObj = json.loads(gig_requirements_tmpJson)
            gig_image =  Usergig_image.objects.filter(package_gig_name=gigDetails , user_id = userDetails)
            gig_image_tmpJson = serializers.serialize("json",gig_image)
            gig_image_tmpObj = json.loads(gig_image_tmpJson)
            response_data = {"gig_details":json.dumps(data_gig_details), "gig_tags":gigTags_tmpObj,"gig_packages":package_data, "gig_extra_delivery":extra_delivery_data, "gig_extra_pack":gig_extra_pack_tmpObj, "extra_gigs":extra_gigs_data, "gig_faqs":gig_faqs_tmpObj, "gig_requirements":gig_requirements_tmpObj, "gig_image":gig_image_tmpObj}
        else:
            response_data = {}
        return JsonResponse(response_data,safe=False)    
     
    
def post_pause_gig_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        gig_id = request.GET['gig_id']
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gig_id , user_id = userDetails)
        gigDetails.gig_status = 'paused'
        gigDetails.save()
        return HttpResponse('sucess')

def post_delete_gig_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        gig_id = request.GET['gig_id']
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gig_id , user_id = userDetails).delete()
        return HttpResponse('sucess')
    
    
@csrf_exempt
def post_availability_view(request):
    if request.method == 'POST':
        userid = request.POST.get("userid")
        unva_from = request.POST.get("unva_from")
        unva_to = request.POST.get("unva_to")
        reason = request.POST.get("reason")
        avail_message = request.POST.get("avail_message")
        checked_new = request.POST.get("checked_new")
        userDetails =  User.objects.get(pk=userid)
        availablity =  UserAvailable.objects.filter(user_id = userDetails).delete()
        user_avail_obj = UserAvailable(available_from=unva_from,available_to=unva_to,available_mssg=avail_message,available_for_new=checked_new,available_types=reason,user_id=userDetails)
        user_avail_obj.save()
        return HttpResponse('sucess')
    
    
@csrf_exempt
def post_avail_delete_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        avail_id = request.GET['avail_id']
        userDetails =  User.objects.get(pk=userid)
        availablity =  UserAvailable.objects.filter(user_id = userDetails).delete()
        return HttpResponse('sucess')

def get_availability_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        try:
            user_avail = UserAvailable.objects.filter(user_id = userid)
            tmpJson = serializers.serialize("json",user_avail)
            tmpObj = json.loads(tmpJson)
        except:
            tmpObj = []
        return HttpResponse(json.dumps(tmpObj))
    
@csrf_exempt
def post_request_image_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files") 
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/buyer_request/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/buyer_request/'+file_path
                urls.append(url)
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)
    
    
@csrf_exempt
def post_make_fav_view(request):
    if request.method == 'POST':
        userid = request.POST.get("userid")
        gigid = request.POST.get("gigid")
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gigid , user_id = userDetails)
        add_fav = Gig_favourites(gig_name=gigDetails,user_id=userDetails)
        add_fav.save()
        favourite_Count= Gig_favourites.objects.filter(gig_name=gigDetails).count()
        return JsonResponse(favourite_Count,safe=False)

@csrf_exempt    
def post_make_unfav_view(request):
    if request.method == 'POST':
        userid = request.POST.get("userid")
        gigid = request.POST.get("gigid")
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gigid , user_id = userDetails)
        Gig_favourites.objects.filter(gig_name=gigDetails,user_id=userDetails).delete()
        favourite_Count= Gig_favourites.objects.filter(gig_name=gigDetails).count()
        return JsonResponse(favourite_Count,safe=False)



@csrf_exempt
def post_service_request_view(request):
    if request.method == 'POST':
        data = ''
        userid = request.POST.get("userid")
        profile_user = request.POST.get("profile_user")
        service_descp = request.POST.get("service_descp")
        service_images = request.POST.get("service_images")
        service_cat = request.POST.get("service_cat")
        service_sub_cat = request.POST.get("service_sub_cat")
        service_time = request.POST.get("service_time")
        service_price = request.POST.get("service_price")
        service_type = request.POST.get("service_type")
        send_to = request.POST.get("send_to")
        try:
            userDetails =  User.objects.get(pk=userid)
            category_details = Categories.objects.get(pk=service_cat)
            sub_category = SubCategories.objects.get(pk=service_sub_cat)
            if(service_type == 'individual'):
                send_to_user = User.objects.get(username=send_to)
                post_bu_req= Buyer_Post_Request(service_desc= service_descp,service_images=service_images,service_category=category_details,service_sub_category=sub_category,service_time=service_time,service_budget=service_price,user_id=userDetails,send_to=send_to_user,service_type=service_type)
                post_bu_req.save()
                get_buyer_request = Buyer_Post_Request.objects.get(pk = post_bu_req.pk)
                try:    
                    message_cover_detls = Conversation.objects.get(initiator=userDetails,receiver = send_to_user)
                except:
                    try:
                        message_cover_detls = Conversation.objects.get(initiator=send_to_user,receiver = userDetails)
                    except:
                        message_cover_detls = Conversation(initiator=userDetails,receiver = send_to_user)
                        message_cover_detls.save()
                conversational_details =   Conversation.objects.get(pk = message_cover_detls.pk)
                create_message = Message(sender=userDetails,receiver=send_to_user,text = "Great news: You received an quotation.",attachment = None,conversation_id=conversational_details,message_type = 'quote',buyer_request_id=get_buyer_request)
                create_message.save()
                noti_create = CustomNotifications(sender = userDetails, recipient=send_to_user, verb='chat',description= "Great news: You received an quotation.")
                noti_create.save()
                data = 'sucess'
            else:
                try:
                    post_bu_req= Buyer_Post_Request(service_desc= service_descp,service_images=service_images,service_category=category_details,service_sub_category=sub_category,service_time=service_time,service_budget=service_price,user_id=userDetails,service_type=service_type)
                    post_bu_req.save()
                    a_logging = AdminLogging(username=userDetails.username,reqst_message="Buyer Request is ready to view, Category: " + str(post_bu_req.service_sub_category.sub_category_Name),reqst_details=str(post_bu_req.pk),mail_address=userDetails.email,log_type="request_post")
                    a_logging.save()
                    data = 'sucess'
                except Exception as e:
                    data = (str(type(e)) + str(e))               
        except Exception as e:
            data = (str(type(e)) + str(e))  
        return HttpResponse(data)

@csrf_exempt    
def post_search_key_view(request):
    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        keyword_type = request.POST.get("keyword_type")
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(whatismyip.whatismyip()),search_types=keyword_type,user_id = userDetails )
            search_term.save()
        else:   
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(whatismyip.whatismyip()),search_types=keyword_type)
            search_term.save()
        return HttpResponse("sucess")



def get_buyer_reviews_view(request):
    if request.method == 'GET':
        sub_category = request.GET['sub_category']
        sub_category_inst = SubSubCategories.objects.get(sub_sub_category_Name= sub_category)
        all_gigs = UserGigs.objects.filter(gig_sub_category=sub_category_inst)
        data = []
        for g in all_gigs:
            buyer_revs = Buyer_Reviews.objects.filter(package_gig_name=g)
            review_date = ''
            for buyer_r in buyer_revs:
                review_date = timesince.timesince(buyer_r.review_date)  
                data.append({"message":buyer_r.review_message,"review_date":review_date,"rev_username":buyer_r.b_review_from.username,"user_profile":buyer_r.b_review_from.avatar}) 
        return JsonResponse(data,safe=False)
    
@csrf_exempt     
def add_referral_link_view(request):
    if request.method == 'GET':
        affiliate_code = request.GET['affiliate_code']
        userDetails = User.objects.get(affiliate_code=affiliate_code)
        ipAddress = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipAddress = x_forwarded_for.split(',')[0]
        ip_address = str(ipAddress)
        if(Referral_Users.objects.filter(affiliate_code=affiliate_code,ip_address=ip_address,refferal_user=None).exists() == False):
            affiliate_user = Referral_Users(affiliate_code=affiliate_code,ip_address=ip_address,user_id=userDetails)
            affiliate_user.save() 
        return HttpResponse('sucess')
    
def get_filter_gigs_details_view(request):
    if request.method == 'GET':
        category_name = request.GET['category_name']
        gig_data= []
        sub_Cat_Name = request.GET['sub_Cat_Name']
        category = SubCategories.objects.get(pk= category_name)
        if(len(sub_Cat_Name.strip()) !=0):
            subcat_inst = SubSubCategories.objects.get(sub_sub_category_Name= sub_Cat_Name)
            gig_details = UserGigs.objects.filter(gig_sub_category= subcat_inst,gig_status="active" ).exclude(user_id__profile_status ="blocked")
        else:
            cat_int = Categories.objects.get(category_Name=category.category_Name)
            gig_details = UserGigs.objects.filter(gig_category= cat_int,gig_status="active" ).exclude(user_id__profile_status ="blocked")
        for g in gig_details:
            seller_reviews = Seller_Reviews.objects.filter(package_gig_name= g)
            seller_count = 0
            for s_review in seller_reviews:
                seller_count = seller_count + float(s_review.average_val)
            try:
                seller_count = round(float(round(seller_count/len(seller_reviews),0)))
            except:
                seller_count = 0   
            userpack= UserGigPackages.objects.filter(package_gig_name=g, package_type= 'basic').first() 
            if(userpack != None):
                start_price = userpack.package_price
            else:
                start_price = 0 
            gig_image = Usergig_image.objects.filter(package_gig_name=g).first() 
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            user_tags = UserGigsTags.objects.filter(gig_name=g).values("gig_tag_name")
            user_tags_str= ''
            for tg in user_tags:
                user_tags_str = user_tags_str + ","+ tg["gig_tag_name"];
            seller_levl= str(g.user_id.user_level.level_name)
            gig_data.append({"gig_title":g.gig_title,"gig_img":gig_image_url,"gig_user_name":g.user_id.username,"gig_user_img":g.user_id.avatar,"start_price":start_price,"no_reviews":len(seller_reviews),"review_count":seller_count,"seller_level":seller_levl,"order_in_progress":g.user_id.ordersin_progress,"delivery_time":g.user_id.avg_delivery_time,"tags":user_tags_str})
        return JsonResponse(gig_data,safe=False)


@csrf_exempt
def post_delete_request_view(request):
    if request.method == 'POST':
        request_id = request.POST.get("request_id")
        Buyer_Post_Request.objects.filter(pk=request_id).delete()
        return HttpResponse("sucess")
    
    
@csrf_exempt
def post_active_request_view(request):
    if request.method == 'POST':
        request_id = request.POST.get("request_id")
        b_request = Buyer_Post_Request.objects.get(pk=request_id)
        b_request.service_status= "active"
        b_request.save()
        return HttpResponse("sucess")


@csrf_exempt
def post_pause_request_view(request):
    if request.method == 'POST':
        request_id = request.POST.get("request_id")
        b_request = Buyer_Post_Request.objects.get(pk=request_id)
        b_request.service_status= "paused"
        b_request.save()
        return HttpResponse("sucess")
    
def Average_Time(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)

def daily_routine():
    all_users = []
    all_users = User.objects.filter(is_admin=False,profile_status="active")
    for us in all_users:
        userDetails = User.objects.get(username = us.username)
        average_delivery_str = 'Within 24 hours'
        total_earning_val = 0
        current_earning_val = 0
        current_month_earning_val = 0
        cancelled_earning_val = 0
        avail_bal_val = 0
        availcredit_bal_val = 0
        affilite_earn_val = 0
        withdrawed_credit_val = 0
        with_used_credit_val = 0
        ref_used_credit_val = 0
        orders_count = User_orders.objects.filter(order_to=userDetails,order_status="active").count()
        user_orders = User_orders.objects.filter((Q(order_status="delivered",order_to=userDetails) | Q(order_status="completed",order_to=userDetails)))
        orders_deliv_lists = []
        todays_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        for u_order in user_orders:
            try:
                order_date = datetime.strptime(str(u_order.order_date),"%Y-%m-%d %H:%M:%S")
            except:
                order_date = datetime.strptime(str(u_order.order_date),"%Y-%m-%d %H:%M:%S.%f")
            delivery_details =  Order_Delivery.objects.filter(delivered_by=userDetails, order_no=u_order ).last()
            if(delivery_details != None):
                if(delivery_details.delivery_date != None):
                    try:
                        delivery_date = datetime.strptime(str(delivery_details.delivery_date),"%Y-%m-%d %H:%M:%S")
                    except:
                        delivery_date = datetime.strptime(str(delivery_details.delivery_date),"%Y-%m-%d %H:%M:%S.%f")
                    diff = relativedelta.relativedelta(order_date, delivery_date)
                    orders_deliv_lists.append(abs(diff.days))
                    try:
                        average_days = int(sum(orders_deliv_lists)/len(orders_deliv_lists))
                    except:
                        average_days = 0
                    if(average_days <= 1):
                        average_delivery_str = "Within 24 hours"
                    elif(average_days <= 2):
                        average_delivery_str = "Within 2 days"
                    elif(average_days <= 3):
                        average_delivery_str = "Within 3 days"
                    elif(average_days <= 5):
                        average_delivery_str = "Within 5 days"
                    elif(average_days >= 5):
                        average_delivery_str = "Within 10 days"
        get_active_orders = User_orders.objects.filter(Q(order_by=us) | Q(order_to= us),order_status = 'active' )
        for order in get_active_orders:
            get_order_messg = Order_Message.objects.filter(receiver=us,is_read=False,message_type='chat').count()
            if(get_order_messg  > 0):
                first_messg = Order_Message.objects.filter(receiver=us,is_read=False,message_type='chat').first()
                if(first_messg.mail_sent == False):
                    if(us.mail_order == True):
                        first_msg_obj = Order_Message.objects.get(pk = first_messg.pk)
                        first_msg_obj.mail_sent = True
                        first_msg_obj.save()
                        mail_content = MailTemplates.chat_order_message(str(first_messg.sender.username).title(),str(first_messg.receiver.username).title(),str(first_messg.text),str(first_messg.timestamp.strftime('%d %b, %Y')),str(order.order_no).title())
                        SendEmailAct(str(us.email),mail_content,"You've received messages from " + str(first_messg.sender.username).title() + ".")
        get_chat_messg = Message.objects.filter(receiver=us,is_read=False,message_type='chat').count()
        if(get_chat_messg  > 0):
            c_first_messg = Message.objects.filter(receiver=us,is_read=False,message_type='chat').first()
            if(c_first_messg.mail_sent == False):
                if(us.mail_order == True):
                    c_first_msg_obj = Message.objects.get(pk = c_first_messg.pk)
                    c_first_msg_obj.mail_sent = True
                    c_first_msg_obj.save()
                    c_mail_content = MailTemplates.chat_message(str(c_first_messg.sender.username).title(),str(c_first_messg.receiver.username).title(),str(c_first_messg.text),str(c_first_messg.timestamp.strftime('%d %b, %Y')))
                    SendEmailAct(str(us.email),c_mail_content,"You've received messages from " + str(first_messg.sender.username).title() + ".")
        total_earnng = User_Earnings.objects.filter(user_id=userDetails) 
        for earn in total_earnng:
            try:
                earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S.%f").date()
            except:
                earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S").date()
            if(earn.earning_type == "cancelled"):
                cancelled_earning_val = round(float(float(cancelled_earning_val) + float(earn.earning_amount)),2)
            if(earn.earning_type == "affiliate"):
                if(todays_date.month == earned_date.month):
                    current_month_earning_val = round(float(float(current_month_earning_val) + float(earn.earning_amount)),2)
                affilite_earn_val = round(float(float(affilite_earn_val) + float(earn.earning_amount)),2)
            if(earn.earning_type != "cancelled"):
                total_earning_val = total_earning_val
                if(todays_date.month == earned_date.month):
                    current_month_earning_val = round(float(float(current_month_earning_val) + float(earn.earning_amount)),2)
            if(earn.clearence_status == "completed"):
                if(earn.withdrawn_amount != ''):
                    withdrawed_credit_val = round(float(float(withdrawed_credit_val) + float(earn.withdrawn_amount)),2)
            if(earn.credit_used != None):
                if(earn.credit_used != ''):
                    with_used_credit_val = round(float(float(with_used_credit_val) + float(earn.credit_used)),2)
            if(earn.clearence_status == "cleared" ):
                try:
                    e_prev_credit = float(earn.credit_used)
                    e_actual_available = float(earn.aval_with) - float(e_prev_credit)
                    avail_bal_val = round(float(float(avail_bal_val) + float(e_actual_available)),2)
                except:
                    avail_bal_val = round(float(avail_bal_val),2)
            if(earn.clearence_status == "pending"):
                current_earning_val = round(float(float(current_earning_val) + float(earn.earning_amount)),2)
        refund_earning = User_Refund.objects.filter(user_id=userDetails,refund_status="cancelled")
        for r_earn in refund_earning: 
            prev_credit = float(r_earn.credit_used)
            actual_available = float(r_earn.refund_amount) - float(prev_credit)
            availcredit_bal_val = round(float(float(availcredit_bal_val) + float(actual_available)),2)
            if(r_earn.credit_used != None):
                if(r_earn.credit_used != ''):
                    ref_used_credit_val = round(float(float(ref_used_credit_val) + float(prev_credit)),2)
        userDetails.total_earning =  round(float(float(total_earning_val) + float(affilite_earn_val)),2)
        userDetails.current_earning = current_earning_val
        userDetails.cancelled_earning = cancelled_earning_val
        userDetails.avail_bal = avail_bal_val
        userDetails.current_month_earning = current_month_earning_val
        userDetails.availcredit_bal = availcredit_bal_val
        userDetails.referrals_earnings = affilite_earn_val
        userDetails.withdrawn_amount = withdrawed_credit_val
        userDetails.with_credits_used_amount = with_used_credit_val
        userDetails.refund_credits_used_amount = ref_used_credit_val
        userDetails.ordersin_progress = orders_count
        userDetails.avg_delivery_time = average_delivery_str
        userDetails.save()

def offers_module():
    all_users = []
    all_users = User.objects.filter(is_admin=False,profile_status="active")
    todays_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    for us in all_users:
        userDetails = User.objects.get(username = us.username)
        seller_lvel = SellerLevels4.objects.get(level_slug= userDetails.user_level.level_slug)
        userDetails.offers_left = seller_lvel.No_of_offers
        userDetails.save()
        if(UserAvailable.objects.filter(user_id=userDetails).exists() == True):
            user_avail_details = UserAvailable.objects.get(user_id=userDetails)
            availableto_date = datetime.strptime(str(user_avail_details.available_to),"%Y-%m-%d").date()
            if(int(todays_date.month) == int(availableto_date.month) and int(todays_date.day) == int(availableto_date.day) and int(todays_date.year) == int(availableto_date.year) ):
                UserAvailable.objects.filter(user_id=userDetails).delete()
                
def every_minute():
    all_users = []
    all_users = User.objects.filter(is_admin=False,profile_status="active")
    for us in all_users:
        userDetails = User.objects.get(username = us.username)
        todays_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        reolution_details = User_Order_Resolution.objects.filter( resolution_status = "pending" , raised_to= userDetails)
        for res in reolution_details:
            if(res.resolution_last_date != None):
                try:
                    resolution_last_date = datetime.strptime(str(res.resolution_last_date ),"%Y-%m-%d %H:%M:%S")
                except:
                    resolution_last_date = datetime.strptime(str(res.resolution_last_date ),"%Y-%m-%d %H:%M:%S.%f")
                if(int(todays_date.month) == int(resolution_last_date.month) and int(todays_date.day) == int(resolution_last_date.day) and int(todays_date.year) == int(resolution_last_date.year) and int(todays_date.hour) == int(resolution_last_date.hour)):
                    if(res.resolution_type == "cancel" and res.resolution_status == "pending"):
                        order_details = User_orders.objects.get(order_no = res.order_no)
                        transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                        order_by_user = User.objects.get(username= order_details.order_by.username)
                        order_to_user = User.objects.get(username= order_details.order_to.username)
                        if(User_Refund.objects.filter(order_no=order_details,transaction=transaction).exists() == False):
                            res.resolution_status = 'accepted'
                            res.save()
                            if(order_details.order_status != "completed" or order_details.order_status != "cancel"): 
                                order_details.order_status = 'cancel'
                                order_details.incoming_request = 'site'
                                order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                order_details.save()
                                transaction.transaction_status = "cancelled"
                                transaction.save()
                                raised_by = User.objects.get(username = res.raised_by.username)
                                raised_to = User.objects.get(username = res.raised_to.username)
                                notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                                if(notification_cancel.is_active == True):
                                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order',order_no = order_details,description= "Your order Automatically Cancelled.")
                                    noti_create.save()
                                refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res,order_no=order_details,transaction=transaction ,user_id=order_by_user,refund_status= 'cancelled')
                                refund_details.save()
                                try:    
                                    cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                                except:
                                    cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)   
                                order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "Order Marked as Cancelled.",conversation_id=cover_detls,order_no=order_details,message_type="chat",is_read= True)
                                order_message.save()
                                order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                                order_ativity.save()
                                earning_val = 0
                                if(float(order_details.order_amount) < 40):
                                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                                    for p in payment_parameters:
                                        serv_fees_val = p.service_fees
                                        serv_fees_type = p.fees_type
                                        if(serv_fees_type == "flat"):
                                            service_fees_price =  int(serv_fees_val)
                                        else:
                                            perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                            service_fees_price = round(perceof_budg,2)
                                else:
                                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                                    for p in payment_parameters:
                                        serv_fees_val = p.service_fees
                                        serv_fees_type = p.fees_type
                                        if(serv_fees_type == "flat"):
                                            service_fees_price =  int(serv_fees_val)
                                        else:
                                            perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                            service_fees_price = round(perceof_budg,2)
                                earning_val = float(earning_val) + (round(float(round(float(order_details.order_amount),2) - service_fees_price),2))
                                order_ativity1 = User_Order_Activity(order_message = "Cancelled Payment Refunded to Buyer",order_amount = earning_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                                order_ativity1.save()
                                order_by =  User.objects.get(username= order_details.order_by.username)   
                                order_to =  User.objects.get(username= order_details.order_to.username)
                                User_Order_Resolution.objects.filter(Q(raised_by = order_by, raised_to= order_to,resolution_status="pending" ,order_no = order_details) | Q(raised_by = order_to, raised_to= order_by,resolution_status="pending",order_no = order_details)).update(resolution_status="rejected", resolution_cancel_mssg = "Order Cancelled.")
                                raised_by = User.objects.get(username = res.raised_by.username)
                                raised_to = User.objects.get(username = res.raised_to.username)
                                notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                                if(notification_cancel.is_active == True):
                                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details,description=  "Your Order #"+ str(order_details.order_no) +" Automatically Marked as Cancelled.")
                                    noti_create.save()
                                if(order_by.mail_order == True):
                                    mail_content = MailTemplates.order_cancelled_buyer(str(order_by.username).title(),str("#"+order_details.order_no))
                                    SendEmailAct(str(order_by.email),mail_content,"Your order has been cancelled.")
                                if(order_to.mail_order == True):
                                    mail_content = MailTemplates.order_cancelled_seller(str(order_to.username).title(),str(order_by.username).title(),str("#"+order_details.order_no))
                                    SendEmailAct(str(order_to.email),mail_content,"Your order has been cancelled.")
                                service_fees_price = 0
                                if(float(order_details.order_amount) < 40):
                                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                                    for p in payment_parameters:
                                        serv_fees_val = p.service_fees
                                        serv_fees_type = p.fees_type
                                        if(serv_fees_type == "flat"):
                                            service_fees_price =  int(serv_fees_val)
                                        else:
                                            perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                            service_fees_price = round(perceof_budg,2)
                                else:
                                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                                    for p in payment_parameters:
                                        serv_fees_val = p.service_fees
                                        serv_fees_type = p.fees_type
                                        if(serv_fees_type == "flat"):
                                            service_fees_price =  int(serv_fees_val)
                                        else:
                                            perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                            service_fees_price = round(perceof_budg,2)
                                earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                                earning_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res,order_no= order_details,clearence_date=None,clearence_status="cancelled",cleared_on=None,user_id=order_to,earning_type="cancelled",affiliate_user=None)
                                earning_details.save()
                    elif(res.resolution_type=="extention" and res.resolution_status == "pending"):
                        order_details = User_orders.objects.get(order_no = res.order_no)
                        if(res.ext_new_date.date() != order_details.due_date.date()):
                            if(order_details.order_status != "completed" or order_details.order_status != "cancel"):  
                                res.resolution_status = 'accepted'
                                res.save()
                                raised_by = User.objects.get(username = res.raised_by.username)
                                raised_to = User.objects.get(username = res.raised_to.username)
                                order_details.due_date = res.ext_new_date
                                order_details.save()   
                                order_ativity = User_Order_Activity(order_message = "×1 Extended Delivery Time" , order_no=order_details,activity_type="extension",activity_by=raised_by,activity_to=raised_to)
                                order_ativity.save()
                                notification_extension = Notification_commands.objects.get(slug = "order_extended")
                                if(notification_extension.is_active == True):
                                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order',order_no = order_details,description=  "Your order Due Date Automatically Extended.")
                                    noti_create.save()
                                if(raised_by.mail_order == True):
                                    mail_content = MailTemplates.order_extension_accepted(str(raised_by.username).title(),str(raised_to.username).title(),str("#"+order_details.order_no))
                                    SendEmailAct(str(raised_by.email),mail_content,"Order Extension has been Approved by " + str(raised_to.username).title() + ".")
                    elif(res.resolution_type=="delivered" and res.resolution_status == "pending"):
                        order_details = User_orders.objects.get(order_no = res.order_no)
                        order_by =  User.objects.get(username= order_details.order_by.username)   
                        order_to =  User.objects.get(username= order_details.order_to.username) 
                        if(User_Earnings.objects.filter(order_no= order_details,earning_type="order").exists() == False):
                            if(order_details.order_status != "completed" or order_details.order_status != "cancel"):
                                service_fees_price = 0
                                if(float(order_details.order_amount) < 40):
                                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                                    for p in payment_parameters:
                                        serv_fees_val = p.service_fees
                                        serv_fees_type = p.fees_type
                                        if(serv_fees_type == "flat"):
                                            service_fees_price =  int(serv_fees_val)
                                        else:
                                            perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                            service_fees_price = round(perceof_budg,2)
                                else:
                                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                                    for p in payment_parameters:
                                        serv_fees_val = p.service_fees
                                        serv_fees_type = p.fees_type
                                        if(serv_fees_type == "flat"):
                                            service_fees_price =  int(serv_fees_val)
                                        else:
                                            perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                            service_fees_price = round(perceof_budg,2)
                                earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                                withdrwal_val = 0
                                withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days") )
                                for ext in withdrawal_ext:
                                    if(ext.parameter_name == "withdrawal_clearence_days"):
                                        withdrwal_val = ext.no_of_days
                                today_date = datetime.today()
                                res.resolution_status = 'accepted'
                                res.save()
                                raised_by = User.objects.get(username = res.raised_by.username)
                                raised_to = User.objects.get(username = res.raised_to.username)
                                transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                                transaction.transaction_status = "completed"
                                transaction.save()
                                notification_delivery = Notification_commands.objects.get(slug = "order_completed")
                                if(notification_delivery.is_active == True):
                                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details,description= "Your order #" + str(order_details.order_no) +" Automatically Marked as completed.")
                                    noti_create.save()
                                clearencedate = today_date + timedelta(days=int(withdrwal_val))                
                                order_details.order_status = 'completed'
                                order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                order_details.save()
                                order_to.u_last_delivery= datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                order_to.save()
                                try:    
                                    cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
                                except:
                                    cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)   
                                refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res,order_no= order_details,clearence_date=clearencedate,clearence_status="pending",cleared_on=None,user_id=order_to,earning_type="order",affiliate_user=None)
                                refund_details.save()
                                order_message = Order_Message(sender=order_by,receiver=order_to,text = "Order Marked as completed.",conversation_id=cover_detls,order_no=order_details,message_type="activity",is_read=True)
                                order_message.save()
                                get_message =  Order_Message.objects.get(pk = order_message.pk)
                                resolution= User_Order_Resolution(resolution_type="completed",resolution_text = "Completed",resolution_message="Completed",resolution_desc="Automatically Marked as Completed.",resolution_status="accepted",order_no=order_details,raised_by=order_by,raised_to=order_to,message=get_message)
                                resolution.save()
                                order_ativity = User_Order_Activity(order_message = "×1 Order Completed" , order_no=order_details,activity_type="completed",activity_by=order_by,activity_to=order_to)
                                order_ativity.save()
                                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earned_val , order_no=order_details,activity_type="pending",activity_by=order_by,activity_to=order_to)
                                order_ativity1.save()
                                User_Order_Resolution.objects.filter(Q(raised_by = raised_by, raised_to= raised_to,resolution_status="pending",order_no = order_details) | Q(raised_by = raised_to, raised_to= raised_by,resolution_status="pending",order_no = order_details)).update(resolution_status="rejected", resolution_cancel_mssg = "Order Completed.")
        total_earnng = User_Earnings.objects.filter(user_id=userDetails,clearence_status = "pending")
        for earn in total_earnng:
            if(earn.clearence_date != None and earn.clearence_status == "pending"):
                try:
                    clearence_date = datetime.strptime(str(earn.clearence_date),"%Y-%m-%d %H:%M:%S")
                except:
	                clearence_date = datetime.strptime(str(earn.clearence_date),"%Y-%m-%d %H:%M:%S.%f")
                if(int(todays_date.month) == int(clearence_date.month) and int(todays_date.day) == int(clearence_date.day) and int(todays_date.year) == int(clearence_date.year) and int(todays_date.hour) == int(clearence_date.hour)):
                    earn.aval_with = earn.earning_amount
                    earn.clearence_status = "cleared"
                    earn.cleared_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    earn.save()
                    order_details = User_orders.objects.get(order_no= earn.order_no)
                    order_by = User.objects.get(username = order_details.order_by.username)
                    order_to = User.objects.get(username = order_details.order_to.username)
                    try:
                        earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S").date()
                    except:
                        earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S.%f").date()
                    User_Order_Activity.objects.filter(order_no=order_details,activity_type="pending",activity_by=order_by,activity_to=order_to,activity_date__year=earned_date.year,activity_date__month=earned_date.month, activity_date__day=earned_date.day).update(order_message="Available for Withdrawal.")                 
                    if(earn.earning_type == "order" ):
                        re_withdrwal_val = 0
                        re_withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days") )
                        for ext in re_withdrawal_ext:
                            if(ext.parameter_name == "withdrawal_clearence_days"):
                                re_withdrwal_val = ext.no_of_days
                        re_today_date = datetime.today()
                        re_clearencedate = re_today_date + timedelta(days=int(re_withdrwal_val))   
                        buyer_refferal = None
                        try:
                            buyer_refferal = Referral_Users.objects.get(refferal_user = order_by)
                        except:
                            buyer_refferal = None
                        if(buyer_refferal != None):
                            affiliate_amount = 0
                            if(buyer_refferal.buyer_affi_done == False):
                                if(float(order_details.order_amount) >= 40):
                                    refferalby_user = User.objects.get(pk =buyer_refferal.user_id.pk)
                                    if(User_Earnings.objects.filter(order_no= order_details,earning_type="affiliate",user_id=refferalby_user).exists() == False):
                                        affiliate_amount = 5
                                        refferal_user = User.objects.get(pk =buyer_refferal.refferal_user.pk)
                                        earnings_details = User_Earnings(order_amount=affiliate_amount,earning_amount=affiliate_amount,platform_fees=0,aval_with="",order_no= order_details,clearence_date=re_clearencedate,clearence_status="pending",cleared_on=None,user_id=refferalby_user,earning_type="affiliate",affiliate_user= refferal_user)
                                        earnings_details.save()
                                        order_ativity = User_Order_Activity(order_message = "×1 Affiliate Commission" ,order_amount = affiliate_amount,activity_type="affiliate",order_no=order_details,activity_by=refferal_user,activity_to=refferalby_user)
                                        order_ativity.save()
                                        order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = affiliate_amount ,order_no=order_details,activity_type="pending",activity_by=refferal_user,activity_to=refferalby_user)
                                        order_ativity1.save()
                                buyer_refferal.buyer_affi_amount = affiliate_amount
                                buyer_refferal.buyer_affi_done = True
                                buyer_refferal.save()
                        seller_refferal = None
                        try:
                            seller_refferal = Referral_Users.objects.get(refferal_user = order_to)
                        except:
                            seller_refferal = None
                        if(seller_refferal != None):
                            s_affiliate_amount = 0
                            if(seller_refferal.seller_affi_done == False):
                                if(float(order_details.order_amount) >= 40):
                                    affiliate_amount = 5
                                    s_refferalby_user = User.objects.get(pk =seller_refferal.user_id.pk)
                                    if(User_Earnings.objects.filter(order_no= order_details,earning_type="affiliate",user_id=s_refferalby_user).exists() == False):
                                        s_refferal_user = User.objects.get(pk =seller_refferal.refferal_user.pk)
                                        earnings_details = User_Earnings(order_amount=affiliate_amount,earning_amount=affiliate_amount,platform_fees=0,aval_with="",order_no= order_details,clearence_date=re_clearencedate,clearence_status="pending",cleared_on=None,user_id=s_refferalby_user,earning_type="affiliate",affiliate_user=s_refferal_user)
                                        earnings_details.save()
                                        order_ativity = User_Order_Activity(order_message = "×1 Affiliate Commission" ,order_amount = affiliate_amount,activity_type="affiliate",order_no=order_details,activity_by=s_refferal_user,activity_to=s_refferalby_user)
                                        order_ativity.save()
                                        order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = affiliate_amount ,order_no=order_details,activity_type="pending",activity_by=s_refferal_user,activity_to=s_refferalby_user)
                                        order_ativity1.save()
                                seller_refferal.seller_affi_amount = affiliate_amount
                                seller_refferal.seller_affi_done = True
                                seller_refferal.save()    
                                                        
def monthly_routine():
    all_users = []
    today = datetime.today()
    first = today.replace(day=1)
    last_date = first - timedelta(days=1)
    first_date = last_date.replace(day=1)
    start_date = datetime.strptime(first_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
    end_date = datetime.strptime(last_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
    completed_orders1 = 0
    all_users = User.objects.filter(is_admin=False,profile_status="active")
    for us in all_users:
        time_diff = []
        mssg_responses =  Message_Response_Time.objects.filter(receiver = us).order_by('-timestamp')
        previous_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        for mssg_r in mssg_responses:
            try:
                resp_date = datetime.strptime(str(mssg_r.timestamp),"%Y-%m-%d %H:%M:%S.%f")
            except:
                resp_date = datetime.strptime(str(mssg_r.timestamp),"%Y-%m-%d %H:%M:%S")
            diff = relativedelta.relativedelta(previous_date,resp_date )
            time_diff.append(int(str(diff.hours).replace("+","").replace("-","")))
            try:
                previous_date = datetime.strptime(str(mssg_r.timestamp),"%Y-%m-%d %H:%M:%S.%f")
            except:
                previous_date = datetime.strptime(str(mssg_r.timestamp),"%Y-%m-%d %H:%M:%S")
        if(len(time_diff) != 0):
            average = Average_Time(time_diff)
            if(round(average) == 0):
                us.avg_respons = 1
                us.save()
            else:
                us.avg_respons = round(average)
                us.save()
        userDetails = User.objects.get(username = us.username)
        no_of_gigs = UserGigs.objects.filter(user_id = userDetails).count()
        if(no_of_gigs > 0):
            seller_level =  ''.join(re.findall(r'\d+', str(userDetails.user_level.level_slug)))
            get_seller_obj = SellerLevels4.objects.get(level_slug = "level"+ (seller_level))
            order_compl_amount = int(get_seller_obj.up_order_amount)
            order_compl_count = int(get_seller_obj.up_order_count)
            order_upgrade_check = int(get_seller_obj.record_check)
            today = datetime.today()
            first = today.replace(day=1)
            last_date = first - timedelta(days=1)
            end_date = datetime.strptime(last_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
            start_date = end_date -  relativedelta.relativedelta(months=int(order_upgrade_check))
            str_start_date = datetime.strptime(start_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
            completed_orders = User_orders.objects.filter(order_status = "completed",completed_date__range=(str_start_date, end_date),order_to=userDetails).count()
            earned_amount = int(round(float(userDetails.total_earning)))
            updgradelevl = None
            downgradelevl = None
            downgrade_levl =  SellerLevels4.objects.filter().last()
            last_down_levl = ''.join(re.findall(r'\d+', str(downgrade_levl.level_slug)))
            try:
                updgradelevl = SellerLevels4.objects.get(level_slug = "level"+ str((int(seller_level)+1)))
            except:
                updgradelevl = None
            try: 
                downgradelevl = SellerLevels4.objects.get(level_slug = "level"+ str((int(seller_level)-1)))
            except:
                downgradelevl = None
            if((completed_orders >= int(order_compl_count)) and (earned_amount >= int(order_compl_amount))):
                if(updgradelevl != None):
                    userDetails.user_level = updgradelevl
                    userDetails.save()
            else:
                if((int(seller_level) != 1) and (int(seller_level) != int(last_down_levl))):
                    if(downgradelevl != None):
                        userDetails.user_level = downgradelevl
                        userDetails.save()
    try:
        dsn = "host='localhost' dbname='kworkapp' user='kworkappuser' password='kworkappPWD'"
        conn = psycopg2.connect(dsn)  
        cursor = conn.cursor()
        sql = "DELETE FROM public.channels_postgres_groupchannel;"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass
    Message_Response_Time.objects.filter(timestamp__range=(start_date, end_date)).delete()
    UploadFile.objects.filter(timestamp__range=(start_date, end_date)).delete()
    channels_postgres.GroupChannel.objects.filter(expire__range=(start_date, end_date)).delete()
    
def get_buyer_request_view(request):
    if request.method == 'GET':
        category_name = request.GET['category_name']
        user_id = request.GET['user_id']
        userDetails = User.objects.get(pk=user_id)
        buyer_requests_list = []
        if(category_name == "All Subcategories"):
            UserGigCategory = UserGigs.objects.filter(user_id= userDetails , gig_status= "active").values("gig_category").distinct()
            for g_c in UserGigCategory:
                if(g_c["gig_category"] != None):
                    category_d = Categories.objects.get(id = g_c["gig_category"])
                    curr_date = datetime.today()
                    new_d = curr_date - timedelta(days=2)
                    buyer_requests = Buyer_Post_Request.objects.filter(service_category= category_d ,service_status="active",service_date__range=(new_d, curr_date),service_type='all').exclude(user_id= userDetails)
                    for b in buyer_requests:
                        offer_data = Request_Offers.objects.filter(user_id = userDetails,buyer_request=b).count()
                        offer_status = ''
                        if(offer_data ==0):
                            offer_status = "not sent"
                        else:
                            offer_status = "sent"
                        service_time_str = ''
                        no_of_offers = Request_Offers.objects.filter(buyer_request=b, offer_status_by_buyer='active').count()
                        if(b.service_time== "24hours"):
                            service_time_str = "24 Hours"
                        elif(b.service_time== "3days"):
                            service_time_str = "3 Days"
                        elif(b.service_time== "7days"):
                            service_time_str = "7 Days"
                        elif(b.service_time== "other"):
                            service_time_str = "Other"
                        no_of_offers = Request_Offers.objects.filter(buyer_request=b, offer_status_by_buyer='active').count()
                        buyer_requests_list.append({"serv_date":str(b.service_date),"buyer_img":b.user_id.avatar,"buyer_username":b.user_id.username,"buyer_mssg":b.service_desc,"buyer_attachments":b.service_images,"buyer_attachments":b.service_images,"no_offers":no_of_offers,"service_time":service_time_str,"service_price":b.service_budget,"req_id":b.id, "req_buyer_number":b.buyer_request_id,"Offer_status":offer_status})
        else:
            category_d = Categories.objects.get(category_Name =category_name)
            curr_date = datetime.today()
            new_d = curr_date - timedelta(days=2)
            buyer_requests = Buyer_Post_Request.objects.filter(service_category= category_d,service_status="active",service_date__range=(new_d, curr_date),service_type='all').exclude(user_id= userDetails)
            for b in buyer_requests:
                offer_data = Request_Offers.objects.filter(user_id = userDetails).count()
                offer_status = ''
                if(offer_data ==0):
                    offer_status = "not sent"
                else:
                    offer_status = "sent"
                service_time_str = ''
                no_of_offers = Request_Offers.objects.filter(buyer_request=b, offer_status_by_buyer='active').count()
                if(b.service_time== "24hours"):
                    service_time_str = "24 Hours"
                elif(b.service_time== "3days"):
                    service_time_str = "3 Days"
                elif(b.service_time== "7days"):
                    service_time_str = "7 Days"
                elif(b.service_time== "other"):
                    service_time_str = "Other"
                buyer_requests_list.append({"serv_date":str(b.service_date),"buyer_img":b.user_id.avatar,"buyer_username":b.user_id.username,"buyer_mssg":b.service_desc,"buyer_attachments":b.service_images,"buyer_attachments":b.service_images,"no_offers":no_of_offers,"service_time":service_time_str,"service_price":b.service_budget,"req_id":b.id, "req_buyer_number":b.buyer_request_id,"Offer_status":offer_status})
        return JsonResponse(json.dumps(buyer_requests_list),safe=False)
    
    
def get_modal_show_request_details_view(request):
    if request.method == 'GET':
        buyer_request_id = request.GET['buyer_request']
        user_id = request.GET['user_id']
        userDetails = User.objects.get(pk=user_id)
        buyer_request_data = []
        user_gig_details = []
        buyer_requests = Buyer_Post_Request.objects.get(id= buyer_request_id)
        buyer_request_data.append({"buyer_img":buyer_requests.user_id.avatar,"buyer_username":buyer_requests.user_id.username,"buyer_mssg":buyer_requests.service_desc})
        gigs_details = UserGigs.objects.filter(gig_status='active',user_id= userDetails)
        for u_gig in gigs_details:
            gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
            gig_image_url = ''
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            user_gig_details.append({"gig_id":u_gig.id,"gig_image":gig_image_url,"gig_title":u_gig.gig_title})
        response_data = {"buyer_details":buyer_request_data,"user_gig_details":user_gig_details}
        return JsonResponse(json.dumps(response_data),safe=False)

                    
def get_modal_show_gig_details_view(request):
    if request.method == 'GET':
        username = request.GET['username']
        userDetails = User.objects.get(username=username)
        user_gig_details = []
        gigs_details = UserGigs.objects.filter(gig_status='active',user_id= userDetails)
        for u_gig in gigs_details:
            gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
            gig_image_url = ''
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            user_gig_details.append({"gig_id":u_gig.id,"gig_image":gig_image_url,"gig_title":u_gig.gig_title})
        response_data = {"user_gig_details":user_gig_details}
        return JsonResponse(json.dumps(response_data),safe=False)

    
def get_gig_parameters_view(request):
    if request.method == 'GET':
        gig_id = request.GET['gig_id']
        user_id = request.GET['user_id']
        userDetails = User.objects.get(pk=user_id)
        gig_Parameters = []
        gigs_details = UserGigs.objects.get(id=gig_id)
        userpack= UserGigPackages.objects.filter(package_gig_name=gigs_details, package_type= 'basic').first() 
        if(userpack != None):
            start_price = userpack.package_price
            gig_Parameters.append({"data":userpack.package_data})
        else:
            gig_Parameters.append({"data":[],"gig_id":gig_id,"user_id":user_id})
        return JsonResponse(json.dumps(gig_Parameters),safe=False)
    

@csrf_exempt
def post_remove_request_view(request):
    if request.method == 'POST':
        b_req_id = request.POST.get("b_req_id")
        user_id = request.POST.get("user_id")
        Buyer_Post_Request.objects.filter(pk=b_req_id).delete()
        return HttpResponse("sucess")


@csrf_exempt
def post_offer_details_view(request):
    if request.method == 'POST':
        o_gig_id = request.POST.get("o_gig_id")
        o_b_req_id = request.POST.get("o_b_req_id")
        o_user_id = request.POST.get("o_user_id")
        o_text_desc = request.POST.get("o_text_desc")
        o_text_price = request.POST.get("o_text_price")
        o_text_del_time = request.POST.get("o_text_del_time")
        o_text_no_revs = request.POST.get("o_text_no_revs")
        o_text_req_gig = request.POST.get("o_text_req_gig")
        off_req= ''
        if(o_text_req_gig == "true"):
            off_req= True
        else:
            off_req= False
        o_offer_type = request.POST.get("o_offer_type")
        o_extra_params = request.POST['o_extra_params']
        gigs_details = UserGigs.objects.get(id=o_gig_id)
        buyer_req_details = Buyer_Post_Request.objects.get(id=o_b_req_id)
        userDetails = User.objects.get(pk=o_user_id)
        offer_details = Request_Offers(gig_name=gigs_details,buyer_request=buyer_req_details,user_id=userDetails, offer_desc=o_text_desc, offer_budget=o_text_price, offer_time=o_text_del_time,no_revisions=o_text_no_revs, ask_requirements= off_req, extra_parameters=str(o_extra_params),offer_type=o_offer_type, )
        offer_details.save()
        last_offer_num = userDetails.offers_left
        userDetails.offers_left = int(last_offer_num) - 1
        userDetails.save()
        return HttpResponse(str(int(last_offer_num) - 1))
    
    
@csrf_exempt
def post_custom_offer_details_view(request):
    if request.method == 'POST':
        o_gig_id = request.POST.get("o_gig_id")
        o_user_id = request.POST.get("o_user_id")
        o_text_desc = request.POST.get("o_text_desc")
        o_text_price = request.POST.get("o_text_price")
        o_text_del_time = request.POST.get("o_text_del_time")
        o_text_no_revs = request.POST.get("o_text_no_revs")
        o_text_req_gig = request.POST.get("o_text_req_gig")
        o_buyer_req_id = request.POST.get("o_buyer_req_id")
        o_offer_sender = request.POST.get("offer_sender")
        o_offer_receiver = request.POST.get("offer_receiver")
        try:
            off_req= ''
            if(o_text_req_gig == "true"):
                off_req= True
            else:
                off_req= False
            o_offer_type = request.POST.get("o_offer_type")
            o_extra_params = request.POST['o_extra_params']
            gigs_details = UserGigs.objects.get(id=o_gig_id)
            user_off_sender = User.objects.get(username = o_offer_sender)
            user_off_receiver = User.objects.get(username = o_offer_receiver)
            if(int(o_buyer_req_id) != 0):
                try:
                    buyer_req_details = Buyer_Post_Request.objects.get(pk = o_buyer_req_id)
                except:
                    buyer_req_details = None
            else:
                buyer_req_details = None
            offer_details = Request_Offers(gig_name=gigs_details,user_id=user_off_sender,buyer_request=buyer_req_details,custom_user=user_off_receiver, offer_desc=o_text_desc, offer_budget=o_text_price, offer_time=o_text_del_time,no_revisions=o_text_no_revs, ask_requirements= off_req, extra_parameters=str(o_extra_params),offer_type=o_offer_type, )
            offer_details.save()
            data = offer_details.pk
        except Exception as e:
            data = (str(type(e)) + str(e))
        return HttpResponse(data)


def get_sorted_offers_view(request):
    if request.method == 'GET':
        sort_val = request.GET['sort_val']
        buyer_id = request.GET['buyer_id']
        buyer_offers_li = []
        buyer_offers = []
        buyer_offer_sorted_li = []
        buyer_request = Buyer_Post_Request.objects.get(buyer_request_id= buyer_id)
        buyer_offers = Request_Offers.objects.filter(buyer_request= buyer_request, offer_type= "request", offer_status_by_buyer='active')
        for b_o in buyer_offers:
            gig_details = UserGigs.objects.get(gig_title = b_o.gig_name.gig_title)
            gig_image_url = ''
            gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            seller_reviews = Seller_Reviews.objects.filter(package_gig_name= gig_details)
            seller_count = 0
            for s_review in seller_reviews:
                seller_count = seller_count + float(s_review.average_val)
            try:
                seller_count = round(float(round(seller_count/len(seller_reviews),0)))
            except:
                seller_count = 0
            
            user_details_off = User.objects.get(username = b_o.user_id.username)
            seller_levl = str(user_details_off.user_level.level_name)
            buyer_offers_li.append({"buyer_username":b_o.user_id.username,"buyer_image":b_o.user_id.avatar,"gig_title":b_o.gig_name.gig_title ,"gig_image":gig_image_url,"seller_reviews":seller_count,"offer_desc":b_o.offer_desc,"offer_price":b_o.offer_budget,"offer_time":b_o.offer_time,"seller_level":seller_levl,"offer_date":str(b_o.offer_date),"offer_id":b_o.id})
        if(sort_val== "default"):
            buyer_offer_sorted_li = buyer_offers_li 
        elif(sort_val== "price"):
            buyer_offer_sorted_li =sorted(buyer_offers_li, key=itemgetter('offer_price')) 
        elif(sort_val== "delivery time"):
            buyer_offer_sorted_li =sorted(buyer_offers_li, key=itemgetter('offer_time')) 
        elif(sort_val== "rating"):
            buyer_offer_sorted_li =sorted(buyer_offers_li, key=itemgetter('seller_reviews'))          
        return JsonResponse(json.dumps(buyer_offer_sorted_li),safe=False)
    

def post_remove_b_offer_req_view(request):
    if request.method == 'GET':
        offer_id = request.GET['offer_id']
        offer_request = Request_Offers.objects.get(pk= offer_id)
        offer_request.offer_status_by_buyer = 'deleted'
        offer_request.save()
        return HttpResponse("sucess")
    
def get_sent_offers_view(request):
    if request.method == 'GET':
        user_id = request.GET['user_id']
        userDetails = User.objects.get(pk=user_id)
        offers_sent = Request_Offers.objects.filter(user_id= userDetails,offer_type='request')
        offers_sent_list = []
        for off in offers_sent:
            service_time_str = ''
            if(off.buyer_request.service_time != None):
                if(off.buyer_request.service_time== "24hours"):
                    service_time_str = "24 Hours"
                elif(off.buyer_request.service_time== "3days"):
                    service_time_str = "3 Days"
                elif(off.buyer_request.service_time== "7days"):
                    service_time_str = "7 Days"
                elif(off.buyer_request.service_time== "other"):
                    service_time_str = "Other"
            offers_sent_list.append({"gig_title":off.gig_name.gig_title,"offer_desc":off.offer_desc,"duration":off.offer_time,"price":off.offer_budget,"buyer_img":off.buyer_request.user_id.avatar,"buyer_name":off.buyer_request.user_id.username,"buyer_req_desc":off.buyer_request.service_desc,"buyer_delivery_time":service_time_str, "buyer_price":off.buyer_request.service_budget})
        return JsonResponse(json.dumps(offers_sent_list),safe=False)


def post_flutterwave_transaction_view(request):
    if request.method == 'GET':
        u_offer_id = request.GET['u_offer_id']
        u_user_id = request.GET['u_user_id']
        u_status = request.GET['u_status']
        u_trans_ref = request.GET['u_trans_ref']
        u_trans_id = request.GET['u_trans_id']
        pay_by_user = User.objects.get(pk = u_user_id)
        offers_sent = Request_Offers.objects.get(pk= u_offer_id)
        pay_to_user = User.objects.get(pk = offers_sent.user_id.id)
        gig_details = UserGigs.objects.get(gig_title = offers_sent.gig_name.gig_title)
        api_details = Api_keys.objects.filter(api_name= "flutterwave").first()
        payment.token = api_details.secrete_key
        details = payment.get_payment_details(u_trans_id)
        data = [] 
        t_e_c_used = 0
        try:       
            flu_amout = details['data']['amount']
            flu_app_fee = details['data']['app_fee']
            flu_pay_type = details['data']['payment_type']
            flu_accnt_id = details['data']['account_id']
            flutt_flw_ref = details['data']['flw_ref']
            meta_data =  details['data']['meta']['data_extra']
            order_amount =  details['data']['meta']['base_price_wsdf']
            u_service_fees =  details['data']['meta']['token']
            u_credit_used =  round(float(details['data']['meta']['credit_used']),2)
            u_base_price = request.GET['u_base_price']
            u_total_price = request.GET['u_total_price']
            already_submitted = 0
            current_val = u_credit_used
            if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offers_sent,paid_by=pay_by_user,paid_to=pay_to_user,paid_for='order').exists() == False):
                if(float(u_credit_used) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled").order_by("pk")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        prev_credit = 0.0
                        actual_available = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(round((actual_available)) != 0):
                                    if(float(current_val) <= float(actual_available)):
                                        previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                        current_val =  0.0
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                    elif(float(u_credit_used) > float(actual_available)):
                                        if(float(current_val) != 0.0):
                                            if(float(current_val) >= float(actual_available)):
                                                c_used_credit = float(actual_available) 
                                            else:
                                                c_used_credit = float(actual_available) - float(current_val)
                                            present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                            r_earn.credit_used = str(round(float(abs(present_credit)),2))
                                            r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            r_earn.save()
                                            current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user,clearence_status="cleared" ).order_by("pk")
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(round((actual_available)) != 0):
                                        if(float(current_val) <= float(actual_available)): 
                                            previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                            t_e_c_used = float(current_val)
                                            current_val =  0.0
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                        elif(float(current_val) > float(actual_available)):
                                            if(float(current_val) != 0.0):
                                                if(float(current_val) >= float(actual_available)):
                                                    c_used_credit = float(actual_available) 
                                                else:
                                                    c_used_credit = float(actual_available) - float(current_val)
                                                present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                                earn.credit_used = str(round(float(abs(present_credit)),2))
                                                earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                                earn.save()
                                                t_e_c_used = float(t_e_c_used) + float(c_used_credit) 
                                                current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                no_of_days = int(offers_sent.offer_time)
                meta_data_list = meta_data.split(",")
                Begindatestring = datetime.today()
                due_date = Begindatestring + timedelta(days=no_of_days)
                if any("del_" in s.strip() for s in meta_data_list):
                    matching = [s.strip() for s in meta_data_list if "del_" in s.strip()]
                    matching_str = ''.join(map(str, matching))
                    extra_del_Details = UserGig_Extra_Delivery.objects.get(pk=int(str(matching_str).replace("del_","")))
                    no_of_days = int(extra_del_Details.delivery_in.parameter_value)
                    due_date = Begindatestring + timedelta(days=no_of_days)
                    order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=order_amount,due_date=due_date)
                    order_details.save()
                else:
                    order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=order_amount,due_date=due_date)
                    order_details.save() 
                order_details_get = User_orders.objects.get(pk = order_details.pk)
                if(float(t_e_c_used) != 0):
                    cre_order_activity = User_Order_Activity(order_message="×1 Credit Used for Purchase.",order_amount=str(t_e_c_used),order_no = order_details_get,activity_type="used_credit",activity_by=pay_by_user,activity_to=pay_by_user)
                    cre_order_activity.save()
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details_get).count()
                else:
                    already_submitted = 2
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        cover_detls = Order_Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        cover_detls = Order_Conversation(initiator=pay_by_user,receiver=pay_to_user,order_no=order_details_get)
                        cover_detls.save()
                try:    
                    message_cover_detls = Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        message_cover_detls = Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        message_cover_detls = Conversation(initiator=pay_to_user,receiver = pay_by_user,convers_type="active")
                        message_cover_detls.save()  
                cover_detls =  Order_Conversation.objects.get(pk = cover_detls.pk)
                order_activity = User_Order_Activity(order_message="×1"+ str(gig_details.gig_title),order_amount=str(offers_sent.offer_budget),order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                order_activity.save()
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='flutterwave',transaction_id=u_trans_id,payment_status=u_status,transaction_ref= u_trans_ref,payment_currency="USD",offer_amount=order_amount,total_amount=flu_amout,processing_fees= u_service_fees,flutter_fluw_ref= flutt_flw_ref,flutter_account_id=flu_accnt_id,flutter_app_fee=flu_app_fee,flutter_pay_type=flu_pay_type,paid_by=pay_by_user,paid_to=pay_to_user,order_no=order_details_get,paid_for='order',transaction_status="active",credits_used=u_credit_used)
                user_trans.save()
                order_message = Order_Message(sender=pay_by_user,receiver=pay_to_user,text = "placed the order",conversation_id=cover_detls,order_no=order_details_get,message_type="chat",is_read = True)
                order_message.save()
                for meta in meta_data_list:
                    if(meta != "None"):
                        if(meta.strip().startswith('del_')):
                            try:
                                main_string= str(meta.strip()).replace("del_","").replace("%20","")
                                extra_del_Details = UserGig_Extra_Delivery.objects.get(pk=int(main_string))
                                user_extra_del = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= None,gig_extra_delivery= extra_del_Details)
                                user_extra_del.save()
                                order_activity = User_Order_Activity(order_message="×1 Extra Fast Delivery",order_amount=extra_del_Details.extra_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                                order_activity.save()
                            except:
                                pass
                        else:
                            try:
                                main_int= str(meta.strip()).replace("%20","")
                                extra_gig = UserExtra_gigs.objects.get(pk = int(main_int))
                                user_extra_gig = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= extra_gig,gig_extra_delivery= None)
                                user_extra_gig.save()
                                order_activity = User_Order_Activity(order_message="×1"+ str(extra_gig.extra_gig_title),order_amount=extra_gig.extra_gig_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                                order_activity.save()
                            except:
                                pass                   
                notification_settings = Notification_commands.objects.get(slug = "payment_sucessful")
                if(notification_settings.is_active == True):
                    sender = User.objects.get(username = 'admin')
                    noti_create = CustomNotifications(sender = sender, recipient=pay_by_user, verb='payment',description="Your Card payment is sucessful.")
                    noti_create.save()
                notification_order = Notification_commands.objects.get(slug = "order_received")
                if(notification_order.is_active == True):
                    noti_create = CustomNotifications(sender = pay_by_user, recipient=pay_to_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_by_user.username).title() + " is started.")   
                    noti_create.save() 
                    noti_create = CustomNotifications(sender = pay_to_user, recipient=pay_by_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_to_user.username).title() + " is started.")
                    noti_create.save()
                if(pay_by_user.mail_order == True):
                    mail_content2 = MailTemplates.order_mail_receipt_buyer(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                    SendEmailAct(str(pay_by_user.email),mail_content2,"Here's your receipt of order - #" + str(order_details.order_no) + ".")
                if(pay_to_user.mail_order == True):
                    mail_content1 = MailTemplates.order_mail_seller(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                    if(offers_sent.offer_type == "request"):
                        SendEmailAct(str(pay_to_user.email),mail_content1," Great news: Your offer has been accepted by " + str(pay_by_user.username).title() +".")
                    else:
                        SendEmailAct(str(pay_to_user.email),mail_content1," Congrates: You have received order from " + str(pay_by_user.username).title() +".")
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
            else:
                order_details = User_orders.objects.get(package_gig_name= gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user)
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details).count()
                else:
                    already_submitted = 2  
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)

def post_paypal_transaction_view(request):
    if request.method == 'GET':
        u_offer_id = request.GET['u_offer_id']
        u_user_id = request.GET['u_user_id']
        u_paypal_id = request.GET['u_paypal_id']
        u_paypal_email = request.GET['u_paypal_email']
        u_trans_id = request.GET['u_trans_id']
        u_trans_status = request.GET['u_trans_status']
        u_base_price = request.GET['u_base_price']
        u_total_price = request.GET['u_total_price']
        u_service_fees = request.GET['u_service_fees']
        u_extra_gigs = request.GET['u_extra_gigs']
        u_credit_used = round(float(request.GET['u_credits_used']),2)
        pay_by_user = User.objects.get(pk = u_user_id)
        offers_sent = Request_Offers.objects.get(pk= u_offer_id)
        pay_to_user = User.objects.get(pk = offers_sent.user_id.id)
        gig_details = UserGigs.objects.get(gig_title = offers_sent.gig_name.gig_title)
        already_submitted = 0
        data = []
        t_e_c_used = 0
        try:
            current_val = u_credit_used
            if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offers_sent,paid_by=pay_by_user,paid_to=pay_to_user,paid_for='order').exists() == False):
                if(float(u_credit_used) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled").order_by("pk")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        prev_credit = 0.0
                        actual_available = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(round((actual_available)) != 0):
                                    if(float(current_val) <= float(actual_available)):
                                        previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                        current_val =  0.0
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                    elif(float(u_credit_used) > float(actual_available)):
                                        if(float(current_val) != 0.0):
                                            if(float(current_val) >= float(actual_available)):
                                                c_used_credit = float(actual_available) 
                                            else:
                                                c_used_credit = float(actual_available) - float(current_val)
                                            present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                            r_earn.credit_used = str(round(float(abs(present_credit)),2))
                                            r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            r_earn.save()
                                            current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user,clearence_status="cleared" ).order_by("pk")
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(round((actual_available)) != 0):
                                        if(float(current_val) <= float(actual_available)): 
                                            previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                            t_e_c_used = float(current_val)
                                            current_val =  0.0
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                        elif(float(current_val) > float(actual_available)):
                                            if(float(current_val) != 0.0):
                                                if(float(current_val) >= float(actual_available)):
                                                    c_used_credit = float(actual_available) 
                                                else:
                                                    c_used_credit = float(actual_available) - float(current_val)
                                                present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                                earn.credit_used = str(round(float(abs(present_credit)),2))
                                                earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                                earn.save()
                                                t_e_c_used = float(t_e_c_used) + float(c_used_credit) 
                                                current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                no_of_days = int(offers_sent.offer_time)
                meta_data_list = u_extra_gigs.split(",")
                Begindatestring = datetime.today()
                due_date = Begindatestring + timedelta(days=no_of_days)
                if any("del_" in s.strip() for s in meta_data_list):
                    matching = [s.strip() for s in meta_data_list if "del_" in s.strip()]
                    matching_str = str(''.join(map(str, matching))).strip().replace("del_","").replace("%20","")
                    extra_del_Details = UserGig_Extra_Delivery.objects.get(pk=int(matching_str.strip()))
                    no_of_days = int(extra_del_Details.delivery_in.parameter_value)
                    due_date = Begindatestring + timedelta(days=no_of_days)
                    order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=u_base_price,due_date=due_date,completed_date=None)
                    order_details.save()
                else:
                    order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=u_base_price,due_date=due_date,completed_date=None)
                    order_details.save()
                order_details_get = User_orders.objects.get(pk = order_details.pk)
                if(float(t_e_c_used) != 0):
                    cre_order_activity = User_Order_Activity(order_message="×1 Credit Used for Purchase.",order_amount=str(t_e_c_used),order_no = order_details_get,activity_type="used_credit",activity_by=pay_by_user,activity_to=pay_by_user)
                    cre_order_activity.save()
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details_get).count()
                else:
                    already_submitted = 2
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        cover_detls = Order_Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        cover_detls = Order_Conversation(initiator=pay_by_user,receiver=pay_to_user,order_no=order_details_get)
                        cover_detls.save()
                try:    
                    message_cover_detls = Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        message_cover_detls = Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        message_cover_detls = Conversation(initiator=pay_to_user,receiver = pay_by_user,convers_type="active")
                        message_cover_detls.save()  
                cover_detls =  Order_Conversation.objects.get(pk = cover_detls.pk)
                order_activity = User_Order_Activity(order_message="×1"+ str(gig_details.gig_title),order_amount=str(offers_sent.offer_budget),order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                order_activity.save()
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='paypal',transaction_id=u_trans_id,payment_status=u_trans_status,payment_currency="USD",offer_amount=u_base_price,total_amount=u_total_price,processing_fees= u_service_fees,paypal_id=u_paypal_id,paypal_email=u_paypal_email,paid_by=pay_by_user,paid_to=pay_to_user,order_no=order_details_get,paid_for='order',transaction_status="active",credits_used=u_credit_used)
                user_trans.save()
                for meta in meta_data_list:
                    if(meta != "None"):
                        if("del_" in meta.strip()):
                            try:
                                main_string= str(meta.strip()).replace("del_","").replace("%20","")
                                extra_del_Details = UserGig_Extra_Delivery.objects.get(pk=int(main_string))
                                user_extra_del = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= None,gig_extra_delivery= extra_del_Details)
                                user_extra_del.save()
                                order_activity = User_Order_Activity(order_message="×1 Extra Fast Delivery",order_amount=extra_del_Details.extra_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                                order_activity.save()
                            except:
                                pass
                        else:
                            try:
                                main_int= str(meta.strip()).replace("%20","")
                                extra_gig = UserExtra_gigs.objects.get(pk = int(main_int))
                                user_extra_gig = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= extra_gig,gig_extra_delivery= None)
                                user_extra_gig.save()
                                order_activity = User_Order_Activity(order_message="×1"+ str(extra_gig.extra_gig_title),order_amount=extra_gig.extra_gig_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                                order_activity.save()
                            except:
                                pass
                notification_settings = Notification_commands.objects.get(slug = "payment_sucessful")
                if(notification_settings.is_active == True):
                    sender = User.objects.get(username = 'admin')
                    noti_create = CustomNotifications(sender = sender, recipient=pay_by_user, verb='payment',description="Your Paypal payment is sucessful.") 
                    noti_create.save()
                notification_order = Notification_commands.objects.get(slug = "order_received")
                if(notification_order.is_active == True):
                    noti_create = CustomNotifications(sender = pay_by_user, recipient=pay_to_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_by_user.username).title() + " is started.")   
                    noti_create.save()
                    noti_create = CustomNotifications(sender = pay_to_user, recipient=pay_by_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_to_user.username).title() + " is started.")
                    noti_create.save()
                if(pay_by_user.mail_order == True):
                    mail_content2 = MailTemplates.order_mail_receipt_buyer(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                    SendEmailAct(str(pay_by_user.email),mail_content2,"Here's your receipt of order - #" + str(order_details.order_no) + ".")
                if(pay_to_user.mail_order == True):
                    mail_content1 = MailTemplates.order_mail_seller(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                    if(offers_sent.offer_type == "request"):
                        SendEmailAct(str(pay_to_user.email),mail_content1," Great news: Your offer has been accepted by " + str(pay_by_user.username).title() +".")
                    else:
                        SendEmailAct(str(pay_to_user.email),mail_content1," Congrates: You have received order from " + str(pay_by_user.username).title() +".")
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
            else:
                order_details = User_orders.objects.get(package_gig_name= gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user)
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details).count()
                else:
                    already_submitted = 2
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e) })
        return JsonResponse(json.dumps(data),safe=False)



def post_credit_transaction_view(request):
    if request.method == 'GET':
        u_offer_id = request.GET['offer_id']
        u_base_price = request.GET['base_price']
        u_total_price =  round(float(request.GET['total_price']),2)
        u_service_fees = request.GET['fees']
        u_extra_gigs = request.GET['extra_gigs']
        u_user_id = request.GET['pay_user']
        u_pay_by = request.GET['pay_by']
        u_credit_used = round(float(request.GET['used_credits']),2)
        pay_by_user = User.objects.get(username = u_pay_by)
        offers_sent = Request_Offers.objects.get(pk= u_offer_id)
        pay_to_user = User.objects.get(pk = offers_sent.user_id.id)
        gig_details = UserGigs.objects.get(gig_title = offers_sent.gig_name.gig_title)
        already_submitted = 0
        data = []
        t_e_c_used = 0
        try:
            current_val = u_credit_used
            if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offers_sent,paid_by=pay_by_user,paid_to=pay_to_user,paid_for='order').exists() == False):
                if(float(u_credit_used) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled").order_by("pk")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        prev_credit = 0.0
                        actual_available = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(round((actual_available)) != 0):
                                    if(float(current_val) <= float(actual_available)):
                                        previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                        current_val =  0.0
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                    elif(float(u_credit_used) > float(actual_available)):
                                        if(float(current_val) != 0.0):
                                            if(float(current_val) >= float(actual_available)):
                                                c_used_credit = float(actual_available) 
                                            else:
                                                c_used_credit = float(actual_available) - float(current_val)
                                            present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                            r_earn.credit_used = str(round(float(abs(present_credit)),2))
                                            r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            r_earn.save()
                                            current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user,clearence_status="cleared" ).order_by("pk")
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(round((actual_available)) != 0):
                                        if(float(current_val) <= float(actual_available)): 
                                            previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                            t_e_c_used = float(current_val)
                                            current_val =  0.0
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                        elif(float(current_val) > float(actual_available)):
                                            if(float(current_val) != 0.0):
                                                if(float(current_val) >= float(actual_available)):
                                                    c_used_credit = float(actual_available) 
                                                else:
                                                    c_used_credit = float(actual_available) - float(current_val)
                                                present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                                earn.credit_used = str(round(float(abs(present_credit)),2))
                                                earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                                earn.save()
                                                t_e_c_used = float(t_e_c_used) + float(c_used_credit) 
                                                current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                u_trans_status = "successful"
                s = shortuuid.ShortUUID(alphabet="0123456789")
                u_trans_id = s.random(length=8)
                no_of_days = int(offers_sent.offer_time)
                meta_data_list = u_extra_gigs.split(",")
                Begindatestring = datetime.today()
                due_date = Begindatestring + timedelta(days=no_of_days)
                if any("del_" in s.strip() for s in meta_data_list):
                    matching = [s.strip() for s in meta_data_list if "del_" in s.strip()]
                    matching_str = str(''.join(map(str, matching))).strip().replace("del_","").replace("%20","")
                    extra_del_Details = UserGig_Extra_Delivery.objects.get(pk=int(matching_str.strip()))
                    no_of_days = int(extra_del_Details.delivery_in.parameter_value)
                    due_date = Begindatestring + timedelta(days=no_of_days)
                    order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=u_base_price,due_date=due_date,completed_date=None)
                    order_details.save()
                else:
                    order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=u_base_price,due_date=due_date,completed_date=None)
                    order_details.save()
                order_details_get = User_orders.objects.get(pk = order_details.pk)
                if(float(t_e_c_used) != 0):
                    cre_order_activity = User_Order_Activity(order_message="×1 Credit Used for Purchase",order_amount=str(t_e_c_used),order_no = order_details_get,activity_type="used_credit",activity_by=pay_by_user,activity_to=pay_by_user)
                    cre_order_activity.save()
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details_get).count()
                else:
                    already_submitted = 2
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        cover_detls = Order_Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        cover_detls = Order_Conversation(initiator=pay_by_user,receiver=pay_to_user,order_no=order_details_get)
                        cover_detls.save()
                try:    
                    message_cover_detls = Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        message_cover_detls = Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        message_cover_detls = Conversation(initiator=pay_to_user,receiver = pay_by_user,convers_type="active")
                        message_cover_detls.save()   
                cover_detls =  Order_Conversation.objects.get(pk = cover_detls.pk)
                order_activity = User_Order_Activity(order_message="×1"+ str(gig_details.gig_title),order_amount=str(offers_sent.offer_budget),order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                order_activity.save()
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='credit',transaction_id=u_trans_id,payment_status=u_trans_status,payment_currency="USD",offer_amount=u_base_price,total_amount=u_total_price,processing_fees= u_service_fees,paid_by=pay_by_user,paid_to=pay_to_user,order_no=order_details_get,paid_for='order',transaction_status="active",credits_used=u_credit_used)
                user_trans.save()
                for meta in meta_data_list:
                    if(meta != "None"):
                        if("del_" in meta.strip()):
                            try:
                                main_string= str(meta.strip()).replace("del_","").replace("%20","")
                                extra_del_Details = UserGig_Extra_Delivery.objects.get(pk=int(main_string))
                                user_extra_del = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= None,gig_extra_delivery= extra_del_Details)
                                user_extra_del.save()
                                order_activity = User_Order_Activity(order_message="×1 Extra Fast Delivery",order_amount=extra_del_Details.extra_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                                order_activity.save()
                            except:
                                pass
                        else:
                            try:
                                main_int= str(meta.strip()).replace("%20","")
                                extra_gig = UserExtra_gigs.objects.get(pk = int(main_int))
                                user_extra_gig = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= extra_gig,gig_extra_delivery= None)
                                user_extra_gig.save()
                                order_activity = User_Order_Activity(order_message="×1"+ str(extra_gig.extra_gig_title),order_amount=extra_gig.extra_gig_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                                order_activity.save()
                            except:
                                pass
                notification_order = Notification_commands.objects.get(slug = "order_received")
                if(notification_order.is_active == True):
                    noti_create = CustomNotifications(sender = pay_by_user, recipient=pay_to_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_by_user.username).title() + " is started.")   
                    noti_create.save()
                    noti_create = CustomNotifications(sender = pay_to_user, recipient=pay_by_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_to_user.username).title() + " is started.")
                    noti_create.save()
                if(pay_by_user.mail_order == True):
                    mail_content2 = MailTemplates.order_mail_receipt_buyer(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                    SendEmailAct(str(pay_by_user.email),mail_content2,"Here's your receipt of order - #" + str(order_details.order_no) + ".")
                if(pay_to_user.mail_order == True):
                    mail_content1 = MailTemplates.order_mail_seller(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                    if(offers_sent.offer_type == "request"):
                        SendEmailAct(str(pay_to_user.email),mail_content1," Great news: Your offer has been accepted by " + str(pay_by_user.username).title() +".")
                    else:
                        SendEmailAct(str(pay_to_user.email),mail_content1," Congrates: You have received order from " + str(pay_by_user.username).title() +".")                
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
            else:
                order_details = User_orders.objects.get(package_gig_name= gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user)
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details).count()
                else:
                    already_submitted = 2
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)


def post_mark_as_read_view(request):
    if request.method == 'GET':
        gig_id = request.GET['gig_id']
        user_id = request.GET['user_id']
        req_ques = request.GET['req_ques']
        order_no = request.GET['order_no']
        data = []
        try:
            order_by_user = User.objects.get(username = user_id)
            gig_details = UserGigs.objects.get(pk = gig_id)
            order_details_get = User_orders.objects.get(order_no = order_no)
            b_reqs = Buyer_Requirements(gig_name=gig_details,requirement_ques=req_ques,user_id=order_by_user,default_req=True,order_no=order_details_get)
            b_reqs.save()
            data.append({"sucess" : "sucess"})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)
    
def post_buyer_requ_save_view(request):
    if request.method == 'GET':
        gig_id = request.GET['gig_id']
        user_id = request.GET['user_id']
        req_ques = request.GET['req_ques']
        req_ans = request.GET['req_ans']
        req_imgs = request.GET['req_imgs']
        order_no = request.GET['order_no']
        data = []
        try:
            order_by_user = User.objects.get(username = user_id)
            gig_details = UserGigs.objects.get(pk = gig_id)
            order_details_get = User_orders.objects.get(order_no = order_no)
            b_reqs = Buyer_Requirements(gig_name=gig_details,requirement_ques=req_ques,user_id=order_by_user,default_req=False,requirement_ans=req_ans,req_documents=req_imgs,order_no=order_details_get)
            b_reqs.save()
            data.append({"sucess" : "sucess"})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)
    
@csrf_exempt
def post_req_image_upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files") 
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/buyer_requirements/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/buyer_requirements/'+file_path
                urls.append(url)
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)
    

def post_check_for_order_view(request):
    if request.method == 'GET':
        order_to = request.GET['order_to']
        gig_id = request.GET['gig_id']
        order_by = request.GET['order_by']
        offer_id = request.GET['offer_id']
        buyer_re_id = request.GET['buyer_re_id']
        order_by_user = User.objects.get(username = order_by)
        order_to_user = User.objects.get(username = order_to)
        gig_details = UserGigs.objects.get(pk = gig_id)
        offer_details = Request_Offers.objects.get(pk = offer_id)
        data = ''
        if(User_orders.objects.filter(package_gig_name= gig_details,order_by=order_by_user,order_to=order_to_user,offer_id=offer_details).exists() == True):
            order_details = User_orders.objects.get(package_gig_name= gig_details,order_by=order_by_user,order_to=order_to_user,offer_id=offer_details)
            data = str(order_details.order_no)
        else:
           data = "not exits"
        return HttpResponse(data)
    
    
def get_date_range_data_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
        data_all = request.GET['data_all']
        category = request.GET['category']
        cat_active = request.GET['cat_active']
        userdetails = User.objects.get(pk = userid)
        data = []
        if(data_all== "all"):
            user_transaction = User_Transactions.objects.filter(paid_by = userdetails)            
            for tran in user_transaction:
                used_credit = '0.0'
                withdra_amount = '0.0'
                try:
                    refund_det = User_Refund.objects.get(transaction = tran)
                    used_credit = str(float(refund_det.credit_used))
                    withdra_amount = str(float(refund_det.withdrawn_amount))
                except:
                    used_credit = '0.0'
                    withdra_amount = '0.0'
                date_val = (tran.transaction_date).date()
                data.append({"t_date":date_val,"t_id":tran.transaction_id,"t_category":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name,"t_order_no":tran.order_no.order_no,"t_currency":"USD","t_amount":tran.total_amount,"t_status":tran.transaction_status,"t_credits":used_credit,"tp_credits":tran.credits_used,"t_type":tran.payment_type,"t_base_price":tran.offer_amount,"t_withdrawal":withdra_amount})
        elif(cat_active== "yes"):
            sub_sub_cat_inst = SubSubCategories.objects.get(sub_sub_category_Name = category)
            user_transaction = User_Transactions.objects.filter(paid_by = userdetails)
            for tran in user_transaction:
                used_credit = '0.0'
                withdra_amount = '0.0'
                try:
                    refund_det = User_Refund.objects.get(transaction = tran)
                    used_credit = str(float(refund_det.credit_used))
                    withdra_amount = str(float(refund_det.withdrawn_amount))
                except:
                    used_credit = '0.0'
                    withdra_amount = '0.0'
                t_category = tran.gig_name.gig_sub_category.sub_sub_category_Name
                if(category == t_category):
                    date_val = (tran.transaction_date).date()
                    data.append({"t_date":date_val,"t_id":tran.transaction_id,"t_category":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name,"t_order_no":tran.order_no.order_no,"t_currency":"USD","t_amount":tran.total_amount,"t_status":tran.transaction_status,"t_credits":used_credit,"tp_credits":tran.credits_used,"t_type":tran.payment_type,"t_base_price":tran.offer_amount,"t_withdrawal":withdra_amount})
        else:
            start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
            end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
            user_transaction = User_Transactions.objects.filter(paid_by = userdetails,transaction_date__range=(start_date, end_date))
            for tran in user_transaction:
                used_credit = '0.0'
                withdra_amount = '0.0'
                try:
                    refund_det = User_Refund.objects.get(transaction = tran)
                    used_credit = str(float(refund_det.credit_used))
                    withdra_amount = str(float(refund_det.withdrawn_amount))
                except:
                    used_credit = '0.0'
                    withdra_amount = '0.0'
                date_val = (tran.transaction_date).date()
                data.append({"t_date":date_val,"t_id":tran.transaction_id,"t_category":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name,"t_order_no":tran.order_no.order_no,"t_currency":"USD","t_amount":tran.total_amount,"t_status":tran.transaction_status,"t_credits":used_credit,"tp_credits":tran.credits_used,"t_type":tran.payment_type,"t_base_price":tran.offer_amount,"t_withdrawal":withdra_amount})
        return JsonResponse(data,safe=False)

def post_activate_gig_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        gig_id = request.GET['gig_id']
        userDetails =  User.objects.get(pk=userid)
        gigDetails =  UserGigs.objects.get(pk=gig_id , user_id = userDetails)
        gigDetails.gig_status = 'active'
        gigDetails.save()
        return HttpResponse('sucess')

@csrf_exempt
def post_draft_object_view(request):
    if request.method == 'POST': 
        d_message = request.POST.get("delivery_message")
        d_images = request.POST.get("delivery_images")
        d_orde_no = request.POST.get("order_no")
        order_details = User_orders.objects.get(order_no=d_orde_no)
        delivered_by  = User.objects.get(pk=order_details.order_to.id)
        delivered_to  = User.objects.get(pk=order_details.order_by.id)
        order_offer_details = Request_Offers.objects.get(pk = order_details.offer_id.pk)
        delivery_count = Order_Delivery.objects.filter(order_no=order_details).count()
        orde_delivery = Order_Delivery(delivery_message=d_message,attachment=d_images,order_no=order_details,delivered_by=delivered_by,delivered_to=delivered_to,delivery_status="draft",total_revision= order_offer_details.no_revisions,current_revision = int(delivery_count) + 1)
        orde_delivery.save()
        return HttpResponse('sucess')    
    
@csrf_exempt
def post_delivered_object_view(request):
    if request.method == 'POST': 
        d_message = request.POST.get("delivery_message")
        d_images = request.POST.get("delivery_images")
        d_orde_no = request.POST.get("order_no")
        order_details = User_orders.objects.get(order_no=d_orde_no)
        delivered_by  = User.objects.get(pk=order_details.order_to.id)
        delivered_to  = User.objects.get(pk=order_details.order_by.id)
        order_details.order_status= 'delivered'
        order_details.save()
        try:    
            cover_detls = Order_Conversation.objects.get(initiator=delivered_to,receiver = delivered_by)
        except:
            cover_detls = Order_Conversation.objects.get(initiator=delivered_by,receiver = delivered_to)
        order_message = Order_Message(sender=delivered_by,receiver=delivered_to,text = "delivery",conversation_id=cover_detls,order_no=order_details,message_type="activity",is_read = True)
        order_message.save()
        get_message =  Order_Message.objects.get(pk = order_message.pk)
        today_date = datetime.today()
        last_date = today_date + timedelta(days=2)
        resolution = User_Order_Resolution(resolution_type="delivered",resolution_text = "Delivery",resolution_message="Delivered",resolution_desc="successfuly delivered",resolution_status="pending",order_no=order_details,raised_by=delivered_by,raised_to=delivered_to,message=get_message, resolution_last_date= last_date)
        resolution.save()
        get_resolution =  User_Order_Resolution.objects.get(pk = resolution.pk)
        order_offer_details = Request_Offers.objects.get(pk = order_details.offer_id.pk)
        delivery_count = Order_Delivery.objects.filter(order_no=order_details).count()
        orde_delivery = Order_Delivery(delivery_message=d_message,attachment=d_images,order_no=order_details,delivered_by=delivered_by,delivered_to=delivered_to,delivery_status="delivered",resolution= get_resolution,total_revision= order_offer_details.no_revisions,current_revision = int(delivery_count) + 1)
        orde_delivery.save()
        order_ativity = User_Order_Activity(order_message = "×1 Order Delivered" , order_no=order_details,activity_type="delivered",activity_by=delivered_by,activity_to=delivered_to)
        order_ativity.save()
        notification_delivered = Notification_commands.objects.get(slug = "order_delivered")
        if(notification_delivered.is_active == True):
            noti_create = CustomNotifications(sender = delivered_by, recipient= delivered_to, verb='order',order_no = order_details,description= str(delivered_by.username).title() + " Delivered the order.")
            noti_create.save()
        if(delivered_to.mail_order == True):
            mail_content = MailTemplates.order_delivered(str(delivered_to.username).title(),"Here, is your Delivery.",str("#"+order_details.order_no))
            SendEmailAct(str(delivered_to.email),mail_content,"Consider it done: Your order "+str("#"+order_details.order_no)+" is ready for your review.")
        return HttpResponse('sucess')

    
@csrf_exempt
def post_resolutions_view(request):
    if request.method == 'POST': 
        res_type = request.POST.get("res_type")
        res_text = request.POST.get("res_text")
        res_message = request.POST.get("res_message")
        res_desc = request.POST.get("res_desc")
        res_days = request.POST.get("res_days")
        raised_by = request.POST.get("raised_by")
        raised_by_user = User.objects.get(username = raised_by)
        order_no = request.POST.get("order_no")
        order_details = User_orders.objects.get(order_no=order_no)
        if(raised_by_user.username != order_details.order_by.username):
            raised_to =  User.objects.get(username = order_details.order_by.username)
        else:
            raised_to =  User.objects.get(username = order_details.order_to.username)
        cover_detls = ''
        prev_date = ''
        new_date = ''
        if(res_type == "extention"):
            notification_extension = Notification_commands.objects.get(slug = "extension_request")
            if(notification_extension.is_active == True):
                noti_create = CustomNotifications(sender = raised_by_user, recipient= raised_to, verb='order',order_no = order_details,description= str(raised_by_user.username).title() + " Requested to Extend Delivery Date.")
                noti_create.save()
            prev_date =  datetime.strptime(order_details.due_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            new_date = prev_date + timedelta(days=int(res_days))
            if(raised_to.mail_order == True):
                mail_content = MailTemplates.order_extension(str(raised_by_user.username).title(),str(raised_to.username).title(),str("#"+order_details.order_no))
                SendEmailAct(str(raised_to.email),mail_content," Note: Extension Request from " + str(raised_by_user.username)) 
        else:
            notification_cancellation = Notification_commands.objects.get(slug = "cancellation_request")
            if(notification_cancellation.is_active == True):
                noti_create = CustomNotifications(sender = raised_by_user, recipient= raised_to, verb='order',order_no = order_details,description= str(raised_by_user.username).title() + " Requested to Cancel This Order.")
                noti_create.save()
            prev_date = datetime.today()
            new_date = datetime.today()
        try:    
            cover_detls = Order_Conversation.objects.get(initiator=raised_by_user,receiver = raised_to)
        except:
            cover_detls = Order_Conversation.objects.get(initiator=raised_to,receiver = raised_by_user)
        order_message = Order_Message(sender=raised_by_user,receiver=raised_to,text = res_message,conversation_id=cover_detls,order_no=order_details,message_type="activity",is_read = True)
        order_message.save()
        next_date = ''
        get_message =  Order_Message.objects.get(pk = order_message.pk)
        today_date = datetime.today()
        last_date = today_date + timedelta(days=2)
        resolution= User_Order_Resolution(resolution_type=res_type,resolution_text = res_text,resolution_message=res_message,resolution_desc=res_desc,resolution_status="pending",order_no=order_details,resolution_days=res_days,raised_by=raised_by_user,raised_to=raised_to,message=get_message,ext_prev_date= prev_date,ext_new_date=new_date, resolution_last_date= last_date)
        resolution.save()
        return HttpResponse('sucess')



@csrf_exempt
def post_order_upload_view(request):
    if request.method == 'POST':
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return HttpResponse(res)
        else:
            if existingPath == 'null':
                fileName = str(shortuuid.ShortUUID().random(length=15)) +"_"+ str(fileName)[0:8]  + pathlib.Path(fileName).suffix 
                path = 'media/order_files/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                FileFolder = UploadFile()
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return HttpResponse(res)
            else:
                path = 'media/order_files/' + existingPath
                model_id = UploadFile.objects.get(existingPath=existingPath)
                if model_id.existingPath == existingPath:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':existingPath})
                        else:
                            res = JsonResponse({'existingPath':existingPath})    
                        return HttpResponse(res)
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return HttpResponse(res)
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return HttpResponse(res)
        



@csrf_exempt
def post_delivery_order_upload_view(request):
    if request.method == 'POST':
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return HttpResponse(res)
        else:
            if existingPath == 'null':
                fileName = str(shortuuid.ShortUUID().random(length=15)) +"_"+ str(fileName)[0:8]  + pathlib.Path(fileName).suffix 
                path = 'media/delivery/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                FileFolder = UploadFile()
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return HttpResponse(res)
            else:
                path = 'media/delivery/' + existingPath
                model_id = UploadFile.objects.get(existingPath=existingPath)
                if model_id.existingPath == existingPath:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':existingPath})
                        else:
                            res = JsonResponse({'existingPath':existingPath})    
                        return HttpResponse(res)
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return HttpResponse(res)
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return HttpResponse(res)


def get_all_order_messages_view(request):
    if request.method == 'GET':
        order_no = request.GET['order_no']
        conver_id = request.GET['conver_id']
        count_val = request.GET['current_count']
        id_list = request.GET['id_list']
        data = []
        try:
            delivery_no=0
            order_details = User_orders.objects.get(order_no = order_no)
            cover_detls =  Order_Conversation.objects.get(pk = conver_id)
            last_id = 0
            first_id = 0
            array_list = ''
            total_counts = Order_Message.objects.filter(conversation_id= cover_detls, order_no= order_details).count()
            # a_message = Order_Message.objects.filter(conversation_id= cover_detls, order_no= order_details).order_by('-pk')
            # for a_m in a_message:
            #     array_list.append(int(a_m.pk))
            array_list =     ",".join(str(msg.pk) for msg in Order_Message.objects.filter(conversation_id= cover_detls, order_no= order_details).order_by('-pk'))
            if(id_list == "start"):
                all_messages = Order_Message.objects.filter(conversation_id= cover_detls, order_no= order_details).order_by('-pk')[:int(count_val)]
            else:
                idlists = id_list.split(",")
                all_messages = Order_Message.objects.filter(conversation_id= cover_detls, order_no= order_details,id__in=idlists).order_by('-pk')
            attachment_str = ''
            for all_m in all_messages:
                if(all_m.message_type == "chat"):
                    if(all_m.attachment != None):
                        if(len(all_m.attachment.strip()) != 0):
                            attachment_str = all_m.attachment.strip()
                        else:
                            attachment_str = "None"
                    else:
                        attachment_str = "None"
                    data.append({"mssg_id":all_m.pk,"mssg_type":"chat","sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"attachment":attachment_str,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp})
                else:
                    reolution_details = User_Order_Resolution.objects.filter(message=all_m).first()
                    if(reolution_details != None):
                        delivery_description= ''
                        delivery_images= ''
                        message_str = ''
                        if(reolution_details.resolution_type == "delivered"):
                            order_del_details = Order_Delivery.objects.get(resolution = reolution_details)
                            delivery_description = order_del_details.delivery_message
                            delivery_images= order_del_details.attachment
                            message_str = ''
                            delivery_no = delivery_no + 1
                        else:
                            message_str = reolution_details.resolution_desc
                        data.append({"mssg_id":all_m.pk,"mssg_type":"activity","sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"attachment":attachment_str,"receiver_name":all_m.receiver.username,"res_type":reolution_details.resolution_type,"res_status":reolution_details.resolution_status,"reciever_username":all_m.receiver.username,"reciever_img":all_m.receiver.avatar,"res_message":message_str,"res_prev_date":reolution_details.ext_prev_date,"res_next_date":reolution_details.ext_new_date,"res_last_date":reolution_details.resolution_last_date,"mssg_time":all_m.timestamp,"res_id":reolution_details.id,"del_descrp":delivery_description, "del_images":delivery_images,"delivery_No":delivery_no,"cancel_mssg":reolution_details.resolution_cancel_mssg})
            data.sort(key=operator.itemgetter('mssg_time'))
            response_data = {"data":data, "total_count":total_counts,"current_count":count_val,"message_ids":array_list}
        except Exception as e:
            response_data = {"data":(str(type(e)) + str(e))}
        return JsonResponse(response_data,safe=False)



def post_accept_click_view(request):
    if request.method == 'GET':
        res_id = request.GET['res_id']
        res_type = request.GET['res_type']
        pre_date = request.GET['pre_date']
        next_date = request.GET['next_date']
        res_details = User_Order_Resolution.objects.get(id = res_id)
        res_details.resolution_status = 'accepted'
        res_details.save()
        data = []
        try:
            if(res_type == "extention"):
                raised_by = User.objects.get(username = res_details.raised_by.username)
                raised_to = User.objects.get(username = res_details.raised_to.username)
                order_details = User_orders.objects.get(order_no = res_details.order_no)
                order_details.due_date = next_date
                order_details.save()
                order_ativity = User_Order_Activity(order_message = "×1 Extended Delivery Time" , order_no=order_details,activity_type="extension",activity_by=raised_by,activity_to=raised_to)
                order_ativity.save()
                notification_extension = Notification_commands.objects.get(slug = "order_extended")
                if(notification_extension.is_active == True):
                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order',order_no = order_details,description= str(raised_to.username).title() + " agreed to extend Due Date.")
                    noti_create.save()
                if(raised_by.mail_order == True):
                    mail_content = MailTemplates.order_extension_accepted(str(raised_by.username).title(),str(raised_to.username).title(),str("#"+order_details.order_no))
                    SendEmailAct(str(raised_by.email),mail_content,"Order Extension has been Approved by " + str(raised_to.username).title() + ".")
            elif(res_type == "cancel"):
                order_details = User_orders.objects.get(order_no = res_details.order_no)
                order_details.order_status = 'cancel'
                order_details.incoming_request = 'site'
                order_details.save()
                raised_by = User.objects.get(username = res_details.raised_by.username)
                raised_to = User.objects.get(username = res_details.raised_to.username)
                order_by_user = User.objects.get(username= order_details.order_by.username)
                order_to_user = User.objects.get(username= order_details.order_to.username)
                transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                transaction.transaction_status = "cancelled"
                transaction.save()
                refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res_details,order_no=order_details,transaction=transaction ,user_id=order_by_user,refund_status= 'cancelled')
                refund_details.save()
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                except:
                    cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)   
                order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "Order Cancelled by " + str(raised_to.username).title(),conversation_id=cover_detls,order_no=order_details,message_type="chat",is_read = True)
                order_message.save()
                order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                order_ativity.save()
                earning_val = 0
                if(float(order_details.order_amount) < 40):
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
                order_by =  User.objects.get(username= order_details.order_by.username)   
                order_to =  User.objects.get(username= order_details.order_to.username)
                service_fees_price = 0
                if(float(order_details.order_amount) < 40):
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
                refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=None,clearence_status="cancelled",cleared_on=None,user_id=order_to,earning_type="cancelled",affiliate_user=None)
                refund_details.save()
                User_Order_Resolution.objects.filter(Q(raised_by = raised_by, raised_to= raised_to,resolution_status="pending",order_no = order_details) | Q(raised_by = raised_to, raised_to= raised_by,resolution_status="pending",order_no = order_details)).update(resolution_status="rejected", resolution_cancel_mssg = "Order Cancelled.")
                notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                if(notification_cancel.is_active == True):
                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details,description= str(raised_to.username).title() + " cancelled the Order.")
                    noti_create.save()
                if(order_by.mail_order == True):
                    mail_content = MailTemplates.order_cancelled_buyer(str(order_by.username).title(),str("#"+order_details.order_no))
                    SendEmailAct(str(order_by.email),mail_content,"Your order has been cancelled.")
                if(order_to.mail_order == True):
                    mail_content = MailTemplates.order_cancelled_seller(str(order_to.username).title(),str(order_by.username).title(),str("#"+order_details.order_no))
                    SendEmailAct(str(order_to.email),mail_content,"Your order has been cancelled.")       
            elif(res_type == "delivered"):
                raised_by = User.objects.get(username = res_details.raised_by.username)
                raised_to = User.objects.get(username = res_details.raised_to.username)
                order_details = User_orders.objects.get(order_no = res_details.order_no)
                notification_delivery = Notification_commands.objects.get(slug = "order_completed")
                if(notification_delivery.is_active == True):
                    noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details,description= str(raised_to.username).title() + " Marked your Order as complete.")
                    noti_create.save()
                service_fees_price = 0
                if(float(order_details.order_amount) < 40):
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
                withdrwal_val = 0
                withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days") )
                for ext in withdrawal_ext:
                    if(ext.parameter_name == "withdrawal_clearence_days"):
                        withdrwal_val = ext.no_of_days
                today_date = datetime.today()
                clearencedate = today_date + timedelta(days=int(withdrwal_val))                
                order_details.order_status = 'completed'
                order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                order_details.save()
                transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                transaction.transaction_status = "completed"
                transaction.save()
                offer_details = Request_Offers.objects.get(pk = order_details.offer_id.pk)
                order_by =  User.objects.get(username= order_details.order_by.username)   
                order_to =  User.objects.get(username= order_details.order_to.username)
                order_to.u_last_delivery= datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                order_to.save()
                User_Order_Resolution.objects.filter(Q(raised_by = order_to, raised_to= order_by,resolution_status="pending",order_no = order_details) | Q(raised_by = order_by, raised_to= order_to,resolution_status="pending",order_no = order_details)).update(resolution_status="rejected", resolution_cancel_mssg = "Order Completed.")
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
                except:
                    cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)   
                earnings_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=clearencedate,clearence_status="pending",cleared_on=None,user_id=order_to,earning_type="order",affiliate_user=None)
                earnings_details.save()
                order_message = Order_Message(sender=order_by,receiver=order_to,text = "Order is completed.",conversation_id=cover_detls,order_no=order_details,message_type="activity",is_read = True)
                order_message.save()
                get_message =  Order_Message.objects.get(pk = order_message.pk)
                resolution= User_Order_Resolution(resolution_type="completed",resolution_text = "Completed",resolution_message="Completed",resolution_desc=str(order_by.username) +" Marked as Completed.",resolution_status="accepted",order_no=order_details,raised_by=order_by,raised_to=order_to,message=get_message)
                resolution.save()
                order_ativity = User_Order_Activity(order_message = "×1 Order Completed" , order_no=order_details,activity_type="completed",activity_by=order_by,activity_to=order_to)
                order_ativity.save()
                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earned_val , order_no=order_details,activity_type="pending",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
            data.append({"sucess" : str("sucess")})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(data,safe=False)
    
def post_decline_click_view(request):
    if request.method == 'GET':
        res_id = request.GET['res_id']
        res_type = request.GET['res_type']
        res_text = request.GET['res_text']
        res_details = User_Order_Resolution.objects.get(id = res_id)
        res_details.resolution_status = 'rejected'
        res_details.resolution_cancel_mssg = res_text
        res_details.save()
        raised_by = User.objects.get(username = res_details.raised_by.username)
        raised_to = User.objects.get(username = res_details.raised_to.username)
        order_details = User_orders.objects.get(order_no = res_details.order_no)
        if(res_details.resolution_type == "cancel"):
            notification_cancel_req = Notification_commands.objects.get(slug = "order_cancellation_request_declined")
            if(notification_cancel_req.is_active == True):
                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details ,description= "Your Order Cancellation Request has been Declined.")
                noti_create.save()
        elif(res_details.resolution_type == "extention"):
            notification_extension_req = Notification_commands.objects.get(slug = "order_extesnion_cancelled")
            if(notification_extension_req.is_active == True):
                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details ,description= "Your Order Extension Request has been Declined.")
                noti_create.save()
            if(raised_by.mail_order == True):
                mail_content = MailTemplates.order_extension_decline(str(raised_to.username).title(),str(raised_by.username).title(),str("#"+order_details.order_no),str(res_text).title())
                SendEmailAct(str(raised_by.email),mail_content,"Extension declined from " + str(raised_to.username).title() + ".")  
        elif(res_details.resolution_type == "delivered"):
            notification_extension_req = Notification_commands.objects.get(slug = "order_delivery_declined")
            if(notification_extension_req.is_active == True):
                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details ,description= str(raised_to.username).title() + " requested an Revision.")
                noti_create.save()
            if(raised_by.mail_order == True):
                mail_content = MailTemplates.revision_requested(str(raised_to.username).title(),str(raised_by.username).title(),str("#"+order_details.order_no))
                SendEmailAct(str(raised_by.email),mail_content,"Revision Requested by Buyer " + str(raised_by.username).title()+ ".")  
        return HttpResponse('sucess')
    

def post_confirm_warning_view(request):
    if request.method == 'GET':
        warning_id = request.GET['warning_id']
        war_details = User_warning.objects.get(id = warning_id)
        war_details.confirmed_status = True
        war_details.confirmed_on =  datetime.today()
        war_details.save()
        userdetails = User.objects.get(id = war_details.user_id.id)
        userdetails.profile_status = 'warning'
        userdetails.save()
        return HttpResponse('sucess')
    

def post_seller_review_view(request):
    if request.method == 'GET':
        order_no = request.GET['order_no']
        s_comm = request.GET['s_comm']
        s_serv = request.GET['s_serv']
        s_recomm = request.GET['s_recomm']
        s_review_txt = request.GET['s_review_txt']
        data = []
        try:
            ord_details = User_orders.objects.get(order_no = order_no)
            orderedby_user = User.objects.get(username = ord_details.order_by.username)
            orderedto_user = User.objects.get(username = ord_details.order_to.username)
            gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)  
            average_val =  round(float(int(int(s_comm) + int(s_serv)+ int(s_recomm)) / 3),2)
            if(Seller_Reviews.objects.filter(order_no=ord_details,s_review_from=orderedby_user,s_review_to=orderedto_user,package_gig_name= gig_details).exists() == False):
                seller_reviews = Seller_Reviews(communication=s_comm,recommendation=s_recomm,service=s_serv,average_val=average_val,seller_response="",review_message=s_review_txt,order_no=ord_details,package_gig_name= gig_details,s_review_from=orderedby_user,s_review_to=orderedto_user,buyer_resp_date=None)
                seller_reviews.save()
                notification_seller = Notification_commands.objects.get(slug = "order_seller_reviews")
                if(notification_seller.is_active == True):
                    noti_create = CustomNotifications(sender = orderedby_user, recipient=orderedto_user,order_no= ord_details, verb='reviews',description= str(orderedby_user.username).title() + " left a " +str(round(average_val)) + " star review.")  
                    noti_create.save()
            data.append({"sucess" : str("sucess")})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(data,safe=False)
    
def post_earning_details_view(request):
    if request.method == 'GET':
        username = request.GET['username']
        parameter = request.GET['parameter']
        param_type = request.GET['param_type']
        user_details = User.objects.get(username = username)
        data_details = []
        if(param_type == "transactions" and parameter == 'all_t'):
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type="e_cancel") | Q(activity_type= "withdrawal") | Q(activity_type= "credit") | Q(activity_type= "pending") | Q(activity_type= "tip") | Q(activity_type= "affiliate")| Q(activity_type= "used_credit"))
            for e_activity in order_activity:
                clearence_date = ''
                if(e_activity.activity_type == "pending"):
                    earning_details = User_Earnings.objects.get(user_id= user_details, order_no=e_activity.order_no.pk,earning_amount=e_activity.order_amount)
                    clearence_date = str(earning_details.clearence_date.strftime('%d-%b-%Y'))
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter == 'withdrawal'):
            clearence_date = ''
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type= "withdrawal"))
            for e_activity in order_activity:
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter == 'used_credit'):
            clearence_date = ''
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type= "used_credit"))
            for e_activity in order_activity:
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter == 'tip'):
            clearence_date = ''
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type= "tip"))
            for e_activity in order_activity:
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter == 'pending'):
            clearence_date = ''
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type= "pending"))
            for e_activity in order_activity:
                earning_details = User_Earnings.objects.get(user_id= user_details, order_no=e_activity.order_no.pk,earning_amount=e_activity.order_amount)
                clearence_date = str(earning_details.clearence_date.strftime('%d-%b-%Y'))
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter == 'e_cancel'):
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type= "e_cancel"))
            for e_activity in order_activity:
                clearence_date = ''
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter =='credit'):
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details).filter(Q(activity_type= "credit"))
            for e_activity in order_activity:
                clearence_date = ''
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "transactions" and parameter =='affiliate'):
            order_activity = User_Order_Activity.objects.filter( activity_to=user_details).filter(Q(activity_type= "affiliate"))
            for e_activity in order_activity:
                clearence_date = ''
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_order_no":e_activity.order_no.order_no,"a_amount":e_activity.order_amount,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "year"):
            order_activity = User_Order_Activity.objects.filter(activity_to=user_details,activity_date__year = int(parameter)).filter(Q(activity_type="e_cancel") | Q(activity_type= "withdrawal") | Q(activity_type= "credit") | Q(activity_type= "pending") | Q(activity_type= "tip")| Q(activity_type= "affiliate")| Q(activity_type= "used_credit"))
            for e_activity in order_activity:
                clearence_date = ''
                if(e_activity.activity_type == "pending"):
                    earning_details = User_Earnings.objects.get(user_id= user_details, order_no=e_activity.order_no.pk,earning_amount=e_activity.order_amount)
                    clearence_date = str(earning_details.clearence_date.strftime('%d-%b-%Y'))
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_amount":e_activity.order_amount,"a_order_no":e_activity.order_no.order_no,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        elif(param_type == "month"):
            if(parameter != "all"):
                my_date = date(2022, int(parameter), 2)
                order_activity = User_Order_Activity.objects.filter( activity_to=user_details,activity_date__month = int(parameter)).filter(Q(activity_type="e_cancel") | Q(activity_type= "withdrawal") | Q(activity_type= "credit") | Q(activity_type= "pending") | Q(activity_type= "tip")| Q(activity_type= "affiliate")| Q(activity_type= "used_credit"))
            else:
                order_activity = User_Order_Activity.objects.filter( activity_to=user_details).filter(Q(activity_type="e_cancel") | Q(activity_type= "withdrawal") | Q(activity_type= "credit") | Q(activity_type= "pending") | Q(activity_type= "tip")| Q(activity_type= "affiliate")| Q(activity_type= "used_credit"))
            for e_activity in order_activity:
                clearence_date = ''
                if(e_activity.activity_type == "pending"):
                    earning_details = User_Earnings.objects.get(user_id= user_details, order_no=e_activity.order_no.pk,earning_amount=e_activity.order_amount)
                    clearence_date = str(earning_details.clearence_date.strftime('%d-%b-%Y'))
                data_details.append({"a_date":e_activity.activity_date,"a_message":e_activity.order_message,"a_amount":e_activity.order_amount,"a_order_no":e_activity.order_no.order_no,"a_type":e_activity.activity_type,"a_clear_date":clearence_date})
        return JsonResponse(data_details,safe=False)
    
def post_credit_tip_details_view(request):
    if request.method == 'GET':
        order_no = request.GET['order_no']
        base_price = request.GET['base_price']
        total_price = request.GET['total_price']
        fees = request.GET['fees']
        used_credits = request.GET['used_credits']
        ord_details = User_orders.objects.get(order_no = order_no)
        order_to = User.objects.get(username = ord_details.order_to.username)
        order_by = User.objects.get(username = ord_details.order_by.username)
        gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)
        offers_sent = Request_Offers.objects.get(pk= ord_details.offer_id.pk)
        refund_earning = User_Refund.objects.filter(user_id=order_by,refund_status="cancelled")
        current_val = float(used_credits)
        data = ''
        t_e_c_used = 0
        try:
            if(User_Earnings.objects.filter(order_amount= base_price,order_no=ord_details,user_id=order_to,earning_type='tip').exists() == False):
                if(float(current_val) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled").order_by("pk")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        prev_credit = 0.0
                        actual_available = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(round((actual_available)) != 0):
                                    if(float(current_val) <= float(actual_available)):
                                        previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                        current_val =  0.0
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                    elif(float(u_credit_used) > float(actual_available)):
                                        if(float(current_val) != 0.0):
                                            if(float(current_val) >= float(actual_available)):
                                                c_used_credit = float(actual_available) 
                                            else:
                                                c_used_credit = float(actual_available) - float(current_val)
                                            present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                            r_earn.credit_used = str(round(float(abs(present_credit)),2))
                                            r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            r_earn.save()
                                            current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user,clearence_status="cleared" ).order_by("pk")
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(round((actual_available)) != 0):
                                        if(float(current_val) <= float(actual_available)): 
                                            previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                            t_e_c_used = float(current_val)
                                            current_val =  0.0
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                        elif(float(current_val) > float(actual_available)):
                                            if(float(current_val) != 0.0):
                                                if(float(current_val) >= float(actual_available)):
                                                    c_used_credit = float(actual_available) 
                                                else:
                                                    c_used_credit = float(actual_available) - float(current_val)
                                                present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                                earn.credit_used = str(round(float(abs(present_credit)),2))
                                                earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                                earn.save()
                                                t_e_c_used = float(t_e_c_used) + float(c_used_credit)
                                                current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
                except:
                    cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)
                withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days") )
                for ext in withdrawal_ext:
                    if(ext.parameter_name == "withdrawal_clearence_days"):
                        withdrwal_val = ext.no_of_days
                        today_date = datetime.today()
                        clearencedate = today_date + timedelta(days=int(withdrwal_val)) 
                earning_val = 0
                if(float(base_price) < 40.0):
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Seller Fees"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  float(serv_fees_val)
                        else:
                            perceof_budg = float((float(base_price)* int(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                else:
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Seller Fees"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  float(serv_fees_val)
                        else:
                            perceof_budg = float((float(base_price)* float(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                if(float(t_e_c_used) != 0):
                    cre_order_activity = User_Order_Activity(order_message="×1 Credit Used for Tip.",order_amount=str(t_e_c_used),order_no = ord_details,activity_type="used_credit",activity_by=order_by,activity_to=order_by)
                    cre_order_activity.save()
                earning_val = float(earning_val) + (round(float(round(float(base_price),2) - service_fees_price),2)) 
                refund_details = User_Earnings(order_amount=base_price,earning_amount=earning_val,platform_fees=service_fees_price,aval_with="",clearence_date=clearencedate,clearence_status="pending",order_no= ord_details,cleared_on=None,user_id=order_to,earning_type="tip",affiliate_user=None)
                refund_details.save()
                u_trans_status = "successful"
                cs = shortuuid.ShortUUID(alphabet="0123456789")
                c_u_trans_id = cs.random(length=8)
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='credit',transaction_id=c_u_trans_id,payment_status=u_trans_status,payment_currency="USD",offer_amount=base_price,total_amount=used_credits,processing_fees= fees,paid_by=order_by,paid_to=order_to,order_no=ord_details,paid_for='tip',transaction_status="completed",credits_used=used_credits)
                user_trans.save()
                order_message = Order_Message(sender=order_by,receiver=order_to,text = "tip",conversation_id=cover_detls,order_no=ord_details,message_type="activity",is_read = True)
                order_message.save()
                get_message =  Order_Message.objects.get(pk = order_message.pk)
                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earning_val , order_no=ord_details,activity_type="pending",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
                order_ativity1 = User_Order_Activity(order_message = "Tip Provide by Buyer",order_amount = earning_val , order_no=ord_details,activity_type="tip",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
                notification_tip = Notification_commands.objects.get(slug = "order_tip_recieved")
                if(notification_tip.is_active == True):
                    noti_create = CustomNotifications(sender = order_by, recipient=order_to, verb='tip',description= str(order_by.username).title() + " left you a Tip.")  
                    noti_create.save()
                if(order_to.mail_order == True):
                    mail_content = MailTemplates.order_tip_received(str(order_by.username).title(),str(ord_details.package_gig_name.gig_title).title(),str(ord_details.package_gig_name.gig_category.category_Name).title(),str(order_to.username).title(),str(ord_details.order_no).title())
                    SendEmailAct(str(order_to.email),mail_content," Great news: Your received an tip from buyer "+str(order_by.username).title()+".") 
                data = "sucess"
        except Exception as e:
            data = str(type(e)) + str(e)
        return HttpResponse(data)


def post_flutter_tip_details_view(request):
    if request.method == 'GET':
        data = []
        order_no = request.GET['order_no']
        order_to_user = request.GET['order_to_user']
        status = request.GET['status']
        trans_ref = request.GET['trans_ref']
        trans_id = request.GET['trans_id']
        ord_details = User_orders.objects.get(order_no = order_no)
        order_to = User.objects.get(username = ord_details.order_to.username)
        order_by = User.objects.get(username = ord_details.order_by.username)
        refund_earning = User_Refund.objects.filter(user_id=order_by,refund_status="cancelled")
        gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)
        offer_details = Request_Offers.objects.get(pk = ord_details.offer_id.pk)
        api_details = Api_keys.objects.filter(api_name= "flutterwave").first()
        payment.token = api_details.secrete_key
        details = payment.get_payment_details(trans_id)
        flu_amout = details['data']['amount']
        flu_app_fee = details['data']['app_fee']
        flu_pay_type = details['data']['payment_type']
        flu_accnt_id = details['data']['account_id']
        flutt_flw_ref = details['data']['flw_ref']
        meta_data =  details['data']['meta']['data_extra']
        order_amount =  details['data']['meta']['base_price_wsdf']
        u_service_fees =  details['data']['meta']['token']
        current_val = float(meta_data)
        t_e_c_used = 0
        try:
            if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offer_details,paid_by=order_by,paid_to=order_to,paid_for='tip').exists() == False):
                if(float(meta_data) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled").order_by("pk")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        prev_credit = 0.0
                        actual_available = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(round((actual_available)) != 0):
                                    if(float(current_val) <= float(actual_available)):
                                        previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                        current_val =  0.0
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                    elif(float(u_credit_used) > float(actual_available)):
                                        if(float(current_val) != 0.0):
                                            if(float(current_val) >= float(actual_available)):
                                                c_used_credit = float(actual_available) 
                                            else:
                                                c_used_credit = float(actual_available) - float(current_val)
                                            present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                            r_earn.credit_used = str(round(float(abs(present_credit)),2))
                                            r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            r_earn.save()
                                            current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user,clearence_status="cleared" ).order_by("pk")
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(round((actual_available)) != 0):
                                        if(float(current_val) <= float(actual_available)): 
                                            previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                            t_e_c_used = float(current_val)
                                            current_val =  0.0
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                        elif(float(current_val) > float(actual_available)):
                                            if(float(current_val) != 0.0):
                                                if(float(current_val) >= float(actual_available)):
                                                    c_used_credit = float(actual_available) 
                                                else:
                                                    c_used_credit = float(actual_available) - float(current_val)
                                                present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                                earn.credit_used = str(round(float(abs(present_credit)),2))
                                                earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                                earn.save()
                                                t_e_c_used = float(t_e_c_used) + float(c_used_credit) 
                                                current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                if(float(t_e_c_used) != 0):
                    cre_order_activity = User_Order_Activity(order_message="×1 Credit Used for Tip.",order_amount=str(t_e_c_used),order_no = ord_details,activity_type="used_credit",activity_by=order_by,activity_to=order_by)
                    cre_order_activity.save()
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
                except:
                    cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)
                withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days"))
                earning_val = 0
                if(float(order_amount) < 40.0):
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Seller Fees"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  float(serv_fees_val)
                        else:
                            perceof_budg = float((float(order_amount)* float(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                else:
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Seller Fees"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  float(serv_fees_val)
                        else:
                            perceof_budg = float((float(order_amount)* float(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                earning_val = float(earning_val) + (round(float(round(float(order_amount),2) - service_fees_price),2))
                for ext in withdrawal_ext:
                    if(ext.parameter_name == "withdrawal_clearence_days"):
                        withdrwal_val = ext.no_of_days
                        today_date = datetime.today()
                        clearencedate = today_date + timedelta(days=int(withdrwal_val))
                refund_details = User_Earnings(order_amount=order_amount,earning_amount=earning_val,platform_fees=service_fees_price,aval_with="",clearence_date=clearencedate,clearence_status="pending",order_no= ord_details,cleared_on=None,user_id=order_to,earning_type="tip",affiliate_user=None)
                refund_details.save()
                order_message = Order_Message(sender=order_by,receiver=order_to,text = "tip",conversation_id=cover_detls,order_no=ord_details,message_type="activity",is_read = True)
                order_message.save()
                get_message =  Order_Message.objects.get(pk = order_message.pk)
                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earning_val , order_no=ord_details,activity_type="pending",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
                order_ativity1 = User_Order_Activity(order_message = "Tip Provide by Buyer",order_amount = earning_val , order_no=ord_details,activity_type="tip",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offer_details,payment_type='flutterwave',transaction_id=trans_id,payment_status=status,transaction_ref= trans_ref,payment_currency="USD",offer_amount=order_amount,total_amount=flu_amout,processing_fees= u_service_fees,credits_used=meta_data,flutter_fluw_ref= flutt_flw_ref,flutter_account_id=flu_accnt_id,flutter_app_fee=flu_app_fee,flutter_pay_type=flu_pay_type,paid_by=order_by,paid_to=order_to,order_no=ord_details,paid_for='tip',transaction_status="completed")
                user_trans.save()
                notification_settings = Notification_commands.objects.get(slug = "payment_sucessful")
                if(notification_settings.is_active == True):
                    sender = User.objects.get(username = 'admin')
                    noti_create = CustomNotifications(sender = sender, recipient=order_by, verb='payment',description="Your Card payment is sucessful.") 
                    noti_create.save()
                notification_tip = Notification_commands.objects.get(slug = "order_tip_recieved")
                if(notification_tip.is_active == True):
                    noti_create = CustomNotifications(sender = order_by, recipient=order_to, verb='tip',description= str(order_by.username).title() + " left you a Tip.")  
                    noti_create.save()
                if(order_to.mail_order == True):
                    mail_content = MailTemplates.order_tip_received(str(order_by.username).title(),str(ord_details.package_gig_name.gig_title).title(),str(ord_details.package_gig_name.gig_category.category_Name).title(),str(order_to.username).title(),str(ord_details.order_no).title())
                    SendEmailAct(str(order_to.email),mail_content," Great news: Your received an tip from buyer "+str(order_by.username).title()+".") 
                data.append({'sucess' : 'sucess'})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)

    
def post_paypal_tip_details_view(request):
    if request.method == 'GET':
        data = []
        order_to_user = request.GET['order_to_user']
        order_no = request.GET['order_no']
        payer_id = request.GET['payer_id']
        payer_email = request.GET['payer_email']
        trans_id = request.GET['trans_id']
        trans_status = request.GET['trans_status']
        base_price = request.GET['base_price']
        total_price = request.GET['total_price']
        service_fees = request.GET['service_fees']
        used_credits = request.GET['used_credits']
        ord_details = User_orders.objects.get(order_no = order_no)
        order_to = User.objects.get(username = ord_details.order_to.username)
        order_by = User.objects.get(username = ord_details.order_by.username)
        refund_earning = User_Refund.objects.filter(user_id=order_by,refund_status="cancelled")
        gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)
        offer_details = Request_Offers.objects.get(pk = ord_details.offer_id.pk)
        t_e_c_used = 0
        try:
            current_val = float(used_credits)
            if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offer_details,paid_by=order_by,paid_to=order_to,paid_for='tip').exists() == False):
                if(float(used_credits) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled").order_by("pk")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        prev_credit = 0.0
                        actual_available = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(round((actual_available)) != 0):
                                    if(float(current_val) <= float(actual_available)):
                                        previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                        current_val =  0.0
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                    elif(float(u_credit_used) > float(actual_available)):
                                        if(float(current_val) != 0.0):
                                            if(float(current_val) >= float(actual_available)):
                                                c_used_credit = float(actual_available) 
                                            else:
                                                c_used_credit = float(actual_available) - float(current_val)
                                            present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                            r_earn.credit_used = str(round(float(abs(present_credit)),2))
                                            r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            r_earn.save()
                                            current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user,clearence_status="cleared" ).order_by("pk")
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(round((actual_available)) != 0):
                                        if(float(current_val) <= float(actual_available)): 
                                            previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                            current_val =  0.0
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            t_e_c_used = float(current_val)
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                        elif(float(current_val) > float(actual_available)):
                                            if(float(current_val) != 0.0):
                                                if(float(current_val) >= float(actual_available)):
                                                    c_used_credit = float(actual_available) 
                                                else:
                                                    c_used_credit = float(actual_available) - float(current_val)
                                                present_credit = float(abs(c_used_credit)) + float(prev_credit)
                                                earn.credit_used = str(round(float(abs(present_credit)),2))
                                                earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                                earn.save()
                                                t_e_c_used = float(t_e_c_used) + float(c_used_credit) 
                                                current_val = round(float(current_val) - float(abs(c_used_credit)),2)
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
                except:
                    cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)
                withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days"))
                earning_val = 0
                if(float(base_price) < 40.0):
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Seller Fees"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  float(serv_fees_val)
                        else:
                            perceof_budg = float((float(base_price)* float(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                else:
                    payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Tip Seller Fees"))
                    for p in payment_parameters:
                        serv_fees_val = p.service_fees
                        serv_fees_type = p.fees_type
                        if(serv_fees_type == "flat"):
                            service_fees_price =  float(serv_fees_val)
                        else:
                            perceof_budg = float((float(base_price)* float(serv_fees_val))/100)
                            service_fees_price = round(perceof_budg,2)
                earning_val = float(earning_val) + (round(float(round(float(base_price),2) - service_fees_price),2))
                for ext in withdrawal_ext:
                    if(ext.parameter_name == "withdrawal_clearence_days"):
                        withdrwal_val = ext.no_of_days
                        today_date = datetime.today()
                        clearencedate = today_date + timedelta(days=int(withdrwal_val))
                if(float(t_e_c_used) != 0):
                    cre_order_activity = User_Order_Activity(order_message="×1 Credit Used for Tip.",order_amount=str(t_e_c_used),order_no = ord_details,activity_type="used_credit",activity_by=order_by,activity_to=order_by)
                    cre_order_activity.save()
                refund_details = User_Earnings(order_amount=base_price,earning_amount=earning_val,platform_fees=service_fees_price,aval_with="",clearence_date=clearencedate,clearence_status="pending",order_no= ord_details,cleared_on=None,user_id=order_to,earning_type="tip",affiliate_user=None)
                refund_details.save()
                order_message = Order_Message(sender=order_by,receiver=order_to,text = "tip",conversation_id=cover_detls,order_no=ord_details,message_type="activity",is_read = True)
                order_message.save()
                get_message =  Order_Message.objects.get(pk = order_message.pk)
                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earning_val , order_no=ord_details,activity_type="pending",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
                order_ativity1 = User_Order_Activity(order_message = "Tip Provide by Buyer",order_amount = earning_val , order_no=ord_details,activity_type="tip",activity_by=order_by,activity_to=order_to)
                order_ativity1.save()
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offer_details,payment_type='paypal',transaction_id=trans_id,payment_status=trans_status,payment_currency="USD",offer_amount=base_price,total_amount=total_price,processing_fees= service_fees,paypal_id=payer_id,paypal_email=payer_email,paid_by=order_by,paid_to=order_to,order_no=ord_details,paid_for='tip',transaction_status="completed",credits_used=used_credits)
                user_trans.save()
                notification_settings = Notification_commands.objects.get(slug = "payment_sucessful")
                if(notification_settings.is_active == True):
                    sender = User.objects.get(username = 'admin')
                    noti_create = CustomNotifications(sender = sender, recipient=order_by, verb='payment',description="Your Paypal payment is sucessful.")
                    noti_create.save()
                notification_tip = Notification_commands.objects.get(slug = "order_tip_recieved")
                if(notification_tip.is_active == True):
                    noti_create = CustomNotifications(sender = order_by, recipient=order_to, verb='tip',description= str(order_by.username).title() + " left you a Tip.")  
                    noti_create.save()
                if(order_to.mail_order == True):
                    mail_content = MailTemplates.order_tip_received(str(order_by.username).title(),str(ord_details.package_gig_name.gig_title).title(),str(ord_details.package_gig_name.gig_category.category_Name).title(),str(order_to.username).title(),str(ord_details.order_no).title())
                    SendEmailAct(str(order_to.email),mail_content," Great news: Your received an tip from buyer "+str(order_by.username).title()+".") 
                data.append({'sucess' : 'sucess'})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)

        
def post_seller_response_view(request):
    if request.method == 'GET':
        seller_rev_id = request.GET['seller_rev_id']
        seller_rev_response = request.GET['seller_rev_response']
        seller_reviews = Seller_Reviews.objects.get(pk = seller_rev_id)
        seller_reviews.seller_response = seller_rev_response
        seller_reviews.buyer_resp_date =  datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        seller_reviews.save()
        return HttpResponse('sucess')
    
def post_buyer_review_view(request):
    if request.method == 'GET':
        order_no = request.GET['order_no']
        b_rating = request.GET['b_rating']
        b_review_txt = request.GET['b_review_txt']
        ord_details = User_orders.objects.get(order_no = order_no)
        data = []
        try:
            orderedby_user = User.objects.get(username = ord_details.order_by.username)
            orderedto_user = User.objects.get(username = ord_details.order_to.username)
            gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)
            if(Buyer_Reviews.objects.filter(order_no=ord_details,b_review_from=orderedto_user,b_review_to=orderedby_user,package_gig_name= gig_details).exists() == False):
                buyer_reviews = Buyer_Reviews(review_message=b_review_txt,rating_val=b_rating,order_no=ord_details,package_gig_name=gig_details,b_review_from=orderedto_user,b_review_to=orderedby_user)
                buyer_reviews.save()
                notification_buyer = Notification_commands.objects.get(slug = "order_buyer_reviews")
                if(notification_buyer.is_active == True):
                    noti_create = CustomNotifications(sender = orderedto_user, recipient=orderedby_user,order_no= ord_details, verb='reviews',description= str(orderedto_user.username).title() + " left a " +str(round(int(b_rating))) + " star review.")  
                    noti_create.save()
            data.append({'sucess' : 'sucess'})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)
    
    
def post_initiate_withdrawl_view(request):
    if request.method == 'GET':
        username = request.GET['username']
        available_balance = request.GET['available_balance'] 
        initiation_type = request.GET['initiation_type']
        pay_id = request.GET['pay_id']
        userDetails = User.objects.get(username = username)
        if(Withdrwal_initiated.objects.filter(user_id= userDetails,withdrawan_status="initiated",withdrawal_amount=str(round(float(available_balance),2)),initiated_type=initiation_type,withdrawn_date=None).exists() == False):
            withdrawal_initiated = Withdrwal_initiated(withdrawal_amount=round(float(available_balance),2),user_id= userDetails,withdrawan_status="initiated",withdrawn_date=None,initiated_type=initiation_type,with_email=pay_id )
            withdrawal_initiated.save()
            a_logging = AdminLogging(username=userDetails.username,reqst_message="Withdrawal is initiated Amount: " + str(round(float(available_balance),2)),reqst_details=str(withdrawal_initiated.pk),mail_address=userDetails.email,log_type="withdrawal")
            a_logging.save()
        return HttpResponse('sucess')
        
def post_check_conver_view(request):
    if request.method == 'GET':
        initiator = request.GET['initiator']
        receiver = request.GET['receiver'] 
        initiator = User.objects.get(username = initiator)
        receiver = User.objects.get(username = receiver)
        try:    
            message_cover_detls = Conversation.objects.get(initiator=initiator,receiver = receiver)
        except:
            try:
                message_cover_detls = Conversation.objects.get(initiator=receiver,receiver = initiator)
            except:
                message_cover_detls = Conversation(initiator=initiator,receiver=receiver,convers_type="active")
                message_cover_detls.save()    
        return HttpResponse('sucess')
    
def get_conv_user_details_view(request):
    if request.method == 'GET':
        receiver_user = request.GET['receiver_user']
        initiator_user = request.GET['initiator_user']
        count_val = request.GET['current_count']
        id_list = request.GET['id_list']
        initiator = User.objects.get(username = initiator_user)
        receiver = User.objects.get(username = receiver_user)
        try:    
            message_cover_detls = Conversation.objects.get(initiator=initiator,receiver = receiver)
        except:
            try:
                message_cover_detls = Conversation.objects.get(initiator=receiver,receiver = initiator)
            except:
                message_cover_detls = Conversation(initiator=initiator,receiver=receiver,convers_type="active")
                message_cover_detls.save()  
        conversational_details =   Conversation.objects.get(pk = message_cover_detls.pk)
        user_details =[]
        initiator_gigs = UserGigs.objects.filter(user_id=initiator, gig_status='active').count()
        receiver_gigs = UserGigs.objects.filter(user_id=receiver, gig_status='active').count()
        Message.objects.filter(conversation_id=conversational_details,is_read=False).update(is_read=True)       
        last_seen_time = Message_Response_Time.objects.filter(receiver=receiver).last()
        last_seen_time_str = ''
        if(last_seen_time != None):
            last_seen_time_str = timesince.timesince(last_seen_time.timestamp)  
        else:
            last_seen_time_str = "1 hour ago"
        messa_resp = Message_Response_Time(receiver=initiator, timestamp= datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        messa_resp.save()
        language_inst = Languages.objects.get(lng_Name = "English")
        user_langauges = UserLanguages.objects.filter(user_id= receiver, language_name=language_inst).first()
        seller_rating = 0
        buyer_rating = 0
        seller_reviews = 0
        buyer_reviews = 0
        seller_all_reviews = Seller_Reviews.objects.filter(s_review_to=receiver)
        for sa_review in seller_all_reviews:
            seller_rating = seller_rating + float(sa_review.average_val)
        try:
            seller_rating = round(float(round(seller_rating/len(seller_all_reviews),0)))
        except:
            seller_count = 0
        seller_reviews = len(seller_all_reviews)
        buyer_all_reviews = Buyer_Reviews.objects.filter(b_review_to=receiver)
        for by_review in buyer_all_reviews:
            buyer_rating = seller_rating + float(by_review.rating_val)
        try:
            buyer_rating = int(round(buyer_rating/len(buyer_all_reviews),0))
        except:
            buyer_rating = 0
        buyer_reviews = len(buyer_all_reviews)
        seller_level_string = str(receiver.user_level.level_name)
        user_details.append({"user_id":receiver.pk,"username":receiver.username,"userimg":receiver.avatar,"user_location":receiver.country.name,"user_start":receiver.created_at.strftime('%b %Y'),"user_english":user_langauges.lang_prof,"seller_level":seller_level_string,"response_time":receiver.avg_respons,"seller_rating":seller_rating,"buyer_rating":buyer_rating,"seller_reviews":seller_reviews,"buyer_reviews":buyer_reviews})
        order_details = []
        order_data = []
        array_list = ''
        current_count = 10
        total_counts = Message.objects.filter(conversation_id= conversational_details).count()
        # a_message = Message.objects.filter(conversation_id= conversational_details).order_by('-pk')
        # for a_m in a_message:
        #     array_list.append(int(a_m.pk))
        array_list =     ",".join(str(msg.pk) for msg in Message.objects.filter(conversation_id= conversational_details).order_by('-pk'))
        all_messages = Message.objects.filter(conversation_id= conversational_details).order_by('-pk')[:int(10)]
        message_data = []
        attachment_str = ''
        for all_m in all_messages:
            attachment_str = ''
            if(all_m.is_read == False):
                all_m.is_read = True
                all_m.save()
            if(all_m.message_type == "chat"):
                if(all_m.attachment != None):
                    if(len(all_m.attachment.strip()) != 0):
                        attachment_str = all_m.attachment.strip()
                    else:
                        attachment_str = "None"
                else:
                    attachment_str = "None"
                message_data.append({"mssg_type":"chat","mssg_id":all_m.pk,"sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"attachment":attachment_str,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp})
            else:
                if(all_m.message_type == "offer"):
                    offer_details = Request_Offers.objects.get(pk= all_m.request_offers_id.pk)
                    orders_details = User_orders.objects.filter(offer_id=offer_details).first()
                    offer_status = ""
                    order_no= ''
                    if(offer_details.offer_status_by_buyer == "active"):
                        offer_status = "active"
                    elif(offer_details.offer_status_by_buyer == "deleted"):
                        offer_status = "deleted"
                    if((orders_details) != None): 
                        offer_status = "ordered"
                        order_no = orders_details.order_no
                    gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
                    offer_data = []
                    message_data.append({ "mssg_type":"offer","mssg_id":all_m.pk,"sender_username":all_m.sender.username,"attachment":"None","sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp,"offer_id":offer_details.pk,"buyer_request_id":0,"gig_title":gig_details.gig_title,"offer_amount":offer_details.offer_budget,"offer_time":offer_details.offer_time,"offer_revision":offer_details.no_revisions,"offer_desc":offer_details.offer_desc,"extra_parameters":offer_details.extra_parameters,"offer_sender":offer_details.custom_user.username,"offer_status":offer_status,"order_no":order_no})
                elif(all_m.message_type == "quote"):
                    buyer_request = Buyer_Post_Request.objects.get(pk= all_m.buyer_request_id.pk)
                    service_time_str = ''
                    no_of_days = ''
                    due_date_str = ''
                    today_date = datetime.today()
                    if(buyer_request.service_time== "24hours"):
                        service_time_str = "24 dours"
                        no_of_days = 1
                        due_date_str = today_date + timedelta(days=int(no_of_days))
                        due_date_str = due_date_str.strftime('%b %d, %Y')
                    elif(buyer_request.service_time== "3days"):
                        service_time_str = "3 days"
                        no_of_days = 3
                        due_date_str = today_date + timedelta(days=int(no_of_days))
                        due_date_str = due_date_str.strftime('%b %d, %Y')
                    elif(buyer_request.service_time== "7days"):
                        service_time_str = "7 days"
                        no_of_days = 7
                        due_date_str = today_date + timedelta(days=int(no_of_days))
                        due_date_str = due_date_str.strftime('%b %d, %Y')
                    elif(buyer_request.service_time== "other"):
                        service_time_str = "Other"
                        due_date_str = ''
                    offer_data = []
                    offer_created_status = ''
                    try:
                        req_offers = Request_Offers.objects.get(buyer_request = buyer_request)
                        offer_created_status = "created"
                    except:
                        offer_created_status = "active"
                    message_data.append({"mssg_type":"quote","mssg_id":all_m.pk,"attachment":"None","sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp,"request_id":buyer_request.pk,"req_desc":buyer_request.service_desc,"req_time":service_time_str,"req_budget":buyer_request.service_budget,"req_due_date":due_date_str,"req_status":buyer_request.service_status,"offer_created_sta":offer_created_status})
        message_data.sort(key=operator.itemgetter('mssg_id'))
        order_details = User_orders.objects.filter(order_by=initiator,order_to = receiver , order_status="active")
        if(len(order_details) == 0):
            order_details = User_orders.objects.filter(order_by=receiver,order_to = initiator, order_status="active")
        current_User = ''
        for order in order_details:
            if(initiator.username == order.order_by.username):
                current_User = "Buyer"
            else:
                current_User = "Seller"
            gig_details = UserGigs.objects.get(gig_title=order.package_gig_name.gig_title)
            gig_image_url = ''
            gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            order_data.append({"order_id":order.pk,"order_no":order.order_no,"order_amount":order.order_amount,"order_due_date":order.due_date.strftime('%b %d, %Y'),"gig_img":gig_image_url,"order_status":order.order_status,"gig_title":order.package_gig_name.gig_title}) 
        response_data = {"response_userDetails":user_details,"conversation_id":conversational_details.pk,"no_of_orders":len(order_details),"curre_User":current_User,"order_details":order_data,"data_messages":message_data, "total_count":total_counts,"current_count":count_val,"message_ids":array_list,"initiator_gigs":initiator_gigs,"receiver_gigs":receiver_gigs,"last_seen_str":last_seen_time_str}
        return JsonResponse(response_data,safe=False)
    
@csrf_exempt
def post_inbox_upload_view(request):
    if request.method == 'POST':
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return HttpResponse(res)
        else:
            if existingPath == 'null':
                try:
                    fileName = str(shortuuid.ShortUUID().random(length=15)) +"_"+ str(fileName)[0:8]  + pathlib.Path(fileName).suffix 
                    path = 'media/chat_files/' + fileName
                    with open(path, 'wb+') as destination: 
                        destination.write(file)
                    FileFolder = UploadFile()
                    FileFolder.existingPath = fileName
                    FileFolder.eof = end
                    FileFolder.name = fileName
                    FileFolder.save()
                    if int(end):
                        res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                    else:
                        res = JsonResponse({'existingPath': fileName})
                except Exception as e:
                    res = JsonResponse({'existingPath': (str(type(e)) + str(e))})
                return HttpResponse(res)
            else:
                path = 'media/chat_files/' + existingPath
                model_id = UploadFile.objects.get(existingPath=existingPath)
                try:
                    if model_id.existingPath == existingPath:
                        if not model_id.eof:
                            with open(path, 'ab+') as destination: 
                                destination.write(file)
                            if int(end):
                                model_id.eof = int(end)
                                model_id.save()
                                res = JsonResponse({'data':'Uploaded Successfully','existingPath':existingPath})
                            else:
                                res = JsonResponse({'existingPath':existingPath})    
                            return HttpResponse(res)
                        else:
                            res = JsonResponse({'data':'EOF found. Invalid request'})
                            return HttpResponse(res)
                    else:
                        res = JsonResponse({'data':'No such file exists in the existingPath'})
                        return HttpResponse(res)
                except Exception as e:
                    res = JsonResponse({'data':(str(type(e)) + str(e))})
                    return HttpResponse(res)
        
def get_offer_details_view(request):
    if request.method == 'GET':
        o_offer_id = request.GET['o_offer_id']
        offer_details = Request_Offers.objects.get(pk= o_offer_id)
        gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
        offer_data = []
        offer_data.append({"offer_id":offer_details.pk,"gig_title":gig_details.gig_title,"offer_amount":offer_details.offer_budget,"offer_time":offer_details.offer_time,"offer_revision":offer_details.no_revisions,"offer_desc":offer_details.offer_desc,"extra_parameters":offer_details.extra_parameters,"offer_sender":offer_details.custom_user.username})
        return JsonResponse(offer_data,safe=False)

def post_decline_offer_view(request):
    if request.method == 'GET':
        o_offer_id = request.GET['o_offer_id']
        offer_details = Request_Offers.objects.get(pk= o_offer_id)
        offer_details.offer_status_by_buyer = "deleted"
        offer_details.save()
        return HttpResponse("sucess")
    

def post_conv_delete_view(request):
    if request.method == 'GET':
        o_conver_id = request.GET['conver_id']
        conv_details = Conversation.objects.get(pk= o_conver_id)
        conv_details.convers_type = "delete"
        conv_details.save()
        return HttpResponse("sucess")
    
def post_conv_block_view(request):
    if request.method == 'GET':
        o_conver_id = request.GET['conver_id']
        conv_details = Conversation.objects.get(pk= o_conver_id)
        conv_details.convers_type = "block"
        conv_details.save()
        return HttpResponse("sucess")
      
def get_all_contacts_view(request):
    if request.method == 'GET':
        o_category = request.GET['category']
        o_username = request.GET['username']
        data = []
        userDetails = User.objects.get(username = o_username)
        all_conversations = Conversation.objects.filter(Q(initiator=userDetails) | Q(receiver= userDetails))
        conversation_lists = []
        for all_c in all_conversations:
            receiver_name = ''
            last_messages = Message.objects.filter(conversation_id= all_c).last()
            if(last_messages != None):
                lastmessage_str = last_messages.text
                last_message_sender = last_messages.sender.username
                last_message_receiver = last_messages.receiver.username
                last_message_time = ''
                last_message_time = timesince.timesince(last_messages.timestamp)  
            else:
                lastmessage_str = ''
                last_message_sender = ''
                last_message_receiver = ''
                last_message_time = ''
            if(all_c.convers_type == o_category and o_category=="active"):
                unread_count = Message.objects.filter(conversation_id= all_c,is_read= False).count()
                if(userDetails.username == all_c.initiator.username):
                    data.append({"user_Name":all_c.receiver.username,'user_receName':all_c.initiator.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.receiver.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver,"unread_count":unread_count})
                else:
                    data.append({"user_Name":all_c.initiator.username,'user_receName':all_c.receiver.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.initiator.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver,"unread_count":unread_count})
            elif(all_c.convers_type == o_category and o_category=="block"):
                if(userDetails.username == all_c.initiator.username):
                    data.append({"user_Name":all_c.receiver.username,'user_receName':all_c.initiator.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.receiver.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver})
                else:
                    data.append({"user_Name":all_c.initiator.username,'user_receName':all_c.receiver.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.initiator.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver})
            elif(all_c.convers_type == "active" and o_category == "unread"):
                unread_count = Message.objects.filter(conversation_id= all_c,is_read= False).count()
                if(unread_count >0):
                    if(userDetails.username == all_c.initiator.username):
                        data.append({"user_Name":all_c.receiver.username,'user_receName':all_c.initiator.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.receiver.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver,"unread_count":unread_count})
                    else:
                        data.append({"user_Name":all_c.initiator.username,'user_receName':all_c.receiver.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.initiator.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver,"unread_count":unread_count})
            elif(all_c.convers_type == "active" and o_category == "offers"):
                unread_count = Message.objects.filter(conversation_id= all_c,is_read= False).count()
                if(userDetails.username == all_c.initiator.username):
                    receiver_user = User.objects.get(username = all_c.receiver.username)
                    custom_orders = Request_Offers.objects.filter(offer_type= "custom",user_id= userDetails, custom_user= receiver_user).count()
                    if(custom_orders == 0):
                        custom_orders = Request_Offers.objects.filter(offer_type= "custom",user_id= receiver_user, custom_user= userDetails).count()
                    if(custom_orders >0):
                        data.append({"user_Name":all_c.receiver.username,'user_receName':all_c.initiator.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.receiver.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver,"unread_count":unread_count})
                else:
                    initiator_user = User.objects.get(username = all_c.initiator.username)
                    custom_orders = Request_Offers.objects.filter(offer_type= "custom",user_id= userDetails, custom_user= initiator_user).count()
                    if(custom_orders == 0):
                        custom_orders = Request_Offers.objects.filter(offer_type= "custom",user_id= initiator_user, custom_user= userDetails).count()
                    if(custom_orders >0):
                        data.append({"user_Name":all_c.initiator.username,'user_receName':all_c.receiver.username,'user_receImg':all_c.initiator.avatar,"user_imag":all_c.initiator.avatar,"last_message_str":lastmessage_str,"last_message_sender":last_message_sender,"last_message_time":last_message_time,"last_message_receiver":last_message_receiver,"unread_count":unread_count})
        return JsonResponse(data,safe=False)


def get_notifications_view(request):
    if request.method == 'GET':
        o_username = request.GET['username']
        data = []
        try:
            userDetails = User.objects.get(username = o_username)
            all_conversations = Conversation.objects.filter(Q(initiator=userDetails) | Q(receiver= userDetails))
            conversation_lists = []
            for all_c in all_conversations:
                if(all_c.convers_type == "active"):
                    unread_count = Message.objects.filter(conversation_id= all_c,is_read= False).count()
                    if(userDetails.username == all_c.initiator.username):
                        pass
                        #data.append({"user_Name":all_c.receiver.username,"unread_count":unread_count})
                    else:
                        data.append({"user_Name":all_c.initiator.username,"unread_count":unread_count})
        except:
            data = []
        return JsonResponse(data,safe=False)

def get_message_notify_view(request):
    if request.method == 'GET':
        data = []
        o_username = request.GET['username']
        response_data = []
        if(len(o_username.strip()) != 0):
            try:
                userDetails = User.objects.get(username = o_username)
                all_nots_list = CustomNotifications.objects.filter(recipient=userDetails,is_read=False).order_by('-pk')
                last_message_time = ''
                unread_count = 0
                username_list = []
                order_username_list = []
                ordre_no = ''
                for noty in all_nots_list:
                    if(len(data) < 10):
                        if(noty.verb.strip() == "chat"): 
                            if noty.sender.username not in username_list:
                                last_message = CustomNotifications.objects.filter(recipient=userDetails,sender = noty.sender.pk,verb= "chat",is_read=False).last()
                                message_date = timesince.timesince(last_message.timestamp) 
                                if(last_message.is_read == False):
                                    unread_count = unread_count + 1
                                last_message_time = last_message.timestamp.strftime('%Y-%m-%d %H:%M')
                                username_list.append(last_message.sender.username)
                                data.append({"mssg_id":last_message.pk,"sender_username":last_message.sender.username,"sender_img":last_message.sender.avatar,"receiver_username":last_message.recipient.username,"receiver_img":last_message.recipient.avatar,"verb":last_message.verb,"text":last_message.description,"message_date":message_date,"isread":last_message.is_read,"order_no":ordre_no})
                        elif(noty.verb.strip() == "order_chat"): 
                            ordre_no = str(noty.order_no.order_no)
                            if noty.sender.username not in order_username_list:
                                last_message = CustomNotifications.objects.filter(recipient=userDetails,sender = noty.sender.pk ,verb= "order_chat",is_read=False).last()
                                message_date = timesince.timesince(last_message.timestamp) 
                                if(last_message.is_read == False):
                                    unread_count = unread_count + 1
                                last_message_time = last_message.timestamp.strftime('%Y-%m-%d %H:%M')
                                order_username_list.append(last_message.sender.username)
                                data.append({"mssg_id":last_message.pk,"sender_username":last_message.sender.username,"sender_img":last_message.sender.avatar,"receiver_username":last_message.recipient.username,"receiver_img":last_message.recipient.avatar,"verb":last_message.verb,"text":last_message.description,"message_date":message_date,"isread":last_message.is_read,"order_no":ordre_no})
            except:
                data = []
                unread_count = 0
                last_message_time = ''
            if(len(data) != 0):
                data.sort(key=operator.itemgetter('mssg_id'), reverse=True)
            response_data= {"data":data,"unread_count":unread_count,"last_time":last_message_time}
        return JsonResponse(response_data,safe=False)

def get_all_notify_view(request):
    if request.method == 'GET':
        data = []
        last_message_time = ''
        o_username = request.GET['username']
        response_data = []
        if(len(o_username.strip()) != 0):
            try:
                userDetails = User.objects.get(username = o_username)
                unread_count = 0
                order_nots_list = CustomNotifications.objects.filter(recipient=userDetails,is_read= False).exclude(Q(verb="order_chat") | Q(verb= "chat")).order_by('-pk')
                for noty in order_nots_list:
                    if(noty.is_read == False):
                        unread_count = unread_count + 1
                    last_message_time = noty.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    if(noty.verb == "order" or noty.verb == "reviews"):
                        order_details = User_orders.objects.get(order_no = noty.order_no.order_no)
                        gig_details = UserGigs.objects.get(gig_title= order_details.package_gig_name.gig_title)
                        imp_gig_image_url = ''
                        imp_gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                        if(imp_gig_image != None):
                            imp_gig_image_url = imp_gig_image.gig_image 
                        message_date = timesince.timesince(noty.timestamp)  
                        data.append({"mssg_id":noty.pk,"sender_username":noty.sender.username,"sender_img":noty.sender.avatar,"receiver_username":noty.recipient.username,"receiver_img":noty.recipient.avatar,"verb":noty.verb,"text":noty.description,"message_date":message_date,"isread":noty.is_read,"gig_img":imp_gig_image_url,"category":gig_details.gig_category.category_Name,"order_no":order_details.order_no})
                    else:
                        message_date = timesince.timesince(noty.timestamp)  
                        data.append({"mssg_id":noty.pk,"sender_username":noty.sender.username,"sender_img":noty.sender.avatar,"receiver_username":noty.recipient.username,"receiver_img":noty.recipient.avatar,"verb":noty.verb,"text":noty.description,"message_date":message_date,"isread":noty.is_read})
            except:
                data = []
                unread_count = 0
                last_message_time = ''
            if(len(data) != 0):
                data.sort(key=operator.itemgetter('mssg_id'), reverse=True)
            response_data= {"data":data,"unread_count":unread_count,"last_time":last_message_time}
        return JsonResponse(response_data,safe=False)

def post_not_mark_as_read_view(request):
    if request.method == 'GET':
        not_id = request.GET['not_id']
        not_sender = request.GET['not_sender']
        getnotif = CustomNotifications.objects.get(pk = not_id)
        getnotif.is_read = True
        getnotif.save()
        return HttpResponse('sucess')
    
def post_mark_as_unread_view(request):
    if request.method == 'GET':
        not_id = request.GET['not_id']
        not_sender = request.GET['not_sender']
        getnotif = CustomNotifications.objects.get(pk = not_id)
        getnotif.is_read = False
        getnotif.save()
        return HttpResponse('sucess')
    
def post_mssg_mark_as_read_view(request):
    if request.method == 'GET':
        not_id = request.GET['not_id']
        not_sender = request.GET['not_sender']
        not_type = request.GET['not_type']
        username = request.GET['username']
        sender_user = User.objects.get(username = not_sender)
        sender_receiver = User.objects.get(username = username)
        messa_resp = Message_Response_Time(receiver=sender_receiver, timestamp= datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        messa_resp.save()
        not_list = CustomNotifications.objects.filter(sender=sender_user,recipient=sender_receiver,verb=not_type).update(is_read=True)
        return HttpResponse('sucess')
    
def get_index_data_view(request):
    if request.method == 'GET':
        active_gigs_details = UserGigs.objects.filter(gig_status='active').exclude(user_id__profile_status ="blocked")
        active_gigs_data= []
        category_list = []
        categories = Categories.objects.all()
        for c in categories:
            sub_cat = SubSubCategories.objects.filter(category_Name=c).first()
            if(sub_cat != None):
                category_list.append({"cat_name":sub_cat.category_Name.category_Name,"subcat_name":sub_cat.sub_category_Name.sub_category_Name,"subsubcat_name":sub_cat.sub_sub_category_Name})
        for u_gig in active_gigs_details:
            gig_image_url = ''
            gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            active_gigs_data.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_username":u_gig.user_id.username,"gig_user_img":u_gig.user_id.avatar})
        active_works = User_orders.objects.filter(order_status="active").count()  
        last_week = datetime.today() - timedelta(days=7)
        menu_list = []  
        categories = Categories.objects.all()
        for i,c in enumerate(categories):
            menu_list.append({"name":c.category_Name,'image':str(c.image)})
        l_username = ''
        l_user_img = ''
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            l_username = userDetails.username
            l_user_img = userDetails.avatar
        buyers_request_week = Buyer_Post_Request.objects.filter(service_date__gte=last_week ,service_type='all').count()
        buyers_this_week = Buyer_Post_Request.objects.filter(service_date__gte=last_week ,service_type='all').distinct('user_id').count()
        responseData = {"gig_details":active_gigs_data,"active_orders":active_works,"new_buyers":buyers_this_week,"buyer_requests":buyers_request_week,"cat_list":category_list,'main_menu' : menu_list,"logged_user":l_username,"logged_user_img":l_user_img}
        return JsonResponse(responseData,safe=False)
    
    
def get_affiliate_data_view(request):
    if request.method == 'GET':
        affiliate_code = 0
        reff_earnings = 0.00
        referral_count = 0
        l_username = ''
        l_user_img = ''
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            affiliate_code = int(userDetails.affiliate_code)
            reff_earnings = round(float(userDetails.referrals_earnings),2)
            referral_count = Referral_Users.objects.filter(user_id=userDetails).exclude(refferal_user__isnull=False).count()
            l_username = userDetails.username
            l_user_img = userDetails.avatar
        responseData =  {"affiliate_code":affiliate_code,"referral_earnings":reff_earnings,"referral_count":referral_count,"logged_user":l_username,"logged_user_img":l_user_img}
        return JsonResponse(responseData,safe=False)

def get_earn_data_view(request):
    if request.method == 'GET':
        learning_topics = []
        learning_Details = []
        l_username = ''
        l_user_img = ''
        responseData = {}
        data = ''
        try:
            if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
                userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                l_username = userDetails.username
                l_user_img = userDetails.avatar
            learning_topics_all = LearnTopics.objects.all()
            for l in learning_topics_all:
                learning_topics.append({"name":l.topic_names})
            learning_Details = []
            learning_topics_Details = LearningTopicDetails.objects.all()
            num_counts = 0
            for l_details in learning_topics_Details:
                num_counts = LearningTopicCounts.objects.filter(topic_name=l_details).count()
                url_link = ''
                try:
                    if(l_details.upload_pdf.url != None):
                        url_link =   request.build_absolute_uri("/") + str(l_details.upload_pdf.url).replace("/home/kworkuser/myprojectdir/","")
                        if(len(l_details.upload_pdf.url) == 0):
                            url_link = str(l_details.video_url)
                    else:
                        url_link = str(l_details.video_url)
                except:
                    url_link = str(l_details.video_url)
                learning_Details.append({"id":l_details.id,"topic_Name":l_details.topic_Name,"timeof_read_in_minute":l_details.timeof_read_in_minute,"topic_description":l_details.topic_description,"image":str(l_details.image),"image_Text":l_details.image_Text,"video_url":url_link,"num_counts":num_counts})
            responseData =  {"topics":learning_topics,"topics_Details":learning_Details,"logged_user":l_username,"logged_user_img":l_user_img}
        except Exception as e:
            data = (str(type(e)) + str(e))
            responseData = {"data":data}
        return JsonResponse(responseData,safe=False)
    
def get_freelancer_data_view(request):
    if request.method == 'GET':
        userdata = []
        l_username = ''
        l_user_img = ''
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            l_username = userDetails.username
            l_user_img = userDetails.avatar
        subcategory= SubCategories.objects.all()
        for sub_cat in subcategory:
            u_profile = UserProfileDetails.objects.filter(sub_category=sub_cat).first()
            if(u_profile != None):
                if(len(userdata) <= 8):
                    userdata.append({"username":u_profile.user_id.username, "profession":u_profile.sub_category.sub_category_Name,"joined_dt":u_profile.user_id.created_at,"profile_img":u_profile.user_id.avatar})
        responseData =  {"user_details":userdata,"logged_user":l_username,"logged_user_img":l_user_img}
        return JsonResponse(responseData,safe=False)
    
def get_all_page_data_view(request):
    if request.method == 'GET':
        userdata = []
        l_username = ''
        l_user_img = ''
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            l_username = userDetails.username
            l_user_img = userDetails.avatar
        responseData =  {"logged_user":l_username,"logged_user_img":l_user_img}
        return JsonResponse(responseData,safe=False)
    
    
def post_user_notification_view(request):
    if request.method == 'GET':
        userid = request.GET['userid']
        umessage = request.GET['umessage']
        uorder = request.GET['uorder']
        uorder_updates = request.GET['uorder_updates']
        userDetails = User.objects.get(pk=userid)
        userDetails.mail_message = umessage
        userDetails.mail_order = uorder
        userDetails.mail_updates = uorder_updates
        userDetails.save()
        return HttpResponse('sucess')

def get_chat_messages_view(request):
    if request.method == 'GET':
        conver_id = request.GET['conver_id']
        count_val = request.GET['current_count']
        id_list = request.GET['id_list']
        cover_detls =  Conversation.objects.get(pk = conver_id)
        idlists = id_list.split(",")
        all_messages = Message.objects.filter(conversation_id= cover_detls,id__in=idlists).order_by('-pk')
        message_data = []
        attachment_str = ''
        for all_m in all_messages:
            attachment_str = ''
            if(all_m.is_read == False):
                all_m.is_read = True
                all_m.save()
            if(all_m.message_type == "chat"):
                attachment_str = ''
                if(all_m.attachment != None):
                    if(len(all_m.attachment.strip()) != 0):
                        attachment_str = all_m.attachment.strip()
                    else:
                        attachment_str = "None"
                else:
                    attachment_str = "None"
                message_data.append({"mssg_type":"chat","mssg_id":all_m.pk,"sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"attachment":attachment_str,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp})
            else:
                if(all_m.message_type == "offer"):
                    offer_details = Request_Offers.objects.get(pk= all_m.request_offers_id.pk)
                    orders_details = User_orders.objects.filter(offer_id=offer_details).first()
                    offer_status = ""
                    order_no= ''
                    if(offer_details.offer_status_by_buyer == "active"):
                        offer_status = "active"
                    elif(offer_details.offer_status_by_buyer == "deleted"):
                        offer_status = "deleted"
                    if((orders_details) != None): 
                        offer_status = "ordered"
                        order_no = orders_details.order_no
                    gig_details = UserGigs.objects.get(gig_title= offer_details.gig_name.gig_title)
                    offer_data = []
                    message_data.append({ "mssg_type":"offer","mssg_id":all_m.pk,"sender_username":all_m.sender.username,"attachment":"None","sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp,"offer_id":offer_details.pk,"buyer_request_id":0,"gig_title":gig_details.gig_title,"offer_amount":offer_details.offer_budget,"offer_time":offer_details.offer_time,"offer_revision":offer_details.no_revisions,"offer_desc":offer_details.offer_desc,"extra_parameters":offer_details.extra_parameters,"offer_sender":offer_details.custom_user.username,"offer_status":offer_status,"order_no":order_no})
                elif(all_m.message_type == "quote"):
                    buyer_request = Buyer_Post_Request.objects.get(pk= all_m.buyer_request_id.pk)
                    service_time_str = ''
                    no_of_days = ''
                    due_date_str = ''
                    today_date = datetime.today()
                    if(buyer_request.service_time== "24hours"):
                        service_time_str = "24 dours"
                        no_of_days = 1
                        due_date_str = today_date + timedelta(days=int(no_of_days))
                        due_date_str = due_date_str.strftime('%b %d, %Y')
                    elif(buyer_request.service_time== "3days"):
                        service_time_str = "3 days"
                        no_of_days = 3
                        due_date_str = today_date + timedelta(days=int(no_of_days))
                        due_date_str = due_date_str.strftime('%b %d, %Y')
                    elif(buyer_request.service_time== "7days"):
                        service_time_str = "7 days"
                        no_of_days = 7
                        due_date_str = today_date + timedelta(days=int(no_of_days))
                        due_date_str = due_date_str.strftime('%b %d, %Y')
                    elif(buyer_request.service_time== "other"):
                        service_time_str = "Other"
                        due_date_str = ''
                    offer_data = []
                    offer_created_status = ''
                    try:
                        req_offers = Request_Offers.objects.get(buyer_request = buyer_request)
                        offer_created_status = "created"
                    except:
                        offer_created_status = "active"
                    message_data.append({"mssg_type":"quote","mssg_id":all_m.pk,"attachment":"None","sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp,"request_id":buyer_request.pk,"req_desc":buyer_request.service_desc,"req_time":service_time_str,"req_budget":buyer_request.service_budget,"req_due_date":due_date_str,"req_status":buyer_request.service_status,"offer_created_sta":offer_created_status})
        message_data.sort(key=operator.itemgetter('mssg_id'))
        response_data = {"data":message_data,"current_count":count_val}
        return JsonResponse(response_data,safe=False)

def post_view_gig_offer_view(request):
    if request.method == 'GET':
        initiator = request.GET['initiator']
        receiver = request.GET['receiver'] 
        package = request.GET['package'] 
        gig_id = request.GET['gig_id']
        initiator = User.objects.get(username = initiator)
        receiver = User.objects.get(pk = receiver)
        gig_details = UserGigs.objects.get(pk = gig_id)
        requirements = Usergig_requirement.objects.filter(package_gig_name=gig_details ).count()
        ask_req = False
        if(requirements >= 1):
            ask_req = True
        userpack= UserGigPackages.objects.filter(package_gig_name=gig_details, package_type= package).first()
        o_text_no_revs = userpack.package_revisions
        o_text_del_time = userpack.package_delivery
        o_text_price = userpack.package_price
        order_descp_str = "You have received an order from "+ str(initiator.username)
        offer_details = Request_Offers(gig_name=gig_details,user_id=receiver,buyer_request=None,custom_user= initiator, offer_desc=order_descp_str, offer_budget=o_text_price, offer_time=o_text_del_time,no_revisions=o_text_no_revs, ask_requirements= ask_req, extra_parameters=str(""),offer_type="custom" )
        offer_details.save()
        return HttpResponse(offer_details.pk)
    
    
def handler404(request, exception):
    context = {}
    response = render(request, "404_error.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "500_page.html", context=context)
    response.status_code = 500
    return response
