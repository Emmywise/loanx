from django.db import models
from accounts.models import Branch

class CashFlow(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, related_name="cash_flow_branch")
    branch_capital = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)

    #receipts
    loan_principal_repayments = models.DecimalField(max_digits=10, decimal_places=2)
    loan_interest_repayments = models.DecimalField(max_digits=10, decimal_places=2)
    loan_penalty_repayments = models.DecimalField(max_digits=10, decimal_places=2)
    loan_fees_repayments = models.DecimalField(max_digits=10, decimal_places=2)
    deductable_loan_fees = models.DecimalField(max_digits=10, decimal_places=2)
    savings_deposits = models.DecimalField(max_digits=10, decimal_places=2)
    savings_fees = models.DecimalField(max_digits=10, decimal_places=2)
    savings_commissions = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    savings_transfer_in = models.DecimalField(max_digits=10, decimal_places=2)
    investor_account_deposits = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    investor_account_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    investor_account_commissions = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    investor_account_transfer_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    other_income = models.DecimalField(max_digits=10, decimal_places=2, default = 0.0)

    #payments
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    payroll = models.DecimalField(max_digits=10, decimal_places=2)
    loan_released = models.DecimalField(max_digits=10, decimal_places=2)
    #loan_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    #deposit = models.DecimalField(max_digits=10, decimal_places=2)
    #withdrawal = models.DecimalField(max_digits=10, decimal_places=2)
    savings_withdrawals = models.DecimalField(max_digits=10, decimal_places=2)
    savings_transfer_out = models.DecimalField(max_digits=10, decimal_places=2)
    investor_account_withdrawals = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    investor_account_transfer_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)



class ProfitLoss(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, related_name="profit_loss_branch")
    branch_capital = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    interest_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    non_deductable_fees_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    deductable_fees_repayment= models.DecimalField(max_digits=10, decimal_places=2)
    penalty_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    savings_fees = models.DecimalField(max_digits=10, decimal_places=2)
    savings_commissions = models.DecimalField(max_digits=10, decimal_places=2)
    investor_account_fees = models.DecimalField(max_digits=10, decimal_places=2)
    investor_account_commissions = models.DecimalField(max_digits=10, decimal_places=2)
    payroll = models.DecimalField(max_digits=10, decimal_places=2)
    savings_interest = models.DecimalField(max_digits=10, decimal_places=2)
    investor_acct_interest = models.DecimalField(max_digits=10, decimal_places=2)
    default_loans = models.DecimalField(max_digits=10, decimal_places=2)


class BalanceSheet(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, related_name="balance_sheet_branch")
    branch_capital = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    #loan_outstanding
    current = models.DecimalField(max_digits=10, decimal_places=2)
    past_due = models.DecimalField(max_digits=10, decimal_places=2)
    restructured = models.DecimalField(max_digits=10, decimal_places=2)
    loan_loss_reserve = models.DecimalField(max_digits=10, decimal_places=2)
    total_investments = models.DecimalField(max_digits=10, decimal_places=2)
    total_fixed_assets = models.DecimalField(max_digits=10, decimal_places=2)
    total_intangible_assets = models.DecimalField(max_digits=10, decimal_places=2)
    total_other_assets = models.DecimalField(max_digits=10, decimal_places=2)
    client_savings = models.DecimalField(max_digits=10, decimal_places=2)
    account_payable = models.DecimalField(max_digits=10, decimal_places=2)
    wages_payable = models.DecimalField(max_digits=10, decimal_places=2)
    short_term_borrowing = models.DecimalField(max_digits=10, decimal_places=2)
    long_term_debt_commercial_rate = models.DecimalField(max_digits=10, decimal_places=2)
    long_term_debt_concessional_rate = models.DecimalField(max_digits=10, decimal_places=2)
    other_accrued_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    income_taxes_payable = models.DecimalField(max_digits=10, decimal_places=2)
    restricted_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    loan_fund_capital = models.DecimalField(max_digits=10, decimal_places=2)
    retained_net_surplus = models.DecimalField(max_digits=10, decimal_places=2)
    net_surplus = models.DecimalField(max_digits=10, decimal_places=2)