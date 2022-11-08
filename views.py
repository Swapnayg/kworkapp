from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import sub
import smtplib
import shortuuid
from operator import itemgetter
from python_flutterwave import payment
from datetime import datetime, timedelta
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
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from django.core import serializers
import json
from kworkapp.models import Categories,UserGigPackages,UploadFile,Api_keys,SpamDetection,User_warning,User_Refund,User_Earnings,ChatWords,Gig_favourites,User_orders_Extra_Gigs,Conversation,Order_Message,Order_Conversation,Order_Delivery,Message_Response_Time,User_Order_Activity,User_Order_Resolution,User_Transactions,Payment_Parameters,Request_Offers,Referral_Users,UserGigPackage_Extra,Buyer_Post_Request,Seller_Reviews,Buyer_Reviews,UserGigsImpressions,User_orders,UserSearchTerms,UserGig_Extra_Delivery,UserExtra_gigs,Usergig_faq,Usergig_image,Usergig_requirement,Parameter,Category_package_Extra_Service,Category_package_Details, CharacterLimit,UserAvailable,UserGigs,UserGigsTags, SellerLevels,Contactus, Languages, LearnTopics, LearningTopicCounts, LearningTopicDetails, SubCategories, SubSubCategories, TopicDetails, User,PageEditor, UserLanguages,Addon_Parameters,Buyer_Requirements, UserProfileDetails, supportMapping, supportTopic,Message
import operator


class indexView(View):
    return_url = None
    def get(self , request,username=''):
        active_gigs_details = UserGigs.objects.filter(gig_status='active')
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
            active_gigs_data.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_user":u_gig.user_id})
        active_works = User_orders.objects.filter(order_status="active").count()  
        last_week = datetime.today() - timedelta(days=7)    
        buyers_request_week = Buyer_Post_Request.objects.filter(service_date__gte=last_week).count()
        buyers_this_week = Buyer_Post_Request.objects.filter(service_date__gte=last_week).distinct('user_id').count()
        return render(request , 'index.html',{"gig_details":active_gigs_data,"active_orders":active_works,"new_buyers":buyers_this_week,"buyer_reqyests":buyers_request_week,"cat_list":category_list,"cat_list_json":json.dumps(category_list)})

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
        return render(request , 'gigs_page.html',{"details":category_details,"sub_details":sub_categoryd,"sub_topics":sub_sub_category,"tagslist":tagslist})

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
    def get(self , request,username='',gig_title=''):
        # try:
            userDetails = User.objects.get(username = username)
            languages = Languages.objects.exclude(lng_slug= u'english').order_by('lng_Name')
            userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
            userlang = []
            english_profi = ''
            userlanguages = UserLanguages.objects.filter(user_id=userDetails)
            for lang in userlanguages:
                userlang.append({"name":lang.language_name.lng_Name,"proficiency":lang.lang_prof}) 
            gig_details = UserGigs.objects.get(user_id=userDetails ,gig_title= gig_title)
            gig_package_details = UserGigPackages.objects.filter(user_id=userDetails ,package_gig_name= gig_details)
            gig_image_details = Usergig_image.objects.filter(user_id=userDetails ,package_gig_name= gig_details)
            seller_reviews = Seller_Reviews.objects.filter(s_review_to=userDetails,package_gig_name= gig_details)
            seller_all_reviews = Seller_Reviews.objects.filter(s_review_to=userDetails)
            comm_count = 0
            recc_count = 0
            serv_count = 0
            seller_count = 0
            seller_all_count = 0
            s_review_date = ''
            seller_rev_data = []
            for sa_review in seller_all_reviews:
                seller_all_count = seller_all_count + int(sa_review.average_val)
            for s_review in seller_reviews:
                comm_count = comm_count + int(s_review.communication)
                recc_count = recc_count + int(s_review.recommendation)
                serv_count = serv_count + int(s_review.service)
                seller_count = seller_count + int(s_review.average_val)
                start_date = datetime.strptime(str(s_review.review_date), "%Y-%m-%d %H:%M:%S")
                s_res_start_date = datetime.strptime(str(s_review.buyer_resp_date), "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                diff = relativedelta.relativedelta(end_date, start_date)
                diff1 = relativedelta.relativedelta(end_date, s_res_start_date)
                if(diff.years == 0 and diff.months == 0):
                    if(diff.days == 0):
                        s_review_date = 'today'
                    else:
                        s_review_date = str(diff.days) + ' days'
                elif(diff.months != 0 and diff.years == 0):
                    if(diff.months == 1):
                        s_review_date = str(diff.months) + ' month'
                    else:
                        s_review_date = str(diff.months) + ' months'
                elif(diff.years != 0):
                    if(diff.years == 1):
                        s_review_date = str(diff.years) + ' year'
                    else:
                        s_review_date = str(diff.years) + ' years'
                if(diff1.years == 0 and diff1.months == 0):
                    if(diff1.days == 0):
                        s_resp_date = 'today'
                    else:
                        s_resp_date = str(diff1.days) + ' days'
                elif(diff1.months != 0 and diff1.years == 0):
                    if(diff1.months == 1):
                        s_resp_date = str(diff1.months) + ' month'
                    else:
                        s_resp_date = str(diff1.months) + ' months'
                elif(diff1.years != 0):
                    if(diff1.years == 1):
                        s_resp_date = str(diff1.years) + ' year'
                    else:
                        s_resp_date = str(diff1.years) + ' years'
                country_flag_icon = '/static/assets/images/flags/'+ s_review.s_review_from.country.code.lower()+ '.svg'
                seller_rev_data.append({"message":s_review.review_message,"review":s_review.average_val,"sender":s_review.s_review_from,"review_date":s_review_date,"seller_resp_date":s_resp_date,"buyer_resp":s_review.buyer_response,"country_flag":country_flag_icon})                 
            try:
                seller_count = round(seller_count/len(seller_reviews),1)
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
            seller_levl= ''
            if(userDetails.seller_level=="level1"):
                seller_levl = "New or higher"
            elif(userDetails.seller_level=="level2"):
                seller_levl = "Advanced or higher"
            elif(userDetails.seller_level=="level3"):
                seller_levl = "Professional"
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
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                impressions = UserGigsImpressions(ip_address=str(whatismyip.whatismyip()),impress_type ="click" ,gig_name=gig_details, user_id=userDetails)
                impressions.save()
            else:   
                impressions = UserGigsImpressions(ip_address=str(whatismyip.whatismyip()),impress_type ="click" ,gig_name=gig_details)
                impressions.save()
            extra_gigs = UserExtra_gigs.objects.filter(package_gig_name=gig_details)
            return render(request , 'Dashboard/view_gig.html',{'userDetails':userDetails,"profile_Details":userProfileDetails,"userlanguages":userlang,"gig_details":gig_details,"gig_package_Details":gig_package_details,"gig_image_Details":gig_image_details,"gig_reviews":seller_rev_data,"seller_count":seller_count,"comm_count":comm_count,"recc_count":recc_count,"serv_count":serv_count,"seller_level":seller_levl,"seller_all_review":seller_all_reviews,"seller_all_count":seller_all_count,"Other_gigs":active_gigs_data,"fav_count":favourite_Count,"current_user_fav":curr_fav,"extra_gigs":extra_gigs})                 
        # except:
        #     return render(request , 'register.html')
            
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
        learning_topics = LearnTopics.objects.all()
        learning_Details = []
        learning_topics_Details = LearningTopicDetails.objects.all()
        num_counts = 0
        for l_details in learning_topics_Details:
            num_counts = LearningTopicCounts.objects.filter(topic_name=l_details).count()
            learning_Details.append({"id":l_details.id,"topic_Name":l_details.topic_Name,"timeof_read_in_minute":l_details.timeof_read_in_minute,"topic_description":l_details.topic_description,"image":l_details.image,"image_Text":l_details.image_Text,"video_url":l_details.video_url,"num_counts":num_counts})
        return render(request , 'earn_letworkbdone.html',{"topics":learning_topics,"topics_Details":learning_Details})

class categoriesView(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'categories.html')

class affiliate_programView(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try: 
                userDetails = User.objects.get(username=str(request.user.username).strip())
                base_url = request.build_absolute_uri('/ref')
                referral_count = Referral_Users.objects.filter(user_id=userDetails).exclude(refferal_user__isnull=False).count()
                return render(request , 'affiliate_program.html',{'userDetails':userDetails,"url": base_url,"referral_count":referral_count})                 
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

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
        return render(request , 'reviews.html',{"categories":categories,"no_reviews":len(buyer_reviews), "aver_count":buyer_count})

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
        return render(request , 'faq.html')


class contact_support_View(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'contact_support.html')

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
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try: 
                userDetails = User.objects.get(username=username)
                userProfileDetails = UserProfileDetails.objects.get(user_id=userDetails)
                userlanguages = UserLanguages.objects.filter(user_id=userDetails)
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
                s_review_date = ''
                b_review_date = ''
                seller_rev_data = []
                buyer_rev_data = []
                for s_review in seller_reviews:
                    comm_count = comm_count + int(s_review.communication)
                    recc_count = recc_count + int(s_review.recommendation)
                    serv_count = serv_count + int(s_review.service)
                    seller_count = seller_count + int(s_review.average_val)
                    start_date = datetime.strptime(str(s_review.review_date), "%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(end_date, start_date)
                    if(diff.years == 0 and diff.months == 0):
                        if(diff.days == 0):
                            s_review_date = 'today'
                        else:
                            s_review_date = str(diff.days) + ' days'
                    elif(diff.months != 0 and diff.years == 0):
                        if(diff.months == 1):
                            s_review_date = str(diff.months) + ' month'
                        else:
                            s_review_date = str(diff.months) + ' months'
                    elif(diff.years != 0):
                        if(diff.years == 1):
                            s_review_date = str(diff.years) + ' year'
                        else:
                            s_review_date = str(diff.years) + ' years'
                    country_flag_icon = '/static/assets/images/flags/'+ s_review.s_review_from.country.code.lower()+ '.svg'
                    seller_rev_data.append({"message":s_review.review_message,"review":s_review.average_val,"sender":s_review.s_review_from,"review_date":s_review_date,"country_flag":country_flag_icon})
                for b_review in buyer_reviews:
                    buyer_count = buyer_count + int(b_review.rating_val)
                    start_date = datetime.strptime(str(b_review.review_date), "%Y-%m-%d %H:%M:%S")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(end_date, start_date)
                    if(diff.years == 0 and diff.months == 0):
                        if(diff.days == 0):
                            b_review_date = 'today'
                        else:
                            b_review_date = str(diff.days) + ' days'
                    elif(diff.months != 0 and diff.years == 0):
                        if(diff.months == 1):
                            b_review_date = str(diff.months) + ' month'
                        else:
                            b_review_date = str(diff.months) + ' months'
                    elif(diff.years != 0):
                        if(diff.years == 1):
                            b_review_date = str(diff.years) + ' year'
                        else:
                            b_review_date = str(diff.years) + ' years'
                    b_country_flag_icon = '/static/assets/images/flags/'+ b_review.b_review_from.country.code.lower()+ '.svg'
                    buyer_rev_data.append({"message":b_review.review_message,"review":b_review.rating_val,"sender":b_review.b_review_from,"review_date":b_review_date,"country_flag":b_country_flag_icon})
                try:
                    seller_count = round(seller_count/len(seller_reviews),1)
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
                        active_gig_details.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"start_price":start_price})
                    elif(u_gig.gig_status == "draft"):
                        draft_gig_details.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"start_price":start_price})
                return render(request , 'Dashboard/profile.html',{'userDetails':userDetails,"profile_Details":userProfileDetails,"userlanguages":userlang,"active_gigs":active_gig_details,"draft_gigs":draft_gig_details,"seller_reviews":seller_rev_data,"seller_count":seller_count,"comm_count":comm_count,"recc_count":recc_count,"serv_count":serv_count,"buyer_count":buyer_count,"buyer_reviews":buyer_rev_data,"character_avail":int(available_char),"character_post_request":int(post_request_char),"user_avail":user_availability,"categories":categories})                 
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class buyer_dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"buyer"
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try: 
                userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                active_gigs_details = UserGigs.objects.filter(gig_status='active')
                active_gigs_data= []
                category_list = []
                categories = Categories.objects.all()
                for c in categories:
                    sub_cat = SubSubCategories.objects.filter(category_Name=c).first()
                    if(sub_cat != None):
                        category_list.append({"cat_name":sub_cat.category_Name.category_Name,"subcat_name":sub_cat.sub_category_Name.sub_category_Name,"subsubcat_name":sub_cat.sub_sub_category_Name})
                for u_gig in active_gigs_details:
                    gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    active_gigs_data.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_user":u_gig.user_id})
                impression_gigs = UserGigsImpressions.objects.filter(user_id= userDetails).values("gig_name").distinct()
                impression_data = []
                for imp in impression_gigs:
                    if(imp["gig_name"] != None):
                        gig_data = UserGigs.objects.get(pk=imp["gig_name"])
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
                            seller_count = seller_count + int(s_review.average_val)
                        try:
                            seller_count = round(seller_count/len(seller_reviews),1)
                        except:
                            seller_count = 0   
                        impression_data.append({"gig_title":gig_data.gig_title,"gig_img_url":imp_gig_image_url,"start_price":start_price,"seller_count":seller_count,"review_count":len(seller_reviews),"gig_username":gig_data.user_id.username, "gig_gig_img":gig_data.user_id.avatar})
                search_term = UserSearchTerms.objects.filter(user_id=userDetails).values("search_words").distinct()
                search_data = []
                for search in search_term:
                    subcate_inst = SubSubCategories.objects.get(sub_sub_category_Name= search["search_words"])
                    try:
                        sear_gig_data = UserGigs.objects.get(gig_sub_category=subcate_inst)
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
                            sea_seller_count = sea_seller_count + int(ss_review.average_val)
                        try:
                            sea_seller_count = round(sea_seller_count/len(sear_seller_reviews),1)
                        except:
                            sea_seller_count = 0   
                        search_data.append({"gig_title":sear_gig_data.gig_title,"gig_img_url":search_gig_image_url,"start_price":search_start_price,"seller_count":sea_seller_count,"review_count":len(sear_seller_reviews),"gig_username":sear_gig_data.user_id.username, "gig_gig_img":sear_gig_data.user_id.avatar})
                    except:
                        pass 
                return render(request , 'Dashboard/buyer_dashboard.html',{"P_gig_details":active_gigs_data,"cat_list":category_list,"cat_list_json":json.dumps(category_list),"impression_gigs":impression_data,"search_data":search_data})               
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')       

