from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from accounts.models import Profile, Branch
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.validators import ValidationError

# Create your models here.


data_type_choices = (
    ('text_field', 'text_field'),
    ('date_field', 'date_field'),
    ('integer_field', 'integer_field'),
    ('decimal_field', 'decimal_field'),
    ('url_field', 'url_field'),
    ('text_area', 'text_area'),
    ('dropdown', 'dropdown'),
    ('file_upload', 'file_upload'),
)


class SavingsProduct(models.Model):
    interest_method_choices = (
        ('Last Savings Balance', 'Last Savings Balance'),
        ('Pro-Rata Basis', 'Pro-Rata Basis')
    )
    posting_frequency_choices = (
        ('Every 1 Month', 'Every 1 Month'),
        ('Every 2 Month', 'Every 2 Month'),
        ('Every 3 Month', 'Every 3 Month'),
        ('Every 4 Month', 'Every 4 Month'),
        ('Every 6 Month', 'Every 6 Month'),
        ('Every 12 Month', 'Every 12 Month'),
    )
    name = models.CharField(max_length=125)
    interest_rate_per_annum = models.DecimalField(max_digits=10, decimal_places=2)
    interest_method = models.CharField(max_length=100, choices=interest_method_choices)
    interest_posting_frequency = models.CharField(max_length=300, choices=posting_frequency_choices)
    min_balance_for_interest = models.DecimalField(max_digits=100, decimal_places=2)
    overdrawn = models.BooleanField(default=False)
    min_balance_for_withdrawal = models.DecimalField(max_digits=100, decimal_places=2)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)

    # reports fields
    deposit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    transfer_in = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    withdrawal = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    dividend = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    transfer_out = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=SavingsProduct)
def update_savings_product_balance(sender, instance, **kwargs):
    instance.balance = instance.deposit + instance.transfer_in - instance.withdrawal \
                       - instance.fees + instance.interest + instance.dividend - instance.transfer_out \
                       + instance.commission


class SavingsAccount(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    savings_product = models.ForeignKey(SavingsProduct, on_delete=models.CASCADE)
    savings_id = models.CharField(max_length=125, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    available_balance = models.DecimalField(max_digits=100, decimal_places=2)
    ledger_balance = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.savings_id or ''


@receiver(pre_save, sender=SavingsAccount)
def update_savings_id(sender, instance, **kwargs):
    # ledger balance
    instance.available_balance = instance.ledger_balance - \
                                 instance.savings_product.min_balance_for_withdrawal
    if not instance.savings_id:
        last_obj = SavingsAccount.objects.last()
        # print(last_obj.savings_id)
        if last_obj:
            if last_obj.savings_id:
                instance.savings_id = str(int(last_obj.savings_id) + 1)
        else:
            instance.savings_id = str(10000001)


class CustomSavingsAccountField(models.Model):
    savings_account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE)
    field = models.CharField(max_length=125)
    text_field = models.TextField(blank=True, null=True)
    date_field = models.DateField(blank=True, null=True)
    integer_field = models.PositiveIntegerField(blank=True, null=True)
    decimal_field = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    url_field = models.URLField(max_length=500, blank=True, null=True)
    text_area = models.TextField(blank=True, null=True)
    dropdown_values = models.TextField(blank=True, null=True, validators=[validate_comma_separated_integer_list])
    dropdown = models.CharField(max_length=200, blank=True, null=True)
    file_upload = models.FileField(upload_to='savings_accounts', blank=True, null=True)


class CashSafeManagement(models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    def __str__(self):
        return self.branch.name

@receiver(post_save, sender=Branch)
def create_cash_safe_management(sender, instance, created, **kwargs):
    try:
        instance.cashsafemanagement
    except:
        CashSafeManagement.objects.create(branch=instance)


class CashSource(models.Model):
    cash_safe_management = models.ForeignKey(CashSafeManagement, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, unique=True)
    debit = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=CashSource)
def sum_cash_source_balance(sender, instance, **kwargs):
    instance.balance = (instance.credit or 0) - (instance.debit or 0)


class Teller(models.Model):
    cash_safe_management = models.ForeignKey(CashSafeManagement, on_delete=models.CASCADE)
    staff = models.OneToOneField(Profile, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    debit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    # reports fields
    report_deposit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_transfer_in = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_withdrawal = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_interest = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_dividend = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_transfer_out = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_commission = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    report_balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.staff.user.username


@receiver(pre_save, sender=Teller)
def sum_teller_balance(sender, instance, **kwargs):
    instance.total_balance = (instance.credit or 0) - (instance.debit or 0)
    instance.report_balance = instance.report_deposit + instance.report_transfer_in - instance.report_withdrawal - \
                              instance.report_fees + instance.report_interest + instance.report_dividends + \
                              instance.report_commision - instance.report_transfer_out


class TransferCash(models.Model):
    cash_safe_management = models.ForeignKey(CashSafeManagement, on_delete=models.CASCADE)
    from_cash_source = models.ForeignKey(CashSource, on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='from_cash_source')
    to_cash_source = models.ForeignKey(CashSource, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='to_cash_source')
    from_teller = models.ForeignKey(Teller, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='from_teller')
    to_teller = models.ForeignKey(Teller, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='to_teller')
    amount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)

    # post save to update the respective cash source and teller amount


@receiver(post_save, sender=TransferCash)
def update_cash_source_and_teller_balance(sender, instance, created, **kwargs):
    if instance.from_cash_source:
        instance.from_cash_source.debit += instance.amount
        instance.from_cash_source.save()
    if instance.to_cash_source:
        instance.to_cash_source.credit += instance.amount
        instance.to_cash_source.save()
    if instance.from_teller:
        instance.from_teller.debit += instance.amount
        instance.from_teller.save()
    if instance.to_teller:
        instance.to_teller.credit += instance.amount
        instance.to_teller.save()


class SavingsTransaction(models.Model):
    savings_transaction_choices = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Bank Fee', 'Bank Fee'),
        ('Interest', 'Interest'),
        ('Dividend', 'Dividend'),
        ('Transfer In', 'Transfer In'),
        ('Transfer Out', 'Transfer Out'),
        ('Commission', 'Commission'),
    )

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    teller = models.ForeignKey(Teller, on_delete=models.CASCADE, blank=True, null=True)
    savings_account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    transaction_type = models.CharField(max_length=100, choices=savings_transaction_choices)
    date_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    account_to_account_transfer = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_type


