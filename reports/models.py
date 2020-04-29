from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from accounts.models import Branch
from loans.models import Borrower, Loan

# Create your models here.


class CalendarEvent(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    title = models.CharField(max_length=125)
    date = models.DateTimeField()
    till_date = models.DateTimeField(blank=True, null=True)
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

    class Meta:
        get_latest_by = ['-date']

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


class LoanBorrowerReport(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    no_loan_released = models.PositiveIntegerField(default=0)
    principal_released = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_pricipal = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_interest = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_penalty = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_principal = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_interest = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payment_penalty = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_total = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    # class Meta:
    #     order = ['-borrower__id']


class LoanReport(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    no_loan_released = models.PositiveIntegerField(default=0)
    principal_released = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_pricipal = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_interest = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_penalty = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    due_loans_total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_principal = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_interest = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payment_penalty = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    payments_total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
