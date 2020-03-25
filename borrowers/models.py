from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import os
# Create your models here.


class Borrower(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    )
    title_choices = (
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss', 'Miss'),
        ('Dr.', 'Dr.'),
        ('Ms.', 'Ms.'),
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
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
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
    date_of_birth = models.DateTimeField()
    address = models.CharField(
        max_length=400)
    city = models.CharField(
        max_length=400)
    state = models.CharField(
        max_length=400)
    zip_code = models.CharField(
        max_length=400)
    land_line = models.CharField(
        max_length=400)
    working_status = models.CharField(
        choices=working_status_choices, max_length=100)
    borrower_photo = models.ImageField(blank=True, null=True)
    description = models.CharField(
        max_length=400)
    is_activated = models.BooleanField(default=False)

    borrower_group = models.ManyToManyField(
        "BorrowerGroup")


class BorrowerGroup(models.Model):
    group_name = models.CharField(max_length=255)
    group_leader = models.ForeignKey(Borrower, on_delete=models.DO_NOTHING)
    meeting_date = models.DateTimeField()
    description = models.CharField(max_length=255, null=True, blank=True)
