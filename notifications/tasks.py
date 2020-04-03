#from .views import SendSMS, SendEmail
from celery import shared_task
from .send_sms import SendSMSAPI

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

@shared_task
def send_sms():
    return SendSMSAPI()
    

@shared_task
def send_mail(purpose, sender, recipient):
    mail_instance = SendEmail()
    #mail_instance.send_mail(invite new borrowers, )
    return mail_instance()

# @shared_task
# def send_sms():
#     return SendSMS()

# @shared_task
# def send_mail():
#     return SendEmail()

@shared_task
def create_random_user_accounts(total):
    # for i in range(total):
    #     username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
    #     email = '{}@example.com'.format(username)
    #     password = get_random_string(50)
    #     User.objects.create_user(username=username, email=email, password=password)
    print('working')
    return '{} random users created with success!'.format(total)