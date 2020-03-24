from django.db import models
from accounts.models import Profile, Branch

# Create your models here.


class Payroll(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    staff = models.ForeignKey(Profile, on_delete=models.CASCADE)
    basic_pay = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    overtime_pay = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    paid_leaves = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    transport_allowance = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    medical_allowance = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    bonus = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    other_allowances = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    total_pay = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    pension = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    health_insurance = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    unpaid_leave = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    tax_deduction = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    salary_loan = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    total_deduction = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    net_pay = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurring_date = models.CharField(max_length=125, blank=True, null=True)
    send_slip_to_staff_email = models.BooleanField(default=False)

    def __str__(self):
        return self.staff.user.username
