# from .views import SendSMS, SendEmail
from celery import shared_task
import time
import string
import datetime

from .send_sms import SendSMSAPI
from .send_email import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from loans.models import Loan

@shared_task
def send_sms():
    return SendSMSAPI()
    

# @shared_task
# def send_mail(purpose, sender, recipient):
#     mail_instance = SendEmail()
#     #mail_instance.send_mail(invite new borrowers, )
#     return mail_instance()

def print_random_string():
    # time.sleep(1)
    print('random string')
    return 'radafds'


# @shared_task
# def send_sms():
#     return SendSMSAPI()

@shared_task
def send_mail_task(purpose, sender, recepient):
    return send_mail(purpose, sender, recepient)

@shared_task
def create_random_user_accounts(total):
    # for i in range(total):
    #     username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
    #     email = '{}@example.com'.format(username)
    #     password = get_random_string(50)
    #     User.objects.create_user(username=username, email=email, password=password)
    print('working')
    return '{} random users created with success!'.format(total)


@shared_task
def mark_overdue_loans():
    filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(remaining_balance__gt = 0)
    if (len(filtered_loans) != 0):
        for f in filtered_loans:
            print(f)
            send_mail('your mail is overdue', 'leke@tcore.uk', 'lexmill99@gmail.com')
            if f.maturity_date == datetime.date.today():
                f.status = "due today"
                f.save()
            else:
                f.status = "past maturity"
                f.save()
        return "code ran successfully"
    return "code ran successfully"

