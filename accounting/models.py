from django.db import models


class CashFlow(models.Model):
    branch_capital = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    payroll = models.DecimalField(max_digits=10, decimal_places=2)
    loan_released = models.DecimalField(max_digits=10, decimal_places=2)
    loan_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawal = models.DecimalField(max_digits=10, decimal_places=2)