class search_gig_view(View):
    return_url = None
    def get(self , request,keyword=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(whatismyip.whatismyip()),search_types=keyword_type)
            search_term.save()
        else:   
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(whatismyip.whatismyip()),search_types=keyword_type)
            search_term.save()
        gig_category_details = Categories.objects.filter(category_Name__contains=keyword)
        gig_sub_category_details = SubSubCategories.objects.filter(sub_sub_category_Name__contains=keyword)
        if(len(gig_category_details)!=0):
            gigs_details = UserGigs.objects.filter(gig_category =gig_category_details[0].pk)
        elif(len(gig_sub_category_details)!=0):
            gigs_details = UserGigs.objects.filter(gig_sub_category =gig_sub_category_details[0].pk)   
        else:
            gigs_details = UserGigs.objects.filter(gig_title__contains=keyword)
        active_gigs_data = []
        for u_gig in gigs_details:
            gig_image = Usergig_image.objects.filter(package_gig_name=u_gig).first() 
            if(gig_image != None):
                gig_image_url = gig_image.gig_image
            active_gigs_data.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_user":u_gig.user_id})
        return render(request , 'search_gig.html',{"keyword":keyword,"active_gigs":active_gigs_data})

class search_profile_view(View):
    return_url = None
    def get(self , request,keyword=''):
        user_details_li= []
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(whatismyip.whatismyip()),search_types="user")
            search_term.save()
        else:   
            search_term= UserSearchTerms(search_words=keyword,ip_address = str(whatismyip.whatismyip()),search_types="user")
            search_term.save()
        user_details = User.objects.filter(username__contains=keyword)
        for u in user_details:
            country_flag_icon = '/static/assets/images/flags/'+ u.country.code.lower()+ '.svg'
            seller_reviews = Seller_Reviews.objects.filter(s_review_to=u).count()
            user_details_li.append({"username":u.username,"country":u.country.name,"profile_img":u.avatar,"c_flag":country_flag_icon, "u_ratings":seller_reviews})
        return render(request , 'search_user.html',{"keyword":keyword,"user_details":user_details_li})

