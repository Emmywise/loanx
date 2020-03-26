from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from accounts.models import Branch

# Create your models here.


class CalendarEvent(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    title = models.CharField(max_length=125)
    when_date = models.DateTimeField()
    from_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class CalendarEventEmail(models.Model):
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    email = models.EmailField(max_length=225)

    def __str__(self):
        return self.email


class CalendarLog(models.Model):

    log_type_choices = (
        ('Disbursed', 'Disbursed'),
        ('Due Amount', 'Due Amount'),
        ('Maturity', 'Maturity'),
        ('Payment Schedule', 'Payment Schedule')
    )

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    log_type = models.CharField(max_length=100, choices=log_type_choices)
    url_path = models.CharField(max_length=400)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date)


class OtherIncomeType(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class OtherIncome(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    income_type = models.ForeignKey(OtherIncomeType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    link_to_loan = models.URLField(max_length=400, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurring = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class OtherIncomeDocuments(models.Model):
    other_income = models.ForeignKey(OtherIncome, on_delete=models.CASCADE)
    document = models.FileField(upload_to='other_income')


class CustomOtherIncomeField(models.Model):

    asset = models.ForeignKey(OtherIncome, on_delete=models.CASCADE)
    field = models.CharField(max_length=125)
    text_field = models.TextField(blank=True, null=True)
    date_field = models.DateField(blank=True, null=True)
    integer_field = models.PositiveIntegerField(blank=True, null=True)
    decimal_field = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    url_field = models.URLField(max_length=500, blank=True, null=True)
    text_area = models.TextField(blank=True, null=True)
    dropdown_values = models.TextField(blank=True, null=True, validators=[validate_comma_separated_integer_list])
    dropdown = models.CharField(max_length=200, blank=True, null=True)
    file_upload = models.FileField(upload_to='other_income', blank=True, null=True)
