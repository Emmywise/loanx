from django.db import models
from django.db.models.signals import post_save
# Create your models here.


class SMS(models.Model):
    status_choices = (
        ('sent', 'sent'),
        ('pending', 'pending'),
        ('failed', 'failed'),
    )
    message_purpose_choices = (
        ('to_all_borrowers', 'to_all_borrowers'),
        # ('delivered', 'delivered'),
        # ('failed', 'failed'),
    )
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=status_choices, max_length=100)
    message_purpose = models.CharField(
        choices=message_purpose_choices, max_length=100)


# def send_msg():
#     return 'sent'


# def check_status(sender, instance, created, *args, **kwargs):
#     if not instance.send_message:
#         instance.status = send_msg()
#         instance.save()


# post_save.connect(check_status, sender=SendSMS)


class SendEmail(models.Model):
    status_choices = (
        ('sent', 'sent'),
        ('delivered', 'delivered'),
        ('failed', 'failed'),
    )
    message_purpose_choices = (
        ('Message to all borrowers', 'Message to all borrowers'),
        ('invite new borrowers', 'invite new borrowers'),
        ('loan remainder', 'loan remainder'),
        ('successful repayment', 'successful repayment'),
        ('daily collection', 'daily collection'),
        ('e-signature', 'e-signature'),
        ('payroll payslip', 'payroll payslip'),
    )
    message = models.CharField(
        max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=status_choices, max_length=100)
    message_purpose = models.CharField(
        choices=message_purpose_choices, max_length=100)


def send_email():
    return 'sent'


def check_status_mail(sender, instance, created, *args, **kwargs):
    if not instance.send_email:
        instance.status = send_email()
        instance.save()


post_save.connect(check_status_mail, sender=SendEmail)
