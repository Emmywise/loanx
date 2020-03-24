from django.db import models
from accounts.models import Branch
from django.core.validators import validate_comma_separated_integer_list

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


class AssetType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Asset(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    purchased_date = models.DateField(blank=True, null=True)
    purchased_price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    replacement_value = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    serial_number = models.CharField(max_length=400, blank=True, null=True)
    bought_form = models.CharField(max_length=400)
    description = models.TextField()

    def __str__(self):
        return self.name


class AssetDocument(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    document = models.FileField(upload_to='assets')


class CustomAssetField(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    field = models.CharField(max_length=125)
    text_field = models.TextField(blank=True, null=True)
    date_field = models.DateField(blank=True, null=True)
    integer_field = models.PositiveIntegerField(blank=True, null=True)
    decimal_field = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    url_field = models.URLField(max_length=500, blank=True, null=True)
    text_area = models.TextField(blank=True, null=True)
    dropdown_values = models.TextField(blank=True, null=True, validators=[validate_comma_separated_integer_list])
    dropdown = models.CharField(max_length=200, blank=True, null=True)
    file_upload = models.FileField(upload_to='asset', blank=True, null=True)


class AssetValuation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    valuation_date = models.DateField()
    value_amount = models.DecimalField(max_digits=100, decimal_places=2)


class ExpensesType(models.Model):
    title = models.CharField(max_length=125)

    def __str__(self):
        return self.title


class Expense(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    expenses_type = models.ForeignKey(ExpensesType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
    # link_to_loan = models.ForeignKey(Loan, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurring_time = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.expenses_type.title


class ExpenseDocument(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    document = models.FileField(upload_to='expenses')

    def __str__(self):
        return self.expense.expenses_type.title


class CustomExpenseField(models.Model):

    asset = models.ForeignKey(Expense, on_delete=models.CASCADE)
    field = models.CharField(max_length=125)
    text_field = models.TextField(blank=True, null=True)
    date_field = models.DateField(blank=True, null=True)
    integer_field = models.PositiveIntegerField(blank=True, null=True)
    decimal_field = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    url_field = models.URLField(max_length=500, blank=True, null=True)
    text_area = models.TextField(blank=True, null=True)
    dropdown_values = models.TextField(blank=True, null=True, validators=[validate_comma_separated_integer_list])
    dropdown = models.CharField(max_length=200, blank=True, null=True)
    file_upload = models.FileField(upload_to='expenses', blank=True, null=True)



