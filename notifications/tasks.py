#from .views import SendSMS, SendEmail
from celery import shared_task
from .send_sms import SendSMSAPI


@shared_task
def send_sms():
    return SendSMSAPI()
    

@shared_task
def send_mail(purpose, sender, recipient):
    mail_instance = SendEmail()
    #mail_instance.send_mail(invite new borrowers, )
    return mail_instance()

    