def logout_social(request):
    logout(request)
    return redirect('index')
    

class seller_main_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"seller"
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
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
                            due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S").date()
                        except:
                            due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        diff = relativedelta.relativedelta(due_date, end_date)
                        num = float(diff.days)
                        if num > 0:
                            order_status = "In progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        elif num == 0:
                            order_status = "In progress"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                        else:
                            order_status = "late"
                            due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late" 
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
                        delivered_per = round(float(len(s_delivered_orders_detls)/total_orders)*100,2)
                    except:
                        delivered_per = 0
                    try:
                        completed_per = round(float(len(s_completed_orders_detls)/total_orders)*100,2)
                    except:
                        completed_per = 0
                    return render(request , 'Dashboard/seller_dashboard.html',{"active_orders":s_active_orders,"delivered_orders":s_delivered_orders,"completed_orders":s_completed_orders,"cancelled_orders":s_cancelled_orders,"Active_earning":active_earnings,"resp_time":userDetails.avg_respons,"this_earning":userDetails.current_earning,"active_per":active_per,"delivered_per":delivered_per,"completed_per":completed_per})
                else:
                    return redirect('account_settings') 
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class offers_view(View):
    return_url = None
    def get(self , request,username='',req_id=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
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
                        seller_count = seller_count + int(s_review.average_val)
                    try:
                        seller_count = round(seller_count/len(seller_reviews),1)
                    except:
                        seller_count = 0
                    seller_levl = ''
                    user_details_off = User.objects.get(username = b_o.user_id.username)
                    if(user_details_off.seller_level=="level1"):
                        seller_levl = "New or higher"
                    elif(user_details_off.seller_level=="level2"):
                        seller_levl = "Advanced or higher"
                    elif(user_details_off.seller_level=="level3"):
                        seller_levl = "Professional"
                    buyer_offers_li.append({"buyer_username":b_o.user_id.username,"buyer_image":b_o.user_id.avatar,"gig_id":b_o.gig_name.id,"gig_title":b_o.gig_name.gig_title ,"gig_image":gig_image_url,"seller_reviews":seller_count,"offer_desc":b_o.offer_desc,"offer_price":b_o.offer_budget,"offer_time":b_o.offer_time,"seller_level":seller_levl,"offer_date":str(b_o.offer_date),"offer_id":b_o.id,"offer_data":json.loads(b_o.extra_parameters)})
                return render(request , 'Dashboard/offers.html',{"buyer_request":buyer_request,"offers":buyer_offers_li})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
    
class payments_view(View):
    return_url = None
    def get(self , request,req_id='',offer_id=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                gigdetails_list = []
                buyer_req_details = Buyer_Post_Request.objects.get(buyer_request_id= req_id)
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
                if(int(offer_details.offer_budget) <=40):
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
                gigdetails_list.append({"gig_title":gig_details.gig_title,"gig_image":imp_gig_image_url,"offer_price": round(float(offer_details.offer_budget),2),"offer_revisions":offer_details.no_revisions,"service_fees":service_fees_price,"total_amount":round(float((int(offer_details.offer_budget)+ int(service_fees_price))),2),"tax_ref_name":gig_details.user_id.username + "_ref_user","pay_to_user":gig_details.user_id.username,"pay_to_user_email":gig_details.user_id.email,"offer_id":offer_details.id,"serv_fees_type":serv_fees_type,"serv_fees_val":serv_fees_val})
                base_url = request.build_absolute_uri("/")
                extra_gigs = UserExtra_gigs.objects.filter(package_gig_name=gig_details)
                api_details = Api_keys.objects.filter(Q(api_name="paypal") | Q(api_name= "flutterwave"))
                paypal_client_id = ''
                flutter_client_id = ''
                for api in api_details:
                    if(api.api_name == "paypal"):
                        paypal_client_id = api.private_key
                    elif(api.api_name == "flutterwave"):
                        flutter_client_id = api.private_key
                return render(request , 'Dashboard/payments.html',{"buyer_req_id":req_id,"gig_details":gigdetails_list,"base_url":base_url,"extra_gigs":extra_gigs,"flutterwave_client_id":flutter_client_id,"paypal_client_id":paypal_client_id})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
    
class requirements_p_view(View):
    return_url = None
    def get(self , request,offer_id="",pay_id="",pay_email="",trans_id="",pay_status="",base_price=0,total_price=0,service_fee=0,pay_to='',extra_gig=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                pay_user = User.objects.get(username = pay_to)
                offer_details = Request_Offers.objects.get(id= offer_id ,user_id = pay_user )
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
                    already_submitted = Buyer_Requirements.objects.filter(user_id= userDetails,gig_name=gig_details).count()
                else:
                    
                    already_submitted = 2  
                    gig_id_str = 0
                return render(request , 'Dashboard/get_requirements_paypal.html',{"offer_id":offer_id,"gig_requirements":gig_requirements,"req_ans_char":gig_req_ans_char,"gig_id":gig_id_str,"submitted":already_submitted})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class requirements_f_view(View):
    return_url = None
    def get(self , request,offer_id="",base_price=0,total_price=0,service_fee=0,pay_to='',extra_gig=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                pay_user = User.objects.get(username = pay_to)
                offer_details = Request_Offers.objects.get(id= offer_id ,user_id = pay_user )
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
                    already_submitted = Buyer_Requirements.objects.filter(user_id= userDetails,gig_name=gig_details).count()
                else:
                    already_submitted = 2  
                    gig_id_str = 0
                return render(request , 'Dashboard/get_requirements_flutter.html',{"offer_id":offer_id,"base_price":base_price,"total_price":total_price,"service_fee":service_fee,"gig_requirements":gig_requirements,"req_ans_char":gig_req_ans_char,"gig_id":gig_id_str,"submitted":already_submitted})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')



class Manage_request_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                active_request = []
                pending_request = []
                rejected_request = []
                paused_request = []
                active_request_obj = Buyer_Post_Request.objects.filter(service_status="active", user_id=userDetails)
                pending_request_obj = Buyer_Post_Request.objects.filter(service_status="pending", user_id=userDetails)
                paused_request_obj = Buyer_Post_Request.objects.filter(service_status="paused", user_id=userDetails)
                rejected_request_obj = Buyer_Post_Request.objects.filter(service_status="rejected" , user_id=userDetails)
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
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class post_request_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "post_request_desc"))
                available_char = 0
                post_request_char = 0
                for c in charcterlimits:
                    if(c.Char_category_Name == "post_request_desc"):
                        post_request_char = c.Max_No_of_char_allowed
                categories = Categories.objects.all()
                return render(request , 'Dashboard/post_request.html',{"character_post_request":int(post_request_char),"categories":categories})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        

class billing_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                user_trans = User_Transactions.objects.filter(paid_by=userDetails)
                category_list = []
                for tran in user_trans:
                    category_list.append({"cat_id":tran.offer_id.gig_name.gig_sub_category.id,"cat_name":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name})
                return render(request , 'Dashboard/billing.html',{"avail_bal": round(float((int(userDetails.avail_bal))),2),"earning_bal": round(float((int(userDetails.total_earning))),2),"cancel_bal": round(float((int(userDetails.cancelled_earning))),2),"cat_lists":category_list})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class inbox_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/chat.html')
    
class buyer_review_view(View):
    return_url = None
    def get(self , request,order_no=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                previous_page = request.META.get('HTTP_REFERER')
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "buyer_review"))
                buyer_char = 0
                for c in charcterlimits:
                    if(c.Char_category_Name == "buyer_review"):
                        buyer_char = c.Max_No_of_char_allowed
                return render(request , 'Dashboard/buyer_review.html',{"previous_page":previous_page,"order_no":order_no,"buyer_descp_count":buyer_char})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')


class seller_review_view(View):
    return_url = None
    def get(self , request,order_no=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                previous_page = request.META.get('HTTP_REFERER')
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "seller_review"))
                seller_char = 0
                for c in charcterlimits:
                    if(c.Char_category_Name == "seller_review"):
                        seller_char = c.Max_No_of_char_allowed
                return render(request , 'Dashboard/seller_review.html',{"previous_page":previous_page,"order_no":order_no,"seller_descp_count":seller_char})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
    
