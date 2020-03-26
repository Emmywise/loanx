from django.db import models
from accounts.models import Profile, Branch


class BranchCapital(models.Model):
    branch_capital_date = models.DateField()
    amount = models.PositiveIntegerField(default=0)
    description = models.CharField(
        max_length=400, blank=True, null=True)


class Month(models.Model):
    month_choices = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    )
    month = models.CharField(
        choices=month_choices, max_length=400, blank=True, null=True)


class CashFlowAccumulated(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    date = models.DateField()
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    # CASH FLOW ACCUMULATED
    # receipts
    branch_capital = models.ForeignKey(
        BranchCapital, on_delete=models.DO_NOTHING)
    loan_principal_repayment = models.CharField(
        max_length=400, blank=True, null=True)
    loan_interest_repayment = models.CharField(
        max_length=400, blank=True, null=True)
    loan_penalty_repayment = models.CharField(
        max_length=400, blank=True, null=True)
    loan_fees_repayment = models.CharField(
        max_length=400, blank=True, null=True)
    deductable_loan_fees = models.CharField(
        max_length=400, blank=True, null=True)
    savings_deposit = models.CharField(
        max_length=400, blank=True, null=True)
    savings_fees = models.CharField(
        max_length=400, blank=True, null=True)
    savings_commissions = models.CharField(
        max_length=400, blank=True, null=True)
    savings_transfer_in = models.CharField(
        max_length=400, blank=True, null=True)
    other_income = models.CharField(
        max_length=400, blank=True, null=True)
    total_receipts = models.CharField(
        max_length=400, blank=True, null=True)
    # payments
    expenses = models.CharField(
        max_length=400, blank=True, null=True)
    payroll = models.CharField(
        max_length=400, blank=True, null=True)
    loan_released = models.CharField(
        max_length=400, blank=True, null=True)
    savings_withdrawals = models.CharField(
        max_length=400, blank=True, null=True)
    savings_transfers_out = models.CharField(
        max_length=400, blank=True, null=True)
    total_payments = models.CharField(
        max_length=400, blank=True, null=True)
    total_cash_balance = models.CharField(
        max_length=400, blank=True, null=True)

    # CASH FLOW MONTHLY


class CashFlowMonthly(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    date = models.DateField()
    opening_balance = models.CharField(
        max_length=400, blank=True, null=True)
    # receipts
    branch_capital = models.ForeignKey(
        BranchCapital, on_delete=models.DO_NOTHING)
    loan_principal_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    loan_interest_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    loan_penalty_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    loan_fees_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    deductable_loan_fees = models.CharField(
        max_length=400, blank=True, null=True)
    savings_deposit = models.CharField(
        max_length=400, blank=True, null=True)
    savings_fees = models.CharField(
        max_length=400, blank=True, null=True)
    savings_commissions = models.CharField(
        max_length=400, blank=True, null=True)
    savings_transfer_in = models.CharField(
        max_length=400, blank=True, null=True)
    other_income = models.CharField(
        max_length=400, blank=True, null=True)
    total_receipts = models.CharField(
        max_length=400, blank=True, null=True)
    # payments
    expenses = models.CharField(
        max_length=400, blank=True, null=True)
    payroll = models.CharField(
        max_length=400, blank=True, null=True)
    loan_released = models.CharField(
        max_length=400, blank=True, null=True)
    savings_withdrawals = models.CharField(
        max_length=400, blank=True, null=True)
    savings_transfers_out = models.CharField(
        max_length=400, blank=True, null=True)
    total_payments = models.CharField(
        max_length=400, blank=True, null=True)
    total_cash_balance = models.CharField(
        max_length=400, blank=True, null=True)


class CashFlowProjection(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    date = models.DateField()
    operating_cash_beginning = models.CharField(
        max_length=400, blank=True, null=True)
    # receipts
    branch_capital = models.CharField(
        max_length=400, blank=True, null=True)
    principal_collections = models.CharField(
        max_length=400, blank=True, null=True)
    interest_collections = models.CharField(
        max_length=400, blank=True, null=True)
    fees_collections = models.CharField(
        max_length=400, blank=True, null=True)
    penalty_collections = models.CharField(
        max_length=400, blank=True, null=True)
    savings_deposits = models.CharField(
        max_length=400, blank=True, null=True)
    other_income = models.CharField(
        max_length=400, blank=True, null=True)
    total_receipts = models.CharField(
        max_length=400, blank=True, null=True)
    # payments
    loan_disbursements = models.CharField(
        max_length=400, blank=True, null=True)
    expenses = models.CharField(
        max_length=400, blank=True, null=True)
    payroll = models.CharField(
        max_length=400, blank=True, null=True)
    savings_withdrawals = models.CharField(
        max_length=400, blank=True, null=True)
    total_payments = models.CharField(
        max_length=400, blank=True, null=True)
    total_cash_balance = models.CharField(
        max_length=400, blank=True, null=True)


class ProfitLoss(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    date = models.DateField()
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    operating_profit = models.CharField(
        max_length=400, blank=True, null=True)
    interest_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    non_deductable_fees_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    deductable_fees_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    penalty_repayments = models.CharField(
        max_length=400, blank=True, null=True)
    savings_fees = models.CharField(
        max_length=400, blank=True, null=True)
    savings_commissions = models.CharField(
        max_length=400, blank=True, null=True)
    operating_expenses = models.CharField(
        max_length=400, blank=True, null=True)
    payroll = models.CharField(
        max_length=400, blank=True, null=True)
    office_equipment = models.CharField(
        max_length=400, blank=True, null=True)
    gross_profit = models.CharField(
        max_length=400, blank=True, null=True)
    other_expenses = models.CharField(
        max_length=400, blank=True, null=True)
    savings_interest = models.CharField(
        max_length=400, blank=True, null=True)
    default_loans = models.CharField(
        max_length=400, blank=True, null=True)
    net_income = models.CharField(
        max_length=400, blank=True, null=True)


class BalanceSheet(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    date = models.DateField()
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    # ASSETS
    loans_outstanding = models.CharField(
        max_length=400, blank=True, null=True)
    current = models.CharField(
        max_length=400, blank=True, null=True)
    past_due = models.CharField(
        max_length=400, blank=True, null=True)
    restructured = models.CharField(
        max_length=400, blank=True, null=True)
    loan_loss_reserve = models.CharField(
        max_length=400, blank=True, null=True)
    net_loans_outstanding = models.CharField(
        max_length=400, blank=True, null=True)
    total_current_assets = models.CharField(
        max_length=400, blank=True, null=True)
    total_investments = models.CharField(
        max_length=400, blank=True, null=True)
    total_fixed_assets = models.CharField(
        max_length=400, blank=True, null=True)
    brand = models.CharField(
        max_length=400, blank=True, null=True)
    total_intangible_assets = models.CharField(
        max_length=400, blank=True, null=True)
    total_other_assets = models.CharField(
        max_length=400, blank=True, null=True)
    total_assets = models.CharField(
        max_length=400, blank=True, null=True)

    # LIABILITY AND EQUITY
    client_savings = models.CharField(
        max_length=400, blank=True, null=True)
    accounts_payable = models.CharField(
        max_length=400, blank=True, null=True)
    wages_payable = models.CharField(
        max_length=400, blank=True, null=True)
    short_term_borrowing = models.CharField(
        max_length=400, blank=True, null=True)
    long_term_debt_commercial = models.CharField(
        max_length=400, blank=True, null=True)
    long_term_debt_concessional = models.CharField(
        max_length=400, blank=True, null=True)
    other_accrued_expenses_payable = models.CharField(
        max_length=400, blank=True, null=True)
    income_taxes_payable = models.CharField(
        max_length=400, blank=True, null=True)
    restricted_revenue = models.CharField(
        max_length=400, blank=True, null=True)
    loan_fund_capital = models.CharField(
        max_length=400, blank=True, null=True)
    retained_net_surplus = models.CharField(
        max_length=400, blank=True, null=True)
    net_surplus = models.CharField(
        max_length=400, blank=True, null=True)
    total_equity = models.CharField(
        max_length=400, blank=True, null=True)
    total_liabilities_and_equity = models.CharField(
        max_length=400, blank=True, null=True)
