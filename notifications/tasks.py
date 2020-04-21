# from .views import SendSMS, SendEmail
from celery import shared_task
import time
import string
import datetime
import decimal

from .send_sms import SendSMSAPI
from .send_email import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from loans.models import Loan
from savings_investments.models import SavingsAccount
from borrowers.models import InviteBorrower

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
def invite_borrowers():
    borrowers = InviteBorrower.objects.all()
    for borrower in borrowers:
        purpose = "register"
        sender = "admin@loanx.xyz"
        recepient = borrower.email_address
        send_mail(purpose, sender, recepient)

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


@shared_task
def CreditAccounts():
    savings_accounts = SavingsAccount.objects.all()
    for savings_account in savings_accounts:
        posting_frequency = savings_account.savings_product.interest_posting_frequency
        total_annual_interest = (((float(savings_account.savings_product.interest_rate_per_annum)/100))*(float(savings_account.available_balance)))
        match_selection = {"Every 1 Month":12,"Every 2 Month":6,"Every 3 Month":4,"Every 4 Month":3,"Every 6 Month":2,"Every 12 Month":1}
        
        def check_freq(freq):
            return match_selection[freq]
        print(type(savings_account.available_balance))
        print(type(savings_account.savings_product.interest_posting_frequency))
        savings_account.available_balance += decimal.Decimal(total_annual_interest/check_freq(savings_account.savings_product.interest_posting_frequency))
        savings_account.ledger_balance += decimal.Decimal(total_annual_interest/check_freq(savings_account.savings_product.interest_posting_frequency))
        savings_account.save()

        if(savings_account.savings_product.interest_posting_frequency == 'Every 1 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/12', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 2 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/6', **kwargs),
                    #'schedule': crontab(minute='07', hour='09', day_of_month='20', month_of_year='*/6', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 3 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/4', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 4 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/3', **kwargs),
                },
            }
            
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 6 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/2', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 12 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/1', **kwargs),
                },
            }

        return "successful"