class warning_review_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                get_warning = User_warning.objects.get(user_id = userDetails , confirmed_status= False)
                warning_count =  User_warning.objects.filter(user_id = userDetails).count()
                previous_page = request.META.get('HTTP_REFERER')
                warning_count_text = ""
                if(warning_count == 3):
                    userDetails.profile_status = "blocked"
                    userDetails.save()
                    return render(request , 'register.html')
                else:
                    if(warning_count == 2):
                        warning_count_text = "Second"
                    elif(warning_count == 1):
                        warning_count_text = "First"
                    return render(request , 'Dashboard/warning.html',{"warning_details":get_warning,"warning_count":warning_count_text,"previous_page":previous_page})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
    
class blocked_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                return render(request , 'Dashboard/blocked.html')
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

                


class favourites_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                fav_lists = Gig_favourites.objects.filter(user_id=userDetails)
                fav_lists_data = []
                for gig in fav_lists:
                    user_gig = UserGigs.objects.get(gig_title= str(gig.gig_name))
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=user_gig).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    fav_lists_data.append({"gig_title":gig.gig_name.gig_title, "gig_image":gig_image_url})
                return render(request , 'Dashboard/favourites.html',{"favourite_lists":fav_lists_data})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class create_gig_view(View):
    return_url = None
    def get(self , request,username='',gigid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:  
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
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
                return render(request , 'Dashboard/create_gig.html',{"category":categorieslist,"Delivery_Time":delivery_time,"No_Revisions":no_revisions,"Extra_Days":extra_days,"Extra_Time":extra_time,"gig_title_char":gig_title_char,"gig_package_title_char":gig_package_title_char,"gig_package_description_char":gig_package_description_char,"gig_extra_description_char":gig_extra_description_char,"gig_extra_title_char":gig_extra_title_char,"gig_description_char":gig_description_char,"gig_faq_question_char":gig_faq_question_char,"gig_faq_answer_char":gig_faq_answer_char,"gig_requirements_ques_char":gig_requirements_ques_char,"gig_requirements_ans_char":gig_requirements_ans_char})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
        
class buyer_manage_orders_view(View):
    return_url = None
    def get(self , request,username='',gigid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:  
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
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class seller_manage_orders_view(View):
    return_url = None
    def get(self , request,username=''):
        request.session['userpage'] =	"seller"
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
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
                        due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S").date()
                    except:
                        due_date = datetime.strptime(str(a_order.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(due_date, end_date)
                    num = float(diff.days)
                    if num > 0:
                        order_status = "In progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        order_status = "In progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    else:
                        order_status = "late"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
                    order_act_lists = []
                    orderactivities = User_Order_Activity.objects.filter(order_no=a_order)
                    for o_act in orderactivities:
                        order_act_lists.append({"order_message":o_act.order_message,"order_amount":o_act.order_amount})
                    s_active_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar,"due_date":a_order.due_date, "buyer_username":a_order.order_by.username,"order_price":a_order.order_amount,"delivery_time":due_in_str,"del_satus":order_status,"order_id":a_order.order_no,"order_activity":order_act_lists})
                for a_order in s_delivered_orders_detls:
                    gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    order_act_lists = []
                    orderactivities = User_Order_Activity.objects.filter(order_no=a_order)
                    for o_act in orderactivities:
                        order_act_lists.append({"order_message":o_act.order_message,"order_amount":o_act.order_amount})
                    s_delivered_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar,"due_date":a_order.due_date, "buyer_username":a_order.order_by.username,"order_price":a_order.order_amount,"del_satus":"Delivered","order_id":a_order.order_no,"order_activity":order_act_lists})
                for a_order in s_completed_orders_detls:
                    gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    order_act_lists = []
                    orderactivities = User_Order_Activity.objects.filter(order_no=a_order)
                    for o_act in orderactivities:
                        order_act_lists.append({"order_message":o_act.order_message,"order_amount":o_act.order_amount})
                    s_completed_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"due_date":a_order.due_date,"order_price":a_order.order_amount,"del_satus":"Completed","order_id":a_order.order_no,"order_activity":order_act_lists})
                for a_order in s_cancelled_orders_detls:
                    gig_details = UserGigs.objects.get(gig_title = a_order.package_gig_name.gig_title)
                    gig_image_url = ''
                    gig_image = Usergig_image.objects.filter(package_gig_name=gig_details).first() 
                    if(gig_image != None):
                        gig_image_url = gig_image.gig_image
                    order_act_lists = []
                    orderactivities = User_Order_Activity.objects.filter(order_no=a_order)
                    for o_act in orderactivities:
                        order_act_lists.append({"order_message":o_act.order_message,"order_amount":o_act.order_amount})
                    s_cancelled_orders.append({"gig_id":gig_details.id,"gig_title":gig_details.gig_title,"gig_image_url":gig_image_url,"buyer_img":a_order.order_by.avatar, "buyer_username":a_order.order_by.username,"due_date":a_order.due_date,"order_price":a_order.order_amount,"del_satus":"Cancelled","order_id":a_order.order_no,"order_activity":order_act_lists})
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
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class buyer_request_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                all_categories = []
                seller_level_offer = 0
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id) 
                seller_lvel = SellerLevels.objects.get(level_name= userDetails.seller_level)
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
                offers_sent = Request_Offers.objects.filter(user_id= userDetails)
                for off in offers_sent:
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
                return render(request , 'Dashboard/buyer_request.html',{"user_details":userDetails,"max_offers":seller_lvel.No_of_offers,"all_categories":all_categories,"delivery_time":delivery_time, "no_revisions":no_revisions,"offer_description":offer_description,"offer_sent_req":offers_sent_list})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html') 

class manage_gigs_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:    
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
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
                    last_month = datetime.today() - timedelta(days=30)
                    ugig_impressions = UserGigsImpressions.objects.filter(user_id=userDetails,gig_name=u_gig,impress_date__gte=last_month).count()
                    user_order_details = User_orders.objects.filter(order_by=userDetails,package_gig_name=u_gig,order_date__gte=last_month).count()
                    cancelled_orders =  User_orders.objects.filter(order_by=userDetails,package_gig_name=u_gig, order_status= 'cancel').count()
                    try:
                        cancel_perc = int((cancelled_orders * 100) / (user_order_details))
                    except:
                        cancel_perc = 0
                    if(u_gig.gig_status == "active"):
                        activegigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "pending"):
                        pendinggigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "modification"):
                        modifgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "draft"):
                        drafgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "denied"):
                        deniedgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                    elif(u_gig.gig_status == "paused"):
                        pausedgigs.append({"gig_id":u_gig.pk,"gig_Name":u_gig.gig_title,"gig_Image":gig_image_url,"gig_impressions":ugig_impressions,"gig_orders":user_order_details,"gig_cancel_rate":cancel_perc})
                return render(request , 'Dashboard/manage_gigs.html',{"active_gigs":activegigs,"pending_gigs":pendinggigs,"require_modif":modifgigs,"draft_gigs":drafgigs,"denied_gigs":deniedgigs,"paused_gigs":pausedgigs})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class earnings_view(View):
    return_url = None
    def get(self , request,username=''):
        return render(request , 'Dashboard/earnings.html')

