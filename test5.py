from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives

subject= 'hello'
to = 'infoswap90@gmail.com'
html_content = '<p>This is an <strong>important</strong> message.</p>'

def sendMail_SMTP(subject,msg,to):
    msgg = ''
    res = EmailMultiAlternatives(subject, "msg", settings.EMAIL_HOST_USER, [to])
    res.attach_alternative(msg, "text/html")
    res.send() 
    if(res == 1):  
        msgg = "Mail Sent Successfuly"  
    else:  
        msgg = "Mail could not sent"  
    return HttpResponse(msgg)

sendMail_SMTP(subject,html_content,to)
