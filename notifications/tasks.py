from .views import SendSMS, SendEmail
from celery import shared_task


@shared_task
def send_sms():
    return SendSMS()

@shared_task
def send_mail():
    return SendEmail()

    