class order_activities_view(View):
    return_url = None
    def get(self , request,username='',orderid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
                delivery  = ''
                delivery_details_list = []
                userDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
                order_details = User_orders.objects.get(order_no = orderid)
                offer_details =  Request_Offers.objects.get(id = order_details.offer_id.id)
                ordered_by_user = User.objects.get(id= order_details.order_by.id)
                ordered_to_user = User.objects.get(id= order_details.order_to.id)
                extra_offer = User_orders_Extra_Gigs.objects.filter(order_no=order_details)
                current_user = ''
                buyer_user_name = ''
                seller_user_name = ''
                if(userDetails.username == ordered_by_user.username):
                    current_user = "Buyer"
                    buyer_user_name = str(ordered_by_user.username)
                    seller_user_name = str(ordered_to_user.username)
                else:
                    current_user = "Seller"
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
                    diff = relativedelta.relativedelta(due_date, end_date)
                    order_due_date = order_details.due_date
                    formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                    num = float(diff.days)
                    if num > 0:
                        order_status = "progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        order_status = "late"
                        formatted_due_date = "failed"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    else:
                        order_status = "late"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
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
                    conversation = Order_Conversation.objects.get(initiator=ordered_to_user,receiver=ordered_by_user)
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
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name="order_message") | Q(Char_category_Name= "delivery_description") | Q(Char_category_Name= "resolution_cancel_text"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "order_message"):
                        message_char = c.Max_No_of_char_allowed
                    elif(c.Char_category_Name == "delivery_description"):
                        delivery_char = c.Max_No_of_char_allowed
                    elif(c.Char_category_Name == "resolution_cancel_text"):
                        cancel_char = c.Max_No_of_char_allowed
                try:
                    conversation = Order_Conversation.objects.get(initiator=ordered_by_user,receiver=ordered_to_user)
                except:
                    conversation = Order_Conversation.objects.get(initiator=ordered_to_user,receiver=ordered_by_user)
                chat_words = list(ChatWords.objects.order_by().values_list('name').distinct())
                chat_words_5_words = list(ChatWords.objects.order_by().values_list('name').distinct())[:5]
                buyer_review = []
                seller_review = []
                if(Buyer_Reviews.objects.filter(b_review_from=ordered_to_user,b_review_to=ordered_by_user).exists() == True):
                    buyer_review = Buyer_Reviews.objects.get(b_review_from=ordered_to_user,b_review_to=ordered_by_user)
                else:
                    buyer_review = []
                if(Seller_Reviews.objects.filter(s_review_from=ordered_by_user,s_review_to=ordered_to_user).exists() == True):
                    seller_review = Seller_Reviews.objects.get(s_review_from=ordered_by_user,s_review_to=ordered_to_user)
                else:
                    seller_review = []
                return render(request , 'Dashboard/order_activity.html',{'req_check': requirements,"delivery":delivered,"order_by":ordered_by_user,"order_to":ordered_to_user,"requirements":requirements_lists,"conversation":conversation,"seller_gig":s_gig_list,"order_details":order_details,"delivery_status":delivery_status,"current_user":current_user,"offer_details":offer_details,"delivery_details":delivery_details_list,"message_char":message_char,"delivery_char":delivery_char,"cancel_char":cancel_char,"extra_offer":extra_offer,"buyer_user_name":buyer_user_name,"seller_user_name":seller_user_name,"conversation_id":str(conversation.id),"chat_words":json.dumps(chat_words),"five_chat_words":json.dumps(chat_words_5_words),"buyer_review":buyer_review,"seller_review":seller_review})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
    
class resolution_view(View):
    return_url = None
    def get(self , request,username='',orderid=0):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
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
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S")
                    except:
                        due_date = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f").date()
                        due_date_format = datetime.strptime(str(order_details.due_date),"%Y-%m-%d %H:%M:%S.%f")
                    end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    diff = relativedelta.relativedelta(due_date, end_date)
                    order_due_date = order_details.due_date
                    formatted_due_date = str(order_due_date.year) + "-" + str(order_due_date.month)+ "-" + str(order_due_date.day)  + " " + str(order_due_date.hour)+ ":" + str(order_due_date.minute)+ ":" + str(order_due_date.second)
                    num = float(diff.days)
                    if num > 0:
                        order_status = "In progress"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    elif num == 0:
                        order_status = "late"
                        formatted_due_date = "failed"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h"
                    else:
                        order_status = "late"
                        due_in_str = str(abs(diff.days)) + "d, " +  str(abs(diff.hours)) +"h late"
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
                
                s_gig_list.append({"gig_id":seller_gig_details.id, "gig_title":seller_gig_details.gig_title,"gig_image":imp_gig_image_url,"gig_username":ordered_to_user.username,"order_status":order_status,"due_in_days":d_days,"due_in_hour":d_hours,"due_in_minutes":d_minutes,"due_in_seconds":d_seconds,"due_date":order_details.due_date,"order_amount":str(order_details.order_amount),"gig_offer_amount":str(offer_details.offer_budget),"order_no":str(order_details.order_no),"formatted_due_date":formatted_due_date,"offer_extra":json.loads(offer_details.extra_parameters),"order_revisions":offer_details.no_revisions,"order_date":order_details.order_date})
                charcterlimits = CharacterLimit.objects.filter(Q(Char_category_Name= "resolution_text"))
                for c in charcterlimits:
                    if(c.Char_category_Name == "resolution_text"):
                        res_char = c.Max_No_of_char_allowed
                extra_days = Parameter.objects.filter(Q(parameter_name="res_days"))
                return render(request , 'Dashboard/resolution.html',{"seller_gig_details":s_gig_list,"resolution_char":res_char,"extra_days":extra_days})
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class account_settings_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:  
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
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')

class dashboard_view(View):
    return_url = None
    def get(self , request,username=''):
        if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
            # try:
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
            # except:
            #     return render(request , 'register.html')
        else:
            return render(request , 'register.html')
                
@csrf_exempt
def save_content_view(request):
    if request.method == 'POST':
        ucontent = request.POST.get("ucontent")
        upageName = request.POST.get("upageName")
        htmlcontent = ''
        with open("kworkapp/templates/"+upageName + '.html', 'r') as f:
            htmlcontent = f.read()
        soup=BeautifulSoup(htmlcontent,'html.parser')
        soup.find('div',attrs={"class":"all_page"}).replace_with(ucontent)
        with open("kworkapp/templates/"+upageName + '.html', "w", encoding = 'utf-8') as file:
            file.write(HTMLParser().unescape(str(soup.prettify()).replace("&lt;","<").replace("&gt;",">").replace("&nbsp;"," ").replace("&amp;","&").replace("&quot;",'"').replace("&apos;","'").replace("&cent;","¢").replace("&pound;","£").replace("&yen;","¥").replace("&euro;","€").replace("&copy;","©").replace("&reg;","®").replace("a&#769;","`").replace("a&#770;","^").replace("a&#771;","~").replace("a&#771;","~")))
        return HttpResponse('sucess')

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
            menulist = list(supportTopic.objects.order_by().values_list('topic_category').distinct())
            for m in menulist:
                if ''.join(map(str, m)).find("- ") == -1:
                    data.append({"title":str(''.join(map(str, m))),"actual_name":str(''.join(map(str, m))),"has_child":1})
        else:
            suport_topic = supportTopic.objects.get(support_topic_Name = umenuname)
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
                data.append({"title":title_name,"actual_name":m.map_to.support_topic_Name,"has_child":child})
        data.sort(key=operator.itemgetter('title'))
        return JsonResponse(data,safe=False)


@csrf_exempt
def get_menus_data_view(request):
    if request.method == 'GET':
        umenuname = request.GET['umenuname']
        data = []
        try:
            suport_topic = supportTopic.objects.get(support_topic_Name = umenuname)
            data1 = TopicDetails.objects.filter(topic_Name = suport_topic)
            for d in data1:
                data.append({"title":d.topic_Name.support_topic_Name,"contents":d.topic_Desc})
        except:
            data = []
        return JsonResponse(data,safe=False)

