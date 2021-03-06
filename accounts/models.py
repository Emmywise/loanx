from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils import timezone
from django.dispatch import receiver
import random
import decimal
from decimal import Decimal
import string
from datetime import timedelta
import datetime
import os

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=125)
    capital = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class Branch(models.Model):

    date_format_choices = (
        ('dd/mm/yyyy', '%d/%m/%Y'),
        ('mm/dd/yyyy', '%m/%d/%Y'),
        ('yyyy/mm/dd', '%Y/%m/%d')
    )

    holiday_effect_on_loan_schedule_choices = (
        ('Next day that is not a holiday', 'Next day that is not a holiday'),
        ('Next Repayment Cycle', 'Next Repayment Cycle')
    )

    name = models.CharField(max_length=400)
    open_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    currency = models.CharField(max_length=10)
    date_format = models.CharField(max_length=20, choices=date_format_choices)
    currency_in_words = models.CharField(max_length=225)
    address = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=400, blank=True, null=True)
    landline = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=400, blank=True, null=True)
    min_loan_amount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    max_loan_amount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    min_loan_interest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    max_loan_interest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_friday_branch_holiday = models.BooleanField(default=False)
    is_saturday_branch_holiday = models.BooleanField(default=False)
    is_sunday_branch_holiday = models.BooleanField(default=False)
    holiday_effect_on_loan_schedule = models.CharField(max_length=100,
                                                       choices=holiday_effect_on_loan_schedule_choices)
    capital = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    loan_generate_string = models.CharField(max_length=400) # unique prepend string eg BR-, ILR-
    open_date = models.DateField()
    is_open = models.BooleanField(default=False)
    remaining_capital = models.DecimalField(max_digits=100, decimal_places=2, blank=True, default=0.00)
    spent_capital = models.DecimalField(max_digits=100, decimal_places=2, blank=True, default=0.00)
    def __str__(self):
        return self.name

@receiver(pre_save, sender=Branch)
def update_remaining_capital(sender, instance, **kwargs):
    instance.remaining_capital = Decimal(instance.capital) - Decimal(instance.spent_capital)

@receiver(pre_save, sender=Branch)
def update_is_open(sender, instance, **kwargs):
    if instance.open_date <= datetime.date.today():
        instance.is_open = True




class BranchHoliday(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return self.branch.name + ' ' + str(self.date)


class BranchAdmin(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    admin = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Profile(models.Model):

    user_type_choices = (
        ('admin', 'admin'),
        ('staff', 'staff'),
        ('customer', 'customer')
    )

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    user_type = models.CharField(max_length=20, choices=user_type_choices)
    suspend = models.BooleanField(default=False)
    # user_role
    is_super_admin = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, blank=True, null=True)
    esignature = models.FileField(upload_to='esignature', blank=True, null=True)

    def __str__(self):
        return self.user.username


class SuspendedAccount(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.profile.user.first_name + ' ' + str(self.profile.user.last_name)


class AccountResetLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=400, blank=True, null=True, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)


def generate_token():
    token = ''
    for i in range(50):
        token += random.choice(string.ascii_letters + string.digits + string.hexdigits)
    return token


def reset_token(sender, instance, created, *args, **kwargs):
    if not instance.reset_token:
        instance.reset_token = generate_token()
        instance.save()


post_save.connect(reset_token, sender=AccountResetLink)
