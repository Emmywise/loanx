from django.db import models
from accounts.models import Profile, Branch
from loans.models import Loan
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.


class Investor(models.Model):
    title_choices = (
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss.', 'Miss.'),
        ('Ms.', 'Ms.'),
        ('Dr.', 'Dr.'),
        ('Prof.', 'Prof.'),
        ('Rev.', 'Rev.'),
    )
    working_status_choices = (
        ('Employee', 'Employee'),
        ('Government Employee', 'Government Employee'),
        ('Private Sector Employee', 'Private Sector Employee'),
        ('Owner', 'Owner'),
        ('Student', 'Student'),
        ('Overseas Worker', 'Overseas Worker'),
        ('Pensioner', 'Pensioner'),
        ('Unemployed', 'Unemployed'),
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=400, blank=True, null=True)
    investor_id = models.CharField(max_length=125, default='')
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female')))
    title = models.CharField(max_length=20, choices=title_choices)
    mobile = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=400)
    state = models.CharField(max_length=400)
    working_status = models.CharField(max_length=100, choices=working_status_choices)
    photo = models.ImageField(upload_to='investor', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.investor_id


@receiver(pre_save, sender=Investor)
def update_investor_id(sender, instance, **kwargs):
    if not instance.investor_id:
        last_obj = Investor.objects.last()
        # print(last_obj.investor_id)
        if last_obj:
            if last_obj.investor_id:
                instance.investor_id = str(int(last_obj.investor_id) + 1)
        else:
            instance.investor_id = str(10000001)


class InvestorDocuments(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    file = models.FileField(upload_to='investor_documents')


class InvestorInvitation(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, 
    blank=True, null=True)
    accepted = models.BooleanField(default=False)


class LoanInvestmentProduct(models.Model):
    interest_posting_frequency_choices = (
        ('Every 1 month', 'Every 1 month'),
        ('Every 2 month', 'Every 2 month'),
        ('Every 3 month', 'Every 3 month'),
        ('Every 4 month', 'Every 4 month'),
        ('Every 6 month', 'Every 6 month'),
        ('Every 12 month', 'Every 12 month'),
    )
    interest_duration_choices = (
        ('Per Day', 'Per Day'),
        ('Per Week', 'Per Week'),
        ('Per Month', 'Per Month'),
        ('Per Year', 'Per Year'),
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,
                    blank=True, null=True)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    interest_rate_per_annum = models.DecimalField(max_digits=6, decimal_places=2)
    interest_duration = models.CharField(max_length=100, choices=interest_duration_choices)
    interest_posting_frequency = models.CharField(max_length=200, choices=interest_posting_frequency_choices)


class InvestorProduct(models.Model):
    interest_posting_frequency_choices = (
        ('Every 1 month', 'Every 1 month'),
        ('Every 2 month', 'Every 2 month'),
        ('Every 3 month', 'Every 3 month'),
        ('Every 4 month', 'Every 4 month'),
        ('Every 6 month', 'Every 6 month'),
        ('Every 12 month', 'Every 12 month'),
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    interest_rate_per_annum = models.DecimalField(max_digits=6, decimal_places=2)
    interest_posting_frequency = models.CharField(max_length=200, choices=interest_posting_frequency_choices)
    min_balance_for_interest_rate = models.DecimalField(max_digits=100, decimal_places=2)
    allow_overdraw = models.BooleanField(default=False)
    min_balance_for_withdrawal = models.DecimalField(max_digits=100, decimal_places=2)


class InvestorAccount(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    investor_product = models.ForeignKey(InvestorProduct, on_delete=models.CASCADE)
    investor_account_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)


@receiver(pre_save, sender=InvestorAccount)
def update_investor_account_id(sender, instance, **kwargs):
    if not instance.investor_account_id:
        last_obj = InvestorAccount.objects.last()
        # print(last_obj.investor_account_id)
        if last_obj:
            if last_obj.investor_account_id:
                instance.investor_account_id = str(int(last_obj.investor_account_id) + 1)
        else:
            instance.investor_account_id = str(10000001)


class LoanInvestment(models.Model):
    loan_investment_product = models.ForeignKey(LoanInvestmentProduct, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class InvestorTransaction(models.Model):
    transaction_type_choices = (
        ('Deposit', 'Deposit'),
        ('Interest', 'Interest'),
        ('Dividend', 'Dividend'),
        ('Transfer In', 'Transfer In'),
        ('Withdrawal', 'Withdrawal'),
        ('Bank Fees', 'Bank Fees'),
        ('Transfer Out', 'Transfer Out'),
        ('Commission', 'Commission'),
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    investor_account = models.ForeignKey(InvestorAccount, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    transaction_type = models.CharField(max_length=30, choices=transaction_type_choices)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.TextField(blank=True, null=True)


@receiver(pre_save, sender=InvestorTransaction)
def update_investor_account_balance(sender, instance, **kwargs):
    if instance.transaction_type in ['Deposit', 'Interest', 'Dividend', 'Transfer In']:
        instance.investor_account.balance += instance.amount
    else:
        instance.investor_account.balance -= instance.amount
    instance.investor_account.save()
