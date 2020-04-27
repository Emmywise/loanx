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
    total = 0
    all_loan_repayments = LoanRepayment.objects.filter(branch=branch)
    if len(all_loan_repayments) > 0:
        for each_loan_repayment in all_loan_repayments:
            total += each_loan_repayment.amount
        return total
    else:
        return 0

def LogDeposits(branch):
    savings_transactions = SavingsTransaction.objects.filter(branch=branch)
    st_total = 0 
    for savings_transaction in savings_transactions:
        if savings_transaction.transaction_type == 'Deposit' and savings_transaction.amount != None:
            st_total += savings_transaction.amount
    savings_products = SavingsProduct.objects.filter(branch=branch)
    sp_total = 0
    for savings_product in savings_products:
        if savings_product.deposit != None:
            sp_total += savings_product.deposit
    csm = CashSafeManagement.objects.get(branch = branch)
    cash_sources = CashSource.objects.filter(cash_safe_management = csm)
    if len(cash_sources) > 0:
        cs_total = 0
        for cash_source in cash_sources:
            if cash_source.credit != None:
                cs_total += cash_source.credit
        return st_total + sp_total + cs_total
    else:
        return 0

def LogWithdrawals(branch):
    savings_transactions = SavingsTransaction.objects.filter(branch=branch)
    st_total = 0 
    for savings_transaction in savings_transactions:
        if savings_transaction.transaction_type == 'Withdrawal' and savings_transaction.amount != None:
            st_total += savings_transaction.amount
    savings_products = SavingsProduct.objects.filter(branch=branch)
    sp_total = 0
    for savings_product in savings_products:
        if savings_product.withdrawal != None:
            sp_total += savings_product.withdrawal
    csm = CashSafeManagement.objects.get(branch = branch)
    cash_sources = CashSource.objects.filter(cash_safe_management = csm)
    if len(cash_sources) > 0:
        cs_total = 0
        for cash_source in cash_sources:
            if cash_source.debit != None:
                cs_total += cash_source.debit
        return st_total + sp_total + cs_total
    else:
        return 0


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
        each_cash_flow.expenses = LogExpenses(each_branch)
        each_cash_flow.payroll = LogPayroll(each_branch)
        each_cash_flow.loan_released = LogLoansReleased(each_branch)
        each_cash_flow.loan_repayment = LogLoanRepayments(each_branch)
        each_cash_flow.deposit = LogDeposits(each_branch) 
        each_cash_flow.withdrawal = LogWithdrawals(each_branch)
        #b = CashFlow(name='Beatles Blog', tagline='All the latest Beatles news.')
        each_cash_flow.save()
        print("yeah")
    return "code ran successfully"
