from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from rest_framework import status

def send_mail(purpose, sender, recepient):
    try:
        subject, from_email, to = purpose, \
                                sender, recepient
        text_content = 'Hey please reset password'
        html_content = '<p>Hey please reset password .' \
                    '</p>' 
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return {"message": "Success", "status":status.HTTP_200_OK}
    except:
        return {"message": "Failed", "status":status.HTTP_400_BAD_REQUEST}