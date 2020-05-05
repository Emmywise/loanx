# from .views import SendSMS, SendEmail
from celery import shared_task
import time
import string
import datetime
import decimal

from .send_sms import SendSMSAPI
from .send_email import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from loans.models import Loan, LoanRepayment
from savings_investments.models import SavingsAccount, SavingsProduct, CashSource, SavingsTransaction, CashSafeManagement
from borrowers.models import InviteBorrower
from accounting.models import CashFlow
from commons.models import Expense
from staffs.models import Payroll
from accounts.models import Branch

@shared_task
def send_sms():
    return SendSMSAPI()
    

# @shared_task
# def send_mail(purpose, sender, recipient):
#     mail_instance = SendEmail()
#     #mail_instance.send_mail(invite new borrowers, )
#     return mail_instance()

def print_random_string():
    # time.sleep(1)
    print('random string')
    return 'radafds'


# @shared_task
# def send_sms():
#     return SendSMSAPI()

@shared_task
def send_mail_task(purpose, sender, recepient):
    return send_mail(purpose, sender, recepient)

@shared_task
def invite_borrowers():
    borrowers = InviteBorrower.objects.all()
    for borrower in borrowers:
        purpose = "register"
        sender = "admin@loanx.xyz"
        recepient = borrower.email_address
        send_mail(purpose, sender, recepient)


# @shared_task
# def apply_penalty_matured_loans():
#     filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(remaining_balance__gt = 0)
#     if (len(filtered_loans) != 0):
#         for f in filtered_loans:

#         return "code ran successfully"
#     return "code ran successfully"


@shared_task
def mark_overdue_loans():
    filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(remaining_balance__gt = 0)
    if (len(filtered_loans) != 0):
        for f in filtered_loans:
            print(f)
            send_mail('your mail is overdue', 'leke@tcore.uk', 'lexmill99@gmail.com')
            if f.maturity_date == datetime.date.today():
                f.status = "due today"
                f.save()
            else:
                f.status = "past maturity"
                f.save()
        return "code ran successfully"
    return "code ran successfully"


@shared_task
def CreditAccounts():
    savings_accounts = SavingsAccount.objects.all()
    for savings_account in savings_accounts:
        posting_frequency = savings_account.savings_product.interest_posting_frequency
        total_annual_interest = (((float(savings_account.savings_product.interest_rate_per_annum)/100))*(float(savings_account.available_balance)))
        match_selection = {"Every 1 Month":12,"Every 2 Month":6,"Every 3 Month":4,"Every 4 Month":3,"Every 6 Month":2,"Every 12 Month":1}
        
        def check_freq(freq):
            return match_selection[freq]
        print(type(savings_account.available_balance))
        print(type(savings_account.savings_product.interest_posting_frequency))
        savings_account.available_balance += decimal.Decimal(total_annual_interest/check_freq(savings_account.savings_product.interest_posting_frequency))
        savings_account.ledger_balance += decimal.Decimal(total_annual_interest/check_freq(savings_account.savings_product.interest_posting_frequency))
        savings_account.save()

        if(savings_account.savings_product.interest_posting_frequency == 'Every 1 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/12', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 2 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/6', **kwargs),
                    #'schedule': crontab(minute='07', hour='09', day_of_month='20', month_of_year='*/6', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 3 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/4', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 4 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/3', **kwargs),
                },
            }
            
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 6 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/2', **kwargs),
                },
            }

        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 12 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/1', **kwargs),
                },
            }

        return "successful"


# @shared_task
# def CacheLoanReleased():

def LogExpenses(branch):
    total = 0
    all_expenses = Expense.objects.filter(branch=branch)
    for each_expense in all_expenses:
        total += each_expense.amount
    return total

def LogPayroll(branch):
    total = 0
    all_payroll = Payroll.objects.filter(branch=branch)
    for each_payroll in all_payroll:
        total += each_payroll.net_pay
    return total