def SendEmailAct(sendto,message,subject):
    sender_address = 'info@letworkbedone.com'
    sender_password = 'xu11yC%5DF=Q'
    themsg = MIMEMultipart()
    themsg['Subject'] = subject
    themsg['To'] = sendto
    themsg['From'] = sender_address
    themsg.attach(MIMEText(message, 'html'))
    themsg = themsg.as_string()
    smtp = smtplib.SMTP_SSL('letworkbedone.com', 465)
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
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:15px;">Thank you for contacting Letsworkbedone Support. Your request ("""+ticket+""") has been received and will be reviewed by our support staff.</span>
    <span style="display:inline-block; vertical-align:middle; Padding:15px;"> Kindly note that our email support hours are from 8:00AM to 7:00PM (Saturday to Thursday) and we will attempt to get back to you as soon as possible during business hours.</span>
	  <span style="display:inline-block; vertical-align:middle; Padding:15px;"> You can add additional comments to your request by replying to this email.</span>
	    
  </td> 
                                </tr>
								<tr style="text-align:left;">
                                   <span style="display:inline-block; vertical-align:middle; Padding:15px;">Thank you</span>
								</tr>
								<tr style="text-align:left;">
                               <span style="display:inline-block; vertical-align:middle; Padding:15px;">Support</span>
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
                data1 = TopicDetails.objects.get(topic_Name = int(suport_topic.id))
                support_list.append(support.support_topic_Name)
                data.append({"title":data1.topic_Name.support_topic_Name,"contents":data1.topic_Desc})
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
        uip_address = str(whatismyip.whatismyip())
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
        userid = request.GET['userid']
        term_val = ''
        if userterms == "true": term_val = True
        else:
            term_val = False
        userDetails = User.objects.get(pk=userid)
        userDetails.country = usercountry
        userDetails.terms = term_val
        userDetails.profile_type = userrole
        userDetails.save()
    return HttpResponse("success")

def post_useremail_Details_view(request):
    if request.method == 'GET':
        useremail = request.GET['useremail']
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
                numberof_gigs = SellerLevels.objects.get(level_name=str(userDetails.seller_level))
                gigs_used = 0
                gig_id = 0
                if(UserGigs.objects.filter(user_id=userDetails).exists() == True):
                    gigs_used = UserGigs.objects.filter(user_id=userDetails).count()
                if(gigs_used == int(numberof_gigs.No_of_gigs)):
                    gig_id = 0
                else:
                    user_gig_obj = UserGigs(user_id=userDetails)
                    user_gig_obj.save()
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
        userDetails = User.objects.get(pk=userid)
        sub_subcatDetails = []
        category_inst = Categories.objects.get(id=select_id)
        _subcatDetails = SubSubCategories.objects.filter(category_Name= category_inst)
        for subcat in _subcatDetails:
            sub_subcatDetails.append({"cat_name":subcat.sub_sub_category_Name,"cat_id":subcat.id})
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
        return HttpResponse('sucess')

def get_gig_details_view(request):
    if request.method == 'GET':
        data = []
        u_gig_id = request.GET['u_gig_id']
        u_user_id = request.GET['u_user_id']
        userDetails =  User.objects.get(pk=u_user_id)
        gigDetails =  UserGigs.objects.get(pk=u_gig_id , user_id = userDetails)
        if(len(gigDetails.gig_title) != 0):
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
        userid = request.POST.get("userid")
        service_descp = request.POST.get("service_descp")
        service_images = request.POST.get("service_images")
        service_cat = request.POST.get("service_cat")
        service_sub_cat = request.POST.get("service_sub_cat")
        service_time = request.POST.get("service_time")
        service_price = request.POST.get("service_price")
        service_type = request.POST.get("service_type")
        send_to = request.POST.get("send_to")
        userDetails =  User.objects.get(pk=userid)
        category_details = Categories.objects.get(pk=service_cat)
        sub_category = SubSubCategories.objects.get(pk=service_sub_cat)
        if(service_type == 'individual'):
            send_to_user = User.objects.get(pk=userid)
            post_bu_req= Buyer_Post_Request(service_desc= service_descp,service_images=service_images,service_category=category_details,service_sub_category=sub_category,service_time=service_time,service_budget=service_price,user_id=userDetails,send_to=send_to_user,service_type=service_type)
            post_bu_req.save()
        else:
            post_bu_req= Buyer_Post_Request(service_desc= service_descp,service_images=service_images,service_category=category_details,service_sub_category=sub_category,service_time=service_time,service_budget=service_price,user_id=userDetails,service_type=service_type)
            post_bu_req.save()
        return HttpResponse('sucess')


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
                start_date = datetime.strptime(str(buyer_r.review_date), "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                diff = relativedelta.relativedelta(end_date, start_date)
                if(diff.years == 0 and diff.months == 0):
                    if(diff.days == 0):
                        review_date = 'today'
                    else:
                        review_date = str(diff.days) + ' days'
                elif(diff.months != 0 and diff.years == 0):
                    if(diff.months == 1):
                        review_date = str(diff.months) + ' month'
                    else:
                        review_date = str(diff.months) + ' months'
                elif(diff.years != 0):
                    if(diff.years == 1):
                        review_date = str(diff.years) + ' year'
                    else:
                        review_date = str(diff.years) + ' years'
                data.append({"message":buyer_r.review_message,"review_date":review_date,"rev_username":buyer_r.b_review_from.username,"user_profile":buyer_r.b_review_from.avatar}) 
        return JsonResponse(data,safe=False)
    
@csrf_exempt     
def add_referral_link_view(request):
    if request.method == 'GET':
        affiliate_code = request.GET['affiliate_code']
        userDetails = User.objects.get(affiliate_code=affiliate_code)
        ip_address = str(whatismyip.whatismyip())
        if(Referral_Users.objects.filter(affiliate_code=affiliate_code,ip_address=ip_address,refferal_user=None).exists() == False):
            referral_user = Referral_Users(affiliate_code=affiliate_code,ip_address=ip_address,user_id=userDetails)
            referral_user.save() 
        return HttpResponse('sucess')
    
def get_filter_gigs_details_view(request):
    if request.method == 'GET':
        category_name = request.GET['category_name']
        gig_data= []
        sub_Cat_Name = request.GET['sub_Cat_Name']
        category = SubCategories.objects.get(pk= category_name)
        if(len(sub_Cat_Name.strip()) !=0):
            subcat_inst = SubSubCategories.objects.get(sub_sub_category_Name= sub_Cat_Name)
            gig_details = UserGigs.objects.filter(gig_sub_category= subcat_inst)
        else:
            cat_int = Categories.objects.get(category_Name=category.category_Name)
            gig_details = UserGigs.objects.filter(gig_category= cat_int)
        for g in gig_details:
            seller_reviews = Seller_Reviews.objects.filter(package_gig_name= g)
            seller_count = 0
            for s_review in seller_reviews:
                seller_count = seller_count + int(s_review.average_val)
            try:
                seller_count = round(seller_count/len(seller_reviews),1)
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
            seller_levl= ''
            if(g.user_id.seller_level=="level1"):
                seller_levl = "New or higher"
            elif(g.user_id.seller_level=="level2"):
                seller_levl = "Advanced or higher"
            elif(g.user_id.seller_level=="level3"):
                seller_levl = "Professional"
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
  
def update_seller_offers():
    all_users = []
    all_users = User.objects.filter(Q(seller_level="level1") | Q(seller_level= "level2") | Q(seller_level= "level3"))
    for us in all_users:
        userDetails = User.objects.get(username = us.username)
        seller_object = SellerLevels.objects.get(level_name= us.seller_level)
        userDetails.offers_left = seller_object.No_of_offers
        userDetails.save()  


def spam_detection():
    print("123")
         
    
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
                    buyer_requests = Buyer_Post_Request.objects.filter(service_category= category_d ,service_status="active",service_date__range=(new_d, curr_date)).exclude(user_id= userDetails)
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
            buyer_requests = Buyer_Post_Request.objects.filter(service_category= category_d,service_status="active",service_date__range=(new_d, curr_date)).exclude(user_id= userDetails)
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
                seller_count = seller_count + int(s_review.average_val)
            try:
                seller_count = round(seller_count/len(seller_reviews),1)
            except:
                seller_count = 0
            seller_levl = ''
            user_details_off = User.objects.get(username = b_o.user_id.username)
            if(user_details_off.seller_level=="level1"):
                seller_levl = "New or higher"
            elif(user_details_off.seller_level=="level2"):
                seller_levl = "Advanced or higher"
            elif(user_details_off.seller_level=="level3"):
                seller_levl = "Professional"
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
        offers_sent = Request_Offers.objects.filter(user_id= userDetails)
        offers_sent_list = []
        for off in offers_sent:
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
        payment.token = 'FLWSECK_TEST-027992a01e7b87b0522d8b2141395a30-X'
        details = payment.get_payment_details(u_trans_id)
        flu_amout = details['data']['amount']
        flu_app_fee = details['data']['app_fee']
        flu_pay_type = details['data']['payment_type']
        flu_accnt_id = details['data']['account_id']
        flutt_flw_ref = details['data']['flw_ref']
        meta_data =  details['data']['meta']['data_extra']
        order_amount =  details['data']['meta']['base_price_wsdf']
        u_service_fees =  details['data']['meta']['token']
        u_base_price = request.GET['u_base_price']
        u_total_price = request.GET['u_total_price']
        data = []
        if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offers_sent,paid_by=pay_by_user,paid_to=pay_to_user).exists() == False):
            no_of_days = int(offers_sent.offer_time)
            Begindatestring = datetime.today()
            due_date = Begindatestring + timedelta(days=no_of_days)
            order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=order_amount,due_date=due_date)
            order_details.save()   
            order_details_get = User_orders.objects.get(pk = order_details.pk)
            try:    
                cover_detls = Order_Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
            except:
                cover_detls = Order_Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
            if(cover_detls == None):
                cover_detls = Order_Conversation(initiator=pay_by_user,receiver=pay_to_user,order_no=order_details_get)
                cover_detls.save()
            cover_detls =  Order_Conversation.objects.get(pk = cover_detls.pk)
            order_activity = User_Order_Activity(order_message="×1"+ str(gig_details.gig_title),order_amount=u_base_price,order_no = order_details_get)
            order_activity.save()
            user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='flutterwave',transaction_id=u_trans_id,payment_status=u_status,transaction_ref= u_trans_ref,payment_currency="USD",offer_amount=order_amount,total_amount=flu_amout,processing_fees= u_service_fees,flutter_fluw_ref= flutt_flw_ref,flutter_account_id=flu_accnt_id,flutter_app_fee=flu_app_fee,flutter_pay_type=flu_pay_type,paid_by=pay_by_user,paid_to=pay_to_user,order_no=order_details_get)
            user_trans.save()
            order_message = Order_Message(sender=pay_by_user,receiver=pay_to_user,text = "placed the order",conversation_id=cover_detls,order_no=order_details_get,message_type="chat")
            order_message.save()
            meta_data_list = meta_data.split(",")
            for meta in meta_data_list:
                if(meta != "None"):
                    extra_gig = UserExtra_gigs.objects.get(pk = int(meta))
                    user_extra_gig = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= extra_gig)
                    user_extra_gig.save()
                    
                    order_activity = User_Order_Activity(order_message="×1"+ str(extra_gig.extra_gig_title),order_amount=extra_gig.extra_gig_price,order_no = order_details_get)
                    order_activity.save()
                    
            data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username})
        else:
            order_details = User_orders.objects.get(package_gig_name= gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user)
            data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username})
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
        pay_by_user = User.objects.get(pk = u_user_id)
        offers_sent = Request_Offers.objects.get(pk= u_offer_id)
        pay_to_user = User.objects.get(pk = offers_sent.user_id.id)
        gig_details = UserGigs.objects.get(gig_title = offers_sent.gig_name.gig_title)
        data = []
        if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offers_sent,paid_by=pay_by_user,paid_to=pay_to_user).exists() == False):
            no_of_days = int(offers_sent.offer_time)
            Begindatestring = datetime.today()
            due_date = Begindatestring + timedelta(days=no_of_days)
            order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=u_base_price,due_date=due_date)
            order_details.save()
            order_details_get = User_orders.objects.get(pk = order_details.pk)
            try:    
                cover_detls = Order_Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
            except:
                cover_detls = Order_Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
            if(cover_detls == None):
                cover_detls = Order_Conversation(initiator=pay_by_user,receiver=pay_to_user,order_no=order_details_get)
                cover_detls.save()
            cover_detls =  Order_Conversation.objects.get(pk = cover_detls.pk)
            order_activity = User_Order_Activity(order_message="×1"+ str(gig_details.gig_title),order_amount=u_base_price,order_no = order_details_get)
            order_activity.save()
            user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='paypal',transaction_id=u_trans_id,payment_status=u_trans_status,payment_currency="USD",offer_amount=u_base_price,total_amount=u_total_price,processing_fees= u_service_fees,paypal_id=u_paypal_id,paypal_email=u_paypal_email,paid_by=pay_by_user,paid_to=pay_to_user,order_no=order_details_get)
            user_trans.save()
            meta_data_list = u_extra_gigs.split(",")
            for meta in meta_data_list:
                if(meta != "None"):
                    extra_gig = UserExtra_gigs.objects.get(pk = int(meta))
                    user_extra_gig = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= extra_gig)
                    user_extra_gig.save()
            data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username})
        else:
            order_details = User_orders.objects.get(package_gig_name= gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user)
            data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username})
        return JsonResponse(json.dumps(data),safe=False)


def post_mark_as_read_view(request):
    if request.method == 'GET':
        gig_id = request.GET['gig_id']
        user_id = request.GET['user_id']
        req_ques = request.GET['req_ques']
        order_no = request.GET['order_no']
        order_by_user = User.objects.get(username = user_id)
        gig_details = UserGigs.objects.get(pk = gig_id)
        order_details_get = User_orders.objects.get(order_no = order_no)
        b_reqs = Buyer_Requirements(gig_name=gig_details,requirement_ques=req_ques,user_id=order_by_user,default_req=True,order_no=order_details_get)
        b_reqs.save()
        return HttpResponse("sucess")
    
def post_buyer_requ_save_view(request):
    if request.method == 'GET':
        gig_id = request.GET['gig_id']
        user_id = request.GET['user_id']
        req_ques = request.GET['req_ques']
        req_ans = request.GET['req_ans']
        req_imgs = request.GET['req_imgs']
        order_no = request.GET['order_no']
        order_by_user = User.objects.get(username = user_id)
        gig_details = UserGigs.objects.get(pk = gig_id)
        order_details_get = User_orders.objects.get(order_no = order_no)
        b_reqs = Buyer_Requirements(gig_name=gig_details,requirement_ques=req_ques,user_id=order_by_user,default_req=False,requirement_ans=req_ans,req_documents=req_imgs,order_no=order_details_get)
        b_reqs.save()
        return HttpResponse("sucess")
    
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
                date_val = (tran.transaction_date).date()
                data.append({"t_date":date_val,"t_id":tran.transaction_id,"t_category":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name,"t_order_no":tran.order_no.order_no,"t_currency":"USD","t_amount":tran.total_amount})
        elif(cat_active== "yes"):
            sub_sub_cat_inst = SubSubCategories.objects.get(sub_sub_category_Name = category)
            user_transaction = User_Transactions.objects.filter(paid_by = userdetails)
            for tran in user_transaction:
                t_category = tran.gig_name.gig_sub_category.sub_sub_category_Name
                if(category == t_category):
                    date_val = (tran.transaction_date).date()
                    data.append({"t_date":date_val,"t_id":tran.transaction_id,"t_category":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name,"t_order_no":tran.order_no.order_no,"t_currency":"USD","t_amount":tran.total_amount})
        else:
            start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
            end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
            user_transaction = User_Transactions.objects.filter(paid_by = userdetails,transaction_date__range=(start_date, end_date))
            for tran in user_transaction:
                date_val = (tran.transaction_date).date()
                data.append({"t_date":date_val,"t_id":tran.transaction_id,"t_category":tran.offer_id.gig_name.gig_sub_category.sub_sub_category_Name,"t_order_no":tran.order_no.order_no,"t_currency":"USD","t_amount":tran.total_amount})
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
        try:    
            cover_detls = Order_Conversation.objects.get(initiator=delivered_to,receiver = delivered_by)
        except:
            cover_detls = Order_Conversation.objects.get(initiator=delivered_by,receiver = delivered_to)
        order_message = Order_Message(sender=delivered_by,receiver=delivered_to,text = "delivery",conversation_id=cover_detls,order_no=order_details,message_type="activity")
        order_message.save()
        resolution_interval_gap = 2
        get_message =  Order_Message.objects.get(pk = order_message.pk)
        resolution_ext = Addon_Parameters.objects.filter(Q(Char_category_Name="resolution_days") )
        for ext in resolution_ext:
            if(ext.parameter_name == "resolution_days"):
                resolution_interval_gap = ext.no_of_days
        today_date = datetime.today()
        last_date = today_date + timedelta(days=int(resolution_interval_gap))
        resolution= User_Order_Resolution(resolution_type="draft",resolution_text = "Delivery",resolution_message="Delivered",resolution_desc="successfuly delivered",resolution_status="pending",order_no=order_details,raised_by=delivered_by,raised_to=delivered_to,message=get_message , resolution_last_date= last_date)
        resolution.save()
        get_resolution =  User_Order_Resolution.objects.get(pk = resolution.pk)
        orde_delivery = Order_Delivery(delivery_message=d_message,attachment=d_images,order_no=order_details,delivered_by=delivered_by,delivered_to=delivered_to,delivery_status="delivered",resolution= get_resolution)
        orde_delivery.save()
        order_ativity = User_Order_Activity(order_message = "×1 Order Delivered" , order_no=order_details)
        order_ativity.save()
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
        try:    
            cover_detls = Order_Conversation.objects.get(initiator=delivered_to,receiver = delivered_by)
        except:
            cover_detls = Order_Conversation.objects.get(initiator=delivered_by,receiver = delivered_to)
        order_message = Order_Message(sender=delivered_by,receiver=delivered_to,text = "delivery",conversation_id=cover_detls,order_no=order_details,message_type="activity")
        order_message.save()
        get_message =  Order_Message.objects.get(pk = order_message.pk)
        today_date = datetime.today()
        last_date = today_date + timedelta(days=2)
        resolution = User_Order_Resolution(resolution_type="delivered",resolution_text = "Delivery",resolution_message="Delivered",resolution_desc="successfuly delivered",resolution_status="pending",order_no=order_details,raised_by=delivered_by,raised_to=delivered_to,message=get_message, resolution_last_date= last_date)
        resolution.save()
        get_resolution =  User_Order_Resolution.objects.get(pk = resolution.pk)
        orde_delivery = Order_Delivery(delivery_message=d_message,attachment=d_images,order_no=order_details,delivered_by=delivered_by,delivered_to=delivered_to,delivery_status="delivered",resolution= get_resolution)
        orde_delivery.save()
        order_ativity = User_Order_Activity(order_message = "×1 Order Delivered" , order_no=order_details)
        order_ativity.save()
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
            prev_date =  datetime.strptime(order_details.due_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            new_date = prev_date + timedelta(days=int(res_days))
        else:
            prev_date = datetime.today()
            new_date = datetime.today()
        try:    
            cover_detls = Order_Conversation.objects.get(initiator=raised_by_user,receiver = raised_to)
        except:
            cover_detls = Order_Conversation.objects.get(initiator=raised_to,receiver = raised_by_user)
        order_message = Order_Message(sender=raised_by_user,receiver=raised_to,text = res_message,conversation_id=cover_detls,order_no=order_details,message_type="activity")
        order_message.save()
        next_date = ''
        get_message =  Order_Message.objects.get(pk = order_message.pk)
        today_date = datetime.today()
        last_date = today_date + timedelta(days=2)
        resolution= User_Order_Resolution(resolution_type=res_type,resolution_text = res_text,resolution_message=res_message,resolution_desc=res_desc,resolution_status="pending",order_no=order_details,resolution_days=res_days,raised_by=raised_by_user,raised_to=raised_to,message=get_message,ext_prev_date= prev_date,ext_new_date=new_date, resolution_last_date= last_date)
        resolution.save()
        order_ativity = User_Order_Activity(order_message = "×1 Order " + res_type , order_no=order_details)
        order_ativity.save()
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
        data = []
        delivery_no=0
        order_details = User_orders.objects.get(order_no = order_no)
        cover_detls =  Order_Conversation.objects.get(pk = conver_id)
        all_messages = Order_Message.objects.filter(conversation_id= cover_detls, order_no= order_details)
        for all_m in all_messages:
            if(all_m.message_type == "chat"):
                attachment_str = ''
                if(all_m.attachment != None):
                    if(len(all_m.attachment.strip()) != 0):
                        attachment_str = all_m.attachment.strip()
                    else:
                        attachment_str = "None"
                else:
                    attachment_str = "None"
                data.append({"mssg_type":"chat","sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"attachment":attachment_str,"receiver_name":all_m.receiver.username,"mssg_time":all_m.timestamp})
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
                    data.append({"mssg_type":"activity","sender_username":all_m.sender.username,"sender_img":all_m.sender.avatar,"timestamp":all_m.timestamp,"message":all_m.text,"attachment":attachment_str,"receiver_name":all_m.receiver.username,"res_type":reolution_details.resolution_type,"res_status":reolution_details.resolution_status,"reciever_username":all_m.receiver.username,"reciever_img":all_m.receiver.avatar,"res_message":message_str,"res_prev_date":reolution_details.ext_prev_date,"res_next_date":reolution_details.ext_new_date,"res_last_date":reolution_details.resolution_last_date,"mssg_time":all_m.timestamp,"res_id":reolution_details.id,"del_descrp":delivery_description, "del_images":delivery_images,"delivery_No":delivery_no,"cancel_mssg":reolution_details.resolution_cancel_mssg})
        data.sort(key=operator.itemgetter('mssg_time'))
        return JsonResponse(data,safe=False)



def post_accept_click_view(request):
    if request.method == 'GET':
        res_id = request.GET['res_id']
        res_type = request.GET['res_type']
        pre_date = request.GET['pre_date']
        next_date = request.GET['next_date']
        res_details = User_Order_Resolution.objects.get(id = res_id)
        res_details.resolution_status = 'accepted'
        res_details.save()
        if(res_type == "extention"):
            order_details = User_orders.objects.get(order_no = res_details.order_no)
            order_details.due_date = next_date
            order_details.save()
        elif(res_type == "cancel"):
            order_details = User_orders.objects.get(order_no = res_details.order_no)
            order_details.order_status = 'cancel'
            order_details.save()
            refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res_details,order_no=order_details)
            refund_details.save()
        elif(res_type == "delivered"):
            order_details = User_orders.objects.get(order_no = res_details.order_no)
            service_fees_price = 0
            if(int(order_details.order_amount) <=40):
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
            clearencedate = today_date + timedelta(days=int(withdrwal_val))                
            order_details.order_status = 'completed'
            order_details.save()
            order_by =  User.objects.get(username= order_details.order_by.username)   
            order_to =  User.objects.get(username= order_details.order_to.username)  
            try:    
                cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
            except:
                cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)
                  
            refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=clearencedate,clearence_status="pending",cleared_on=None,user_id=order_to,earning_type="order",affiliate_user=None)
            refund_details.save()
            order_message = Order_Message(sender=order_by,receiver=order_to,text = "completed",conversation_id=cover_detls,order_no=order_details,message_type="activity")
            order_message.save()
            get_message =  Order_Message.objects.get(pk = order_message.pk)
            resolution= User_Order_Resolution(resolution_type="completed",resolution_text = "Completed",resolution_message="Completed",resolution_desc="successfuly completed",resolution_status="accepted",order_no=order_details,raised_by=order_by,raised_to=order_to,message=get_message)
            resolution.save()
            order_ativity = User_Order_Activity(order_message = "×1 Order Completed" , order_no=order_details)
            order_ativity.save()
        return HttpResponse('sucess')
    
def post_decline_click_view(request):
    if request.method == 'GET':
        res_id = request.GET['res_id']
        res_type = request.GET['res_type']
        res_text = request.GET['res_text']
        res_details = User_Order_Resolution.objects.get(id = res_id)
        res_details.resolution_status = 'rejected'
        res_details.resolution_cancel_mssg = res_text
        res_details.save()
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
        ord_details = User_orders.objects.get(order_no = order_no)
        orderedby_user = User.objects.get(username = ord_details.order_by.username)
        orderedto_user = User.objects.get(username = ord_details.order_to.username)
        gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)
        average_val =  round(float(int(s_comm) + int(s_serv)+ int(s_recomm) / 3),2)
        seller_reviews = Seller_Reviews(communication=s_comm,recommendation=s_recomm,service=s_serv,average_val=average_val,seller_response="",review_message=s_review_txt,order_no=ord_details,package_gig_name= gig_details,s_review_from=orderedby_user,s_review_to=orderedto_user,buyer_resp_date=None)
        seller_reviews.save()
        return HttpResponse('sucess')