<<<<<<< HEAD
#from .views import SendSMS, SendEmail
from celery import shared_task
from .send_sms import SendSMSAPI
=======
# from .views import SendSMS, SendEmail
from celery import shared_task
import time
import string
>>>>>>> 25e6c36653d6c5970ec80d687907cc23aa76f8c5

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

<<<<<<< HEAD
@shared_task
def send_sms():
    return SendSMSAPI()
    

@shared_task
def send_mail(purpose, sender, recipient):
    mail_instance = SendEmail()
    #mail_instance.send_mail(invite new borrowers, )
    return mail_instance()
=======

def print_random_string():
    # time.sleep(1)
    print('random string')
    return 'radafds'

>>>>>>> 25e6c36653d6c5970ec80d687907cc23aa76f8c5

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