from django.db import models
from accounts.models import Branch

class CashFlow(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    branch_capital = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    payroll = models.DecimalField(max_digits=10, decimal_places=2)
    loan_released = models.DecimalField(max_digits=10, decimal_places=2)
    loan_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawal = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
