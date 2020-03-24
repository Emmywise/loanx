from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from accounts.models import Profile, Branch
# Create your models here.


data_type_choices = (
        ('text_field', 'text_field'),
        ('date_field', 'date_field'),
        ('integer_field', 'integer_field'),
        ('decimal_field', 'decimal_field'),
        ('url_field', 'url_field'),
        ('text_area', 'text_area'),
        ('dropdown', 'dropdown'),
        ('file_upload', 'file_upload'),
    )


class SavingsProduct(models.Model):
    interest_method_choices = (
        ('Last Savings Balance', 'Last Savings Balance'),
        ('Pro-Rata Basis', 'Pro-Rata Basis')
    )
    name = models.CharField(max_length=125)
    interest_rate_per_anum = models.DecimalField(max_digits=10, decimal_places=2)
    interest_method = models.CharField(max_length=100, choices=interest_method_choices)
    interest_posting_frequency = models.CharField(max_length=300, blank=True, null=True)
    interest_addition_time = models.CharField(max_length=300, blank=True, null=True)
    min_balance_for_interest = models.DecimalField(max_digits=100, decimal_places=2)
    overdrawn = models.BooleanField(default=False)
    min_balance_for_withdrawal = models.DecimalField(max_digits=100, decimal_places=2)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name


class SavingsAccount(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    savings_product = models.ForeignKey(SavingsProduct, on_delete=models.DO_NOTHING)
    savings_id = models.CharField(max_length=125, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    available_balance = models.DecimalField(max_digits=100, decimal_places=2)
    ledger_balance = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.savings_id


class CustomSavingsAccountField(models.Model):

    asset = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE)
    field = models.CharField(max_length=125)
    text_field = models.TextField(blank=True, null=True)
    date_field = models.DateField(blank=True, null=True)
    integer_field = models.PositiveIntegerField(blank=True, null=True)
    decimal_field = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    url_field = models.URLField(max_length=500, blank=True, null=True)
    text_area = models.TextField(blank=True, null=True)
    dropdown_values = models.TextField(blank=True, null=True, validators=[validate_comma_separated_integer_list])
    dropdown = models.CharField(max_length=200, blank=True, null=True)
    file_upload = models.FileField(upload_to='savings_accounts', blank=True, null=True)

