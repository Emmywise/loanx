from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from accounts.models import Profile, Country
import loans.models
from loans.models import LoanOfficer
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import random
import string

# Create your models here.


#def random_ref_generator(size=20, chars=string.ascii_letters + string.digits):
#    return ''.join(random.choice(chars) for _ in range(size))

#ref_gen = random_ref_generator()

class Borrower(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'), 
    )
    title_choices = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Dr', 'Dr'),
        ('Ms', 'Ms'),
        ('Rev', 'Rev'),
    )
    working_status_choices = (
        ('Employer', 'Employer'),
        ('Government Employee', 'Government Employee'),
        ('Private Sector', 'Private Sector'),
        ('Employee', 'Employee'),
        ('Owner', 'Owner'),
        ('Student', 'Student'),
        ('Overseas Worker', 'Overseas Worker'),
        ('Pensioner', 'Pensioner'),
        ('Unemployed', 'Unemployed'),
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    profile = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    borrower_uid = models.CharField(verbose_name='Borrower Unique ID', max_length=50, blank=True, default='')
    first_name = models.CharField(
        max_length=400)
    middle_name = models.CharField(
        max_length=400)
    last_name = models.CharField(
        max_length=400)
    business_name = models.CharField(
        max_length=400, null=True, blank=True)
    gender = models.CharField(
        choices=gender_choices, max_length=100)
    title = models.CharField(
        choices=title_choices, max_length=100)
    mobile = models.CharField(
        max_length=11)
    email = models.EmailField(max_length=100)
    date_of_birth = models.CharField(
        max_length=400)
    address = models.CharField(
        max_length=400)
    city = models.CharField(
        max_length=400)
    state = models.CharField(
        max_length=400)
    zip_code = models.CharField(
        max_length=400, blank=True, null=True)
    land_line = models.CharField(
        max_length=400, blank=True, null=True)
    working_status = models.CharField(
        choices=working_status_choices, max_length=100, blank=True)
    borrower_photo = CloudinaryField('image',null=True, blank=True)
    description = models.CharField(
        max_length=400)
    authorization_code = models.CharField(max_length=125, blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    loan_score = models.PositiveIntegerField(blank=True, null=True)
    loan_officer = models.ForeignKey(LoanOfficer, on_delete=models.SET_NULL, verbose_name='Loan Officer', null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

@receiver(pre_save, sender=Borrower)
def update_borrower_uid(sender, instance, **kwargs):
    mobile = instance.mobile
    if len(mobile) > 10:
        m = mobile.startswith("234")
        if m:
            s = mobile[3:]
            instance.borrower_uid = s
        else:
            s = mobile[1:]
            instance.borrower_uid = s
    else:
        instance.borrower_uid = mobile


class BorrowerGroup(models.Model):
    group_name = models.CharField(max_length=255)
    group_leader = models.ForeignKey(Borrower, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='group_leader')
    meeting_date = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    members = models.ManyToManyField(Borrower, through='Membership')
    def __str__(self):
        return self.group_name


class Membership(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrower_group = models.ForeignKey(BorrowerGroup, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.borrower.first_name + " " + "in" + " "+ self.borrower_group.group_name


class InviteBorrower(models.Model):
    email_address = models.CharField(max_length=255, default='', blank=False)

    def __str__(self):
        return self.email_address