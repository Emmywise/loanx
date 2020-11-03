from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from accounts.models import Profile, Country
import os
# Create your models here.


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
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
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
        choices=working_status_choices, max_length=100)
    borrower_photo = CloudinaryField('image',null=True, blank=True)
    description = models.CharField(
        max_length=400)
    is_activated = models.BooleanField(default=False)
    loan_score = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


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
    email_address = models.CharField(max_length=255)