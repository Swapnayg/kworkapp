
import requests
import pycountry

from kworkapp.models import Languages, User, UserLanguages, UserProfileDetails

def get_avatar(backend, strategy, details, response,user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        url = response['picture']
        ext = url.split('.')[-1]
    url_req = 'http://ipinfo.io/json'
    response = requests.get(url_req)
    data = response.json()
    country_name = pycountry.countries.get(alpha_2=data["country"])
    user.country = data["country"]
    if url:
        user.avatar = url
    user.save()
    userDetails = User.objects.get(pk=user.id)
    if(UserProfileDetails.objects.filter(user_id=userDetails).exists() == False):
        userprofile = UserProfileDetails(profile_title="",profess_overview="",user_id=userDetails)
        userprofile.save()
    if(UserLanguages.objects.filter(user_id=userDetails).exists() == False):
        language = Languages.objects.get(lng_Name="English")
        userlanguages = UserLanguages(language_name=language,lang_prof="Basic",user_id=userDetails)
        userlanguages.save()