def LogLoansReleased(branch):
    total = 0
    all_loans_released = Loan.objects.filter(branch=branch).exclude(status="denied").exclude(status="processing")
    for each_loan_released in all_loans_released:
        total += each_loan_released.principal_amount
    return total

def LogLoanRepayments(branch):
    principal_amount = LogLoansReleased(branch)
    total = 0.0
    principal_repayments = 0.0
    all_loan_repayments = LoanRepayment.objects.filter(branch=branch)
    if len(all_loan_repayments) > 0:
        for each_loan_repayment in all_loan_repayments:
            total += each_loan_repayment.amount
        if total > principal_amount:
            principal_repayments = total
        else:
            principal_repayments = principal_amount
    else:
        pass
    #getting the interest
    """principal repayment is total amount of principal repaid"""
    """ total is all the money repaid"""
    """principal amount is all the money released"""
    """principal plus interest is all the principal plus interest delivered"""
    """interest repayment is 0 if all money repaid is less than or equal to principal amount, else
    it is equal to the total money repaid minus principal repayment and should be equal to principal + interest - prin
    cipal if it is greater than it"""
    all_loans_released = Loan.objects.filter(branch=branch).exclude(status="denied").exclude(status="processing")
    principal_plus_interest = 0.0
    principal_plus_interest_loan_fees = 0.0
    principal_plus_interest_loan_fees_penalty = 0.0
    for each_loan_released in all_loans_released:
        each_principal_plus_interest = each_loan_released.interest + each_loan_released.principal_amount
        principal_interest_loanfees = each_loan_released.interest + each_loan_released.principal_amount + each_loan_released.loan_fees
        principal_penalty = each_loan_released.interest + each_loan_released.principal_amount + each_loan_released.loan_fees + penalty_amount
        principal_plus_interest += each_principal_plus_interest
        principal_plus_interest_loan_fees += principal_interest_loanfees
        principal_plus_interest_loan_fees_penalty += principal_penalty

    interest_repayment = 0.0
    if total <= principal_amount:
        interest_repayment = 0.0
    elif total > principal_amount and total <= (principal_plus_interest - principal_amount):
        interest_repayment = total - principal_amount
    else:
        interest_repayment = principal_plus_interest - principal_amount
    """ loan fees """
    if total >= principal_plus_interest_loan_fees:
        loan_fee_repayment = 0.0
    elif total > principal_plus_interest and total < principal_plus_interest_loan_fees:
        loan_fee_repayment = total - principal_plus_interest
    else:
        loan_fee_repayment = principal_plus_interest_loan_fees - principal_plus_interest
    """ penalty repayment"""
    if total >= principal_plus_interest_loan_fees_penalty:
        penalty_repayment = 0.0
    elif total > principal_plus_interest_loan_fees and total < principal_plus_interest_loan_fees_penalty:
        penalty_repayment = total - principal_plus_interest_loan_fees
    else:
        penalty_repayment = principal_plus_interest_loan_fees_penalty - principal_plus_interest_loan_fees
    return {"principal_repayment":principal_repayments, "interest_repayment":interest_repayment, "loan_fee_repayment":loan_fee_repayment, "penalty_repayment":penalty_repayment}


def LogDeposits(branch):
    savings_transactions = SavingsTransaction.objects.filter(branch=branch)
    st_total = 0.0 
    st_tranfers_in = 0.0
    for savings_transaction in savings_transactions:
        if savings_transaction.transaction_type == 'Deposit' and savings_transaction.amount != None:
            st_total += savings_transaction.amount
    for savings_transaction in savings_transactions:
        if savings_transaction.transaction_type == 'Transfer In' and savings_transaction.amount != None:
            st_tranfers_in += savings_transaction.amount
    savings_products = SavingsProduct.objects.filter(branch=branch)
    sp_total = 0.0
    sp_transfer_in = 0.0
    for savings_product in savings_products:
        if savings_product.deposit != None:
            sp_total += savings_product.deposit
        elif savings_product.transfer_in != None:
            sp_transfer_in += savings_product.transfer_in
    # csm = CashSafeManagement.objects.get(branch = branch)
    # cash_sources = CashSource.objects.filter(cash_safe_management = csm)
    # if len(cash_sources) > 0:
    #     cs_total = 0
    #     for cash_source in cash_sources:
    #         if cash_source.credit != None:
    #             cs_total += cash_source.credit
    return {"deposits":st_total + sp_total, "transfers_in":  st_tranfers_in + sp_transfer_in}
    # else:
    #     return 0

def LogWithdrawals(branch):
    savings_transactions = SavingsTransaction.objects.filter(branch=branch)
    st_total = 0
    st_tranfers_out = 0.0 
    for savings_transaction in savings_transactions:
        if savings_transaction.transaction_type == 'Withdrawal' and savings_transaction.amount != None:
            st_total += savings_transaction.amount
        elif savings_transaction.transaction_type == 'Transfer Out' and savings_transaction.amount != None:
            st_tranfers_out += savings_transaction.amount
    savings_products = SavingsProduct.objects.filter(branch=branch)
    sp_total = 0
    sp_tranfers_out = 0.0 
    for savings_product in savings_products:
        if savings_product.withdrawal != None:
            sp_total += savings_product.withdrawal
        elif savings_product.transfer_out != None:
            sp_transfer_out += savings_product.transfer_out
    return {"withdrawals":st_total + sp_total, "transfers_out":  st_tranfers_out + sp_transfer_out}
    # csm = CashSafeManagement.objects.get(branch = branch)
    # cash_sources = CashSource.objects.filter(cash_safe_management = csm)
    # if len(cash_sources) > 0:
    #     cs_total = 0
    #     for cash_source in cash_sources:
    #         if cash_source.debit != None:
    #             cs_total += cash_source.debit
    #st_total + sp_total 
    #     return st_total + sp_total + cs_total
    # else:
    #     return 0


#SavingsTransaction__transaction_type
#SavingsProduct
#CashSource

@shared_task
def SaveCashFlow():
    branch = Branch.objects.all()
    for each_branch in branch:
        each_cash_flow = CashFlow()
        each_cash_flow.branch = each_branch
        if each_branch.capital != None:
            each_cash_flow.branch_capital = each_branch.capital
        else:
            each_cash_flow.branch_capital = 0
        log_loan_repayments = LogLoanRepayments(each_branch)
        log_deposits = LogDeposits(each_branch)
        log_loans_released = LogLoansReleased(each_branch)
        log_withdrawals = LogWithdrawals(each_branch)
        each_cash_flow.loan_principal_repayments = log_loan_repayments['principal_repayment']
        each_cash_flow.loan_interest_repayments = log_loan_repayments["interest_repayment"]
        each_cash_flow.loan_penalty_repayments = log_loan_repayments["penalty_repayment"]
        each_cash_flow.loan_fees_repayments = log_loan_repayments["loan_fee_repayment"]
        each_cash_flow.deductable_loan_fees = log_loan_repayments["loan_fee_repayment"]
        each_cash_flow.savings_deposits = log_loan_repayments["deposits"]
        each_cash_flow.transfer_in = log_deposits["transfers_in"]
        each_cash_flow.expenses = LogExpenses(each_branch)
        each_cash_flow.payroll = LogPayroll(each_branch)
        each_cash_flow.loan_released = LogLoansReleased(each_branch)
        each_cash_flow.savings_withdrawals = log_withdrawals["withdrawals"]
        each_cash_flow.savings_transfer_out = log_withdrawals["transfers_out"]
        #each_cash_flow.loan_repayment = LogLoanRepayments(each_branch)
        #each_cash_flow.deposit = LogDeposits(each_branch) 
        #each_cash_flow.withdrawal = LogWithdrawals(each_branch)
        #b = CashFlow(name='Beatles Blog', tagline='All the latest Beatles news.')
        each_cash_flow.save()

    return "code ran successfully"