@receiver(post_save, sender=SavingsTransaction)
def update_teller_and_account_balance(sender, instance, created, **kwargs):
    if instance.approved:
        if instance.transaction_type in ['Deposit', 'Interest', 'Dividend', 'Transfer In']:
            if not instance.account_to_account_transfer:
                instance.teller.credit += instance.amount
                # instance.teller.save()
            instance.savings_account.ledger_balance += instance.amount
            instance.savings_account.save()
        if instance.transaction_type in ['Withdrawal', 'Bank Fee', 'Transfer Out', 'Commission']:
            if not instance.account_to_account_transfer:
                instance.teller.debit += instance.amount
                # instance.teller.save()
            instance.savings_account.ledger_balance -= instance.amount
            instance.savings_account.save()
        if instance.transaction_type == 'Deposit':
            instance.savings_account.savings_product.deposit += instance.amount
            instance.teller.report_deposit += instance.amount
        if instance.transaction_type == 'Interest':
            instance.savings_account.savings_product.interest += instance.amount
            instance.teller.report_interest += instance.amount
        if instance.transaction_type == 'Commission':
            instance.savings_account.savings_product.commission -= instance.amount
            instance.teller.report_commission -= instance.amount
        if instance.transaction_type == 'Dividend':
            instance.savings_account.savings_product.dividend += instance.amount
            instance.teller.report_dividend += instance.amount
        if instance.transaction_type == 'Transfer In':
            instance.savings_account.savings_product.transfer_in += instance.amount
            if not instance.account_to_account_transfer:
                instance.teller.report_transfer_in += instance.amount
        if instance.transaction_type == 'Withdrawal':
            instance.savings_account.savings_product.witdrawal += instance.amount
            instance.teller.report_withdrawal += instance.amount
        if instance.transaction_type == 'Bank Fee':
            instance.savings_account.savings_product.fees += instance.amount
            instance.teller.report_fees += instance.amount
        if instance.transaction_type == 'Transfer Out':
            instance.savings_account.savings_product.transfer_out += instance.amount
            if not instance.account_to_account_transfer:
                instance.teller.report_transfer_out += instance.amount

        instance.savings_account.savings_product.save()
        if instance.teller:
            instance.teller.save()


class FundTransferLog(models.Model):
    teller = models.ForeignKey(Teller, on_delete=models.DO_NOTHING, blank=True, null=True)
    from_account = models.ForeignKey(SavingsAccount, on_delete=models.DO_NOTHING, related_name='from_account')
    to_account = models.ForeignKey(SavingsAccount, on_delete=models.DO_NOTHING, related_name='to_account')
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date_time = models.DateTimeField()


@receiver(post_save, sender=FundTransferLog)
def update_transaction_table(sender, instance, created, **kwargs):
    SavingsTransaction.objects.create(
        branch=instance.from_account.branch,
        teller=instance.teller,
        savings_account=instance.from_account,
        amount=instance.amount,
        transaction_type='Transfer Out',
        date_time=instance.date_time,   
        approved=True,
        account_to_account_transfer=True
    )
    SavingsTransaction.objects.create(
        branch=instance.to_account.branch,
        teller=instance.teller,
        savings_account=instance.to_account,
        amount=instance.amount,
        transaction_type='Transfer In',
        date_time=instance.date_time,
        approved=True,
        account_to_account_transfer=True
    )
