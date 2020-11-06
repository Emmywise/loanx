from django.db import models
from accounts.models import Profile, Branch
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

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
    pay_date = models.DateField()

    def __str__(self):
        return self.staff.user.username


@receiver(pre_save, sender=Payroll)
def calculate_payroll(sender, instance, raw, **kwargs):
    instance.total_pay = 0
    if instance.basic_pay:
        instance.total_pay = instance.total_pay + instance.basic_pay
    if instance.overtime_pay:
        instance.total_pay = instance.total_pay + instance.overtime_pay
    if instance.paid_leaves:
        instance.total_pay = instance.total_pay + instance.paid_leaves
    if instance.transport_allowance:
        instance.total_pay = instance.total_pay + instance.transport_allowance
    if instance.medical_allowance:
        instance.total_pay = instance.total_pay + instance.medical_allowance
    if instance.bonus:
        instance.total_pay = instance.total_pay + instance.bonus
    if instance.other_allowances:
        instance.total_pay = instance.total_pay + instance.other_allowances

    instance.total_deduction = 0
    if instance.pension:
        instance.total_deduction = instance.total_deduction + instance.pension
    if instance.health_insurance:
        instance.total_deduction = instance.total_deduction + instance.health_insurance
    if instance.unpaid_leave:
        instance.total_deduction = instance.total_deduction + instance.unpaid_leave
    if instance.tax_deduction:
        instance.total_deduction = instance.total_deduction + instance.tax_deduction
    if instance.salary_loan:
        instance.total_deduction = instance.total_deduction + instance.salary_loan

    instance.net_pay = instance.total_pay - instance.total_deduction


# @receiver(post_save, sender=Payroll)
# def configure_recurring_and_send_slip(sender, instance, created):
#     pass

class Staff(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.SET_NULL, default='', null=True)

    def __str__(self):
        return self.user_id.user.first_name + ' ' + str(self.user_id.user.last_name) + ' - ' + str(self.user_id.branch)
