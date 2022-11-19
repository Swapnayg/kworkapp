from kworkapp.models import  Conversation,Message,User
from django.db.models import Q
from kworkapp.models import Categories,SubCategories,SubSubCategories,Api_keys,User_warning,User
import json
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone

def message_processor(request):
    frndData =[]
    if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
        try:
            UserDetails = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
            friends = Conversation.objects.filter(Q(initiator = UserDetails) | Q(receiver = UserDetails))
            #c_img = UserProfileDetails.get_userdetails_by_id(id = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id))
            #c_status = UserprivacySettings.get_userprivacydetails_by_id(id = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id))
            friendCount = len(friends)
            if(friendCount!= 0):
                for f in friends:
                    friendId = 0
                    userDetails1 = ''
                    userDetails2 = ''
                    conves_id= f.id
                    if(UserDetails.id == f.initiator.id):
                        friendId = f.receiver.id
                        userDetails1 = User.objects.get(id=friendId)
                        userDetails2 = User.objects.get(id=f.initiator.id)
                    elif(UserDetails.id == f.receiver.id):
                        friendId = f.initiator.id
                        userDetails1 = User.objects.get(id=friendId)
                        userDetails2 = User.objects.get(id=f.receiver.id)
                    requestobj = ''
                    # try:
                    #     requestobj = Friendship.objects.get((Q(user=userDetails1, friend=userDetails2) | Q(user=userDetails2, friend=userDetails1)))
                    # except:
                    #     requestobj = Friendship.objects.get((Q(user=userDetails1, friend=userDetails2) | Q(user=userDetails2, friend=userDetails1)))
                    req_status = ''
                    if(requestobj.friend.email == UserDetails.email):
                        req_status = "accepted"
                    else:
                        req_status = "sent"
                    # try:
                    #     userProfile = UserProfileDetails.objects.get(id=friendId)
                    # except:                            
                    #     userProfile = []
                    # try:
                    #     userAvailable = UserprivacySettings.objects.get(id=friendId)
                    # except:                            
                    #     userAvailable = []
                    # try:
                    #     workDetails =  UserWorkPlaceDetails.objects.filter(id=friendId).latest('id')
                    #     userExp = str(workDetails.designation_name).title()
                    # except:                            
                    #     userExp = "Fresher"
                    # skillDetails =  UserProfessionalDetails.objects.filter(user_id=userDetails1)
                    # skillstr = ''
                    # for s in skillDetails:
                    #     skillstr = skillstr + str(s.skill_Name) + ", "
                    #     userLang = ''
                    #     langauges = UserLanguages.get_userlanguage_by_id(id = User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id))
                    #     if(langauges.user_english != "no"):
                    #         userLang + langauges.user_english.title() +","
                    #     if(langauges.user_french != "no"):
                    #         userLang + langauges.user_english.title() +","
                    #     if(langauges.user_italian != "no"):
                    #         userLang + langauges.user_english.title() +","
                    #     if(langauges.user_hindi != "no"):
                    #         userLang + langauges.user_english.title() +","
                    #     if(langauges.user_spanish != "no"):
                    #         userLang + langauges.user_english.title() +","
                    #     if(langauges.user_arabic != "no"):
                    #         userLang + langauges.user_english.title() +","
                    #     if(userLang == ''): 
                    #         userLang = "English"
                    # frndData.append({"userDetails":userDetails1,"user_profile":userProfile,"req_status":req_status,"skillDetails":skillstr[:-2],"userAvailable":userAvailable,"experience":userExp,"langauges":userLang,"convs_id":conves_id}) 
            else:
                frndData = []
        except:
            frndData = []
    return {
        'friends' : frndData
    }

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    logged_usesList = User.objects.filter(id__in=user_id_list)
    users_data = []
    for u in logged_usesList:
        if(u.username != "admin"):
            users_data.append({"name":u.username})
    return json.dumps(users_data)

def menu_procesor(request):
    sub_menulist = []
    menu_list = []
    user_warning = ''
    user_blocked = ''
    categories = Categories.objects.all()
    if((request.session.get('userEmail'))!=None or ((request.user!=None) and (len(str(request.user.username).strip())) != 0)):
        userDetails =  User.objects.get(pk=request.session.get('userId')  if request.session.get('userId') !=None else request.user.id)
        user_warning = ''
        try:
            get_warning = User_warning.objects.get(user_id = userDetails , confirmed_status= False) 
            if(get_warning != None):
                user_warning = "yes"
        except:
            user_warning = "no"
        if(userDetails.profile_status == "blocked"):
            user_blocked = "yes"
        else:
            user_blocked = "no"
            
    for i,c in enumerate(categories):
        menu_list.append({"name":c.category_Name,'image':c.image})
        category_int = Categories.objects.get(category_Name= c.category_Name)
        subcategories = SubSubCategories.objects.filter(category_Name=category_int)
        for j,ssc in enumerate(subcategories):
            sub_menulist.append({"name":ssc.sub_sub_category_Name,"menu":c.category_Name,"subcategory":ssc.sub_category_Name.sub_category_Name})
    return {
        'main_menu' : menu_list,
        'sub_menu' : json.dumps(sub_menulist),
        "warning_message":user_warning,
        "block_message":user_blocked,
        "session_users":get_current_users()
    }



def set_settings(request):
    api_details = Api_keys.objects.filter(Q(api_name="google") | Q(api_name= "facebook"))
    for api in api_details:
        if(api.api_name == "google"):
            settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = api.private_key
            settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = api.secrete_key
        elif(api.api_name == "facebook"):
            settings.SOCIAL_AUTH_FACEBOOK_KEY = api.private_key
            settings.SOCIAL_AUTH_FACEBOOK_SECRET = api.secrete_key
    return {
        'settings_val' : 'true',
    }
