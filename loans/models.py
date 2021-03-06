from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import os
import decimal
import datetime
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#from borrowers.models import Borrower  
from accounts.models import Profile, Branch, Country
from cloudinary.models import CloudinaryField
from staffs.models import Staff
today = datetime.date.today()
# Create your models here.


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx',
                        '.jpg', '.png', '.xlsx', '.xls', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class LoanType(models.Model):
    loan_type_options = [
        ('Business', 'Business'),
        ('Overseas', 'Overseas'),
        ('Pensioner', 'Pensioner'),
        ('Personal', 'Personal'),
        ('Student', 'Student')
    ]
    penalty_choices = [
        ('Fully Paid Loans', 'Fully Paid Loans'),
        ('Defaulted Loans', (
            ('Credit Counseling Loans', 'Credit Counseling Loans'),
            ('Collection Agency Loans', 'Collection Agency Loans'),
            ('Sequestrate Loans', 'Sequestrate Loans'),
            ('Debt Review Loans', 'Debt Review Loans'),
            ('Fraud Loans', 'Fraud Loans'),
            ('Legal Loans', 'Legal Loans'),
            ('Write-Off Loans', 'Write-Off Loans')
        )
        ),
    ]
    penalty_rate = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(choices=loan_type_options, max_length=100)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    # apply_penalty_to = models.CharField(choices=penalty_choices, max_length=100)

    def __str__(self):
        return self.name





class Loan(models.Model):
    repayment_cycle_choices = (
        ("daily", "daily"),
        ("weekly", "weekly"),
        ("biweekly", "biweekly"),
        ("monthly", "monthly"),
        ("bi-monthly", "bi-monthly"),
        ("quarterly", "quarterly"),
        ("every 4 months", "every 4 months"),
        ("semi-annually", "semi-annually"),
        ("annually", "annually"),
        ("lump sum", "lump sum"),
    )


    status_choices = (
        ("processing", "processing"),
        ("open", (
            ("current", "current"),
            ("due today", "due today"),
            ("missed repayment", "missed repayment"),
            ("arrears", "arrears"),
            ("past maturity", "past maturity")
        )
        ),
        ("restructured", "restructured"),
        ("fully paid", "fully paid"),
        ("defaulted", (
            ("credit counselling", "credit counselling"),
            ("collection agency", "collection agency"),
            ("sequestrate", "sequestrate"),
            ("debt review", "debt review"),
            ("fraud", "fraud"),
            ("investigation", "investigation"),
            ("legal", "legal"),
            ("write-off", "write-off"),
        )
        ),
        ("denied", "denied"),
        ("not taken up", "not taken up")
    )

    interest_type_types = (
        ('Percentage Based', 'Percentage Based'),
        ('Fixed Amount Per Cycle', 'Fixed Amount Per Cycle'),
    )
    loan_interest_percentage_period_types = (
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    loan_duration_period_types = (
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    decimal_places_types = (
        ('round_off_2dp', 'round_off_2dp'),
        ('round_off_Integer', 'round_off_Integer'),
        ('round_off_1_dp', 'round_off_1_dp'),
        ('round_up_1dp', 'round_up_1dp'),
        ('round_up_10', 'round_up_10'),
        ('round_off_100', 'round_off_100'),
    )
    interest_method_types = (
        ('Flat Rate', 'Flat Rate'),
        ('Reducing Balance - Equal Installments','Reducing Balance - Equal Installments'),
        ('Reducing Balance - Equal Principal','Reducing Balance - Equal Principal'),
        ('Interest-Only', ' Interest-Only'),
        ('Compound-Interest', 'Compound Interest'),
    )
    disbursed_choices = (
        ('Online Transfer', 'Online Transfer'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Wire Transfer', 'Wire Transfer'),
    )  
    charge_in_loan_schedule_type = (
        ('dont include in the loan schedule', 'dont include in the loan schedule'),
        ('distribute fee evenly among all repayments', 'distribute fee evenly among all repayments'),
        ('charge fee based on the release date', 'charge fee based on the release date'),
        ('charge fee based on the first repayment', 'charge fee based on the first repayment'),
        ('charge fee based on the last repayment', 'charge fee based on the last repayment'),
    )
    last_paid_date = models.DateField(auto_now_add=False, blank=True, null=True)
    bank = models.CharField(verbose_name='Bank Name', max_length=100, blank=False, default='')
    amount_to_borrower = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    account_name = models.CharField(verbose_name='Account Name', max_length=100, blank=False, default='')
    charge_in_loan_schedule = models.CharField(verbose_name=('How should this be charged in Loan Schedule?'),
                            max_length=100, default='', choices=charge_in_loan_schedule_type, blank=True)
    fixed_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    loan_title = models.CharField(max_length=100, default='', blank=False) 
    account_no = models.CharField(verbose_name='Account No.', max_length=15, default='', unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.DO_NOTHING)
    loan_type = models.ForeignKey(LoanType, on_delete=models.DO_NOTHING)
    principal_amount = models.FloatField(max_length=400, blank=False, default="")
    interest_mode = models.CharField(choices=interest_type_types, max_length=400, blank=True, null=True, default='Percentage Based')
    duration = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=30, choices=status_choices, default='processing')
    request_date = models.DateField(auto_now=True)
    loan_release_date = models.DateField(blank=True, null=True) 
    direct_debit = models.BooleanField(default=False)
    interest_method = models.CharField(choices=interest_method_types, max_length=100)
    loan_interest_percentage = models.CharField(max_length=400, blank=True, null=True)
    loan_interest_fixed_amount = models.CharField(max_length=400, blank=True, null=True)
    loan_interest_percentage_period = models.CharField(choices=loan_interest_percentage_period_types, max_length=400, blank=True, null=True)
    loan_duration = models.PositiveIntegerField(default=0)
    no_of_repayments = models.PositiveIntegerField(default=1, blank=True, null=True)
    loan_duration_period = models.CharField(choices=loan_duration_period_types,max_length=400, blank=True, null=True)
    repayment_cycles = models.CharField(verbose_name='repayment Cycle', max_length=100, choices=repayment_cycle_choices, default='')
    decimal_places = models.CharField(choices=decimal_places_types, max_length=400, blank=True, null=True)
    interest_start_date = models.DateField(blank=True, null=True)
    loan_guarantor = models.ManyToManyField('LoanGuarantor', default='', related_name='loan_guarantor', blank=True)
    loan_collateral = models.ForeignKey('LoanCollateral', on_delete=models.DO_NOTHING, null=True, default='')
    maturity_date = models.DateField(blank=True, null=True)
    repayment_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    interest_on_prorata = models.BooleanField(default=False)
    released = models.BooleanField(default=False)
    maturity = models.BooleanField(default=False)
    email = models.EmailField(max_length=120, blank=True, null=True)
    authorization_code = models.CharField(max_length=120, blank=True, null=True)
    penalty_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    staff_permission_disbursed = models.BooleanField(default=True)
    staff_permission_accepted = models.BooleanField(default=False)
    disbursed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    bvn = models.CharField(max_length=20, blank=True, null=True)
    total_due_principal = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    total_due_interest = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    total_due_loan_fee = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    total_due_penalty = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    interest = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    #loan_fees = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    current_repayment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    loan_fees = models.ManyToManyField('LoanFee', default=None)
    penalty_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    loan_score = models.IntegerField(default=0, blank=True, null=True)
    disbursed_by = models.CharField(max_length=50, choices=disbursed_choices, blank=False, default='Online Transfer')
    loan_description = models.TextField(default='', blank=True)
    account_number = models.CharField(verbose_name='Account Number', max_length=20, blank=False, default='')
    staff_permission_approved = models.BooleanField(default=False)
    staff_permission_disbursed = models.BooleanField(default=False)
    staff_permission_accepted = models.BooleanField(default=False)
    approval_level = models.IntegerField(default=0)
    first_approval = models.ForeignKey(to='staffs.Staff', on_delete=models.SET_NULL, null=True, related_name='first_approval')
    second_approval = models.ForeignKey(to='staffs.Staff', on_delete=models.SET_NULL, null=True, related_name='second_approval')
    third_approval = models.ForeignKey(to='staffs.Staff', on_delete=models.SET_NULL, null=True, related_name='third_approval')
    amount_paid =  models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.account_no + ' - ' + str(self.borrower.first_name) + '  ' + str(self.borrower.last_name)

    def get_balance(self):
        return self.repayment_amount - self.amount_paid

    def released(self):
        return self.status == "current"

    def maturity(self):
        return self.maturity_date <= datetime.date.today()

@receiver(pre_save, sender=Loan)
def update_interest_rate(sender, instance, **kwargs):
    if instance.interest_mode == 'Percentage Based':
        if instance.loan_interest_percentage == 'null' and instance.interest_rate == 'null':
    # if instance.interest_rate == None:
            instance.interest_rate = instance.loan_type.interest_rate
            instance.loan_interest_percentage = instance.loan_type.interest_rate
        elif instance.loan_interest_percentage != 'null':
            instance.interest_rate = instance.loan_interest_percentage
        elif instance.interest_rate != 'null':
            instance.loan_interest_percentage = instance.loan_type.interest_rate
    elif instance.interest_mode == 'Fixed Amount Per Cycle':
        instance.fixed_amount = instance.loan_interest_fixed_amount
    if instance.penalty_rate == None:
        instance.penalty_rate = instance.loan_type.penalty_rate

@receiver(pre_save, sender=Loan)
def update_penalty_rate(sender, instance, **kwargs):
    if instance.penalty_rate == 'null':
        instance.penalty_rate = instance.loan_type.penalty_rate

@receiver(pre_save, sender=Loan)
def update_account_no(sender, instance, **kwargs):
    if instance.branch.loan_generate_string:
        gen_string = instance.branch.loan_generate_string
    if not instance.account_no:
        last_obj = Loan.objects.last()
        if last_obj:
            if last_obj.account_no:
                numb = last_obj.account_no.split("-", 1)[-1]
                last_obj.account_no = int(numb)
                new_string = str(int(last_obj.account_no) + 1)
                instance.account_no = gen_string + '' + new_string
        else:
            instance.account_no = gen_string + '' + str(10000001)

@receiver(pre_save, sender=Loan)
def update_balance(sender, instance, **kwargs):
    if instance.remaining_balance <= 0.00:
        instance.remaining_balance = 0.00
    elif instance.remaining_balance > 0:
        instance.remaining_balance = decimal.Decimal(instance.repayment_amount) - decimal.Decimal(instance.amount_paid)
    else:
        pass
    instance.loan_score = instance.borrower.loan_score

@receiver(pre_save, sender=Loan)
def update_status(sender, instance, **kwargs):
    if instance.amount_paid >= 0.00 and instance.status != 'fully paid' and instance.disbursed == True and instance.maturity_date < today:
        instance.status = "past maturity"
    elif instance.amount_paid >= 0.00 and instance.status != "fully paid" and instance.disbursed == True and instance.maturity_date < today:
        instance.status = "missed repayment"
    elif instance.amount_paid >= 0.00 and instance.status != "fully paid" and instance.disbursed == True and instance.maturity_date == today:
        instance.status = "due today"
    elif instance.amount_paid == 0.00 and instance.status != "fully paid" and instance.disbursed == True and instance.maturity_date < today:
        instance.status = 'arrears'
    elif instance.amount_paid > 0.00 and instance.remaining_balance != instance.repayment_amount and instance.remaining_balance == 0 and instance.disbursed == True:
        instance.status = 'fully paid'
    elif instance.amount_paid >= 0.00 and instance.status != 'fully paid' and instance.disbursed == True and instance.maturity_date > today:
        instance.status = 'current'

#@receiver(pre_save, sender=Loan)
#def update_interest_rate(sender, instance, **kwargs):
#    if instance.interest_rate == None:
#        instance.interest_rate = instance.loan_type.interest_rate
#    if instance.penalty_rate == None:
#        instance.penalty_rate = instance.loan_type.penalty_rate

#@receiver(pre_save, sender=Loan)
#def update_balance(sender, instance, **kwargs):
#    instance.remaining_balance = decimal.Decimal(instance.repayment_amount) - decimal.Decimal(instance.amount_paid)
#    if instance.remaining_balance == 0:
#        instance.status = "fully paid"
#    instance.loan_score = instance.borrower.loan_score

  


class LoanOfficer(models.Model):
    #loan = models.ManyToManyField(Loan, blank=True, null=True)
    #members = models.ManyToManyField(Loan, through="LoanMembership")
    #name = models.CharField(max_length=128, blank=True, null=True)
    #phonenumber = models.CharField(max_length=128, blank=True, null=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.staff_id.user_id.user.first_name + ' ' + str(self.staff_id.user_id.user.last_name)

#    user_id = models.OneToOneField(Profile, on_delete=models.SET_NULL, default='', null=True)

#    def __str__(self):
#        return self.user_id.user.first_name + ' ' + str(self.user_id.user.last_name) + ' - ' + str(self.user_id.branch)




class LoanMembership(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    loan_officer = models.ForeignKey(LoanOfficer, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.loan.borrower.first_name + " " + "in" + " "+ self.loan_officer.name


class LoanApproval(models.Model):
    staff = models.ForeignKey(to='staffs.Staff', on_delete=models.SET_NULL, null=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, default=None)
    decision = models.CharField(max_length=100, default='', blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.loan.account_no



class LoanRepayment(models.Model):
    time_to_post = (
        ("12:00am-3:59am", "12:00am-3:59am"),
        ("4:00am-7:59am", "4:00am-7:59am"),
        ("8:00am-11:59pm", "8:00am-11:59pm"),
        ("12:00pm-3:59pm", "12:00pm-3:59pm"),
        ("4:00pm-7:59pm", "4:00pm-7:59pm"),
        ("8:00pm-11.59pm", "8:00pm-11.59pm"),
    )

    loan_repayment_choices = (
        ("accepted", "accepted"),
        ("pending", "pending"),
        ("declined", "declined"),
    )
    charge_interest_choices = (
        ("normally", "normally"),
        ("charge_on_release_date", "charge_on_release_date"),
        ("charge_on_first_repayment", "charge_on_first_repayment"),
        ("charge_on_last_repayment", "charge_on_last_repayment"),
        ("do_not_charge_on_last_repayment", "do_not_charge_on_last_repayment"),
    )
    payment_type_choices = (
        ("manual", "manual"),
        ("card", "card"),
    )
    repayment_cycle_types = (
        ("daily", "daily"),
        ("weekly", "weekly"),
        ("biweekly", "biweekly"),
        ("monthly", "monthly"),
        ("bi-monthly", "bi-monthly"),
        ("quarterly", "quarterly"),
        ("every 4 months", "every 4 months"),
        ("semi-annually", "semi-annually"),
        ("annually", "annually"),
        ("lump sum", "lump sum"),
    )
    repayment_mode_choices = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Wire Transfer", "Wire Transfer"),
        ("Online Transfer", "Online Transfer"),
        ("PayPal", "PayPal"),
    )
    loan = models.ForeignKey(
        'Loan', on_delete=models.DO_NOTHING)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    repayment_mode = models.CharField(choices=repayment_mode_choices,
                            max_length=400, blank=True, null=True)
    amount = models.DecimalField(max_digits=60, decimal_places=2)
    interest_paid = models.DecimalField(max_digits=60, decimal_places=2, blank=True, null=True)
    interest = interest = models.DecimalField(max_digits=60, decimal_places=2, blank=True, null=True)
    duration = models.CharField(max_length=222, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    amount_taken = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateField()
    payment_type = models.CharField(
        max_length=128, blank=True, null=True, choices=payment_type_choices)
    status = models.CharField(max_length=60, choices=loan_repayment_choices, blank=True, null=True)
    charge_interest = models.CharField(
        max_length=60, choices=charge_interest_choices, blank=True, null=True)
    repayment_cycle = models.CharField(choices=repayment_cycle_types,
                                       max_length=400, blank=True, null=True)
    proof_of_payment = models.FileField(validators=[validate_file_extension],
                                        upload_to="repayments", blank=True, null=True)

    collector = models.ForeignKey(LoanOfficer, on_delete=models.DO_NOTHING, blank=True, null=True)
    number_of_repayments = models.PositiveIntegerField(default=0, blank=True, null=True)
    grace_period = models.PositiveIntegerField(default=0, blank=True, null=True)
    grace_period_once_per_loan = models.BooleanField(default=False, blank=True, null=True)
    penalty_branch_holiday = models.BooleanField(default=True, blank=True, null=True)
    first_repayment_date = models.DateField(blank=True, null=True)
    last_repayment_date = models.DateField(blank=True, null=True)
    first_repayment_on_prorata = models.BooleanField(default=False, blank=True, null=True)
    adjust_remaining_repayments = models.BooleanField(default=False, blank=True, null=True)
    amortization = models.CharField(max_length=400, blank=True, null=True)
    days_passed = models.PositiveIntegerField(default=0, blank=True, null=True)
    pending_due = models.CharField(max_length=400, blank=True, null=True)
    comment = models.CharField(max_length=400, blank=True, null=True)
    outstanding_principal = models.CharField(max_length=400, blank=True, null=True)
    amount_paid = models.CharField(max_length=400, blank=True, null=True)
    left_to_be_paid = models.CharField(max_length=400, blank=True, null=True)
    leftToBePaidTotal = models.CharField(max_length=400, blank=True, null=True)
    next_due_date = models.DateField(auto_now_add=False, null=True)
    past_due_date = models.DateField(auto_now_add=False, null=True)
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return str(self.loan.id) + "-" + str(self.date) + "-" + self.loan.borrower.first_name + " " + self.loan.borrower.last_name

@receiver(pre_save, sender=LoanRepayment)
def update_borrower(sender, instance, **kwargs):
    instance.borrower = instance.loan.borrower   

class LoanDisbursement(models.Model):
    status_types = (
        ("Current", "Current"),
        ("Arrears", "Arrears"),       
    )
    disbursement_mode_types = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Wire Transfer", "Wire Transfer"),
        ("Online Transfer", "Online Transfer")
    )
    loan_interest_percentage_period_types = (
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    loan_duration_period_types = (
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    loan = models.OneToOneField(Loan, on_delete=models.DO_NOTHING)
    disbursement_mode = models.CharField(
        choices=disbursement_mode_types, max_length=100)
    status = models.CharField(
        choices=status_types, max_length=100)
    disbursed_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    outstanding = models.CharField(max_length=400, blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    loan_interest_percentage = models.CharField(
        max_length=400, blank=True, null=True)
    loan_interest_fixed_amount = models.CharField(
        max_length=400, blank=True, null=True)
    loan_interest_percentage_period = models.CharField(
        choices=loan_interest_percentage_period_types, max_length=400, blank=True, null=True)
    loan_duration_period = models.CharField(choices=loan_duration_period_types,
                                            max_length=400, blank=True, null=True)
    loan_officer = models.ForeignKey(LoanOfficer, on_delete=models.DO_NOTHING)
    date_disbursed = models.DateField(auto_now_add=True, null=True, blank=True)

@receiver(pre_save, sender=LoanDisbursement)
def update_balance(sender, instance, **kwargs):
    instance.loan.disbursed = True



class LoanComment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=128, blank=True, null=True)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(LoanOfficer, on_delete=models.DO_NOTHING)


class LoanGroup(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)


class LoanRemainder(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    days_before_due = models.PositiveIntegerField(default=1)
    frequency = models.PositiveIntegerField(default=1)
    staff_to_receive_remainder = models.ForeignKey(
        LoanOfficer, on_delete=models.DO_NOTHING)


class LoanRestructure:
    loan_restructure_choices = (
        ("outstanding_principal_amount", "outstanding_principal_amount"),
        ("outstanding_principal_interest", "outstanding_principal_interest"),
        ("outstanding_principal_interest fees",
         "outstanding_principal_interest fees"),
        ("outstanding_total_amount", "outstanding_total_amount"),
    )
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    staff_handling_restructuring = models.ForeignKey(
        LoanOfficer, on_delete=models.DO_NOTHING)


class LoanFee(models.Model):
    interest_type_types = (
        ("Percentage Based", "Percentage Based"),
        ("Fixed Amount Per Cycle", "Fixed Amount Per Cycle"),
    )
    #apply_loan_fee_choices = (
     #   ("Principal", "Principal"),
      #  ("Interest", "Interest"),
       # ("Principal + Interest", "Principal + Interest"),
    #)
    #loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)
    #staff_initiating_it = models.ForeignKey(
     #   LoanOfficer, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    interest_type = models.CharField(
        choices=interest_type_types, max_length=100)
    #apply_loan_fee = models.CharField(
    #    choices=apply_loan_fee_choices, max_length=100)
    percentage = models.DecimalField(decimal_places=2, max_digits=20, default=0)

    def __str__(self):
        return self.name

class LoanAttachment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=400)
    attachment = models.FileField(
        upload_to='attachments', blank=True, null=True)

    def __str__(self):
        return self.name


class LoanCollateral(models.Model):
    loan_type_choices = (
        ('Automobiles', 'Automobiles'),
        ('Electronic Items', 'Electronic Items'),
        ('Insurance Policies', 'Insurance Policies'),
        ('Investments', 'Investments'),
        ('Machineries and Equipments', 'Machineries and Equipments'),
        ('Real Estate', 'Real Estate'),
        ('Valuables and Collectibles', 'Valuables and Collectibles'),
        ('Others', 'Others')
    )
    current_status = (
        ('Deposited into branch', 'Deposited into branch'),
        ('Collateral with borrower', 'Collateral with borrower'),
        ('Returned to borrower', 'Returned to borrower'),
        ('Repossession initiated', 'Repossession initiated'),
        ('under auction', 'under auction'),
        ('sold', 'sold'),
        ('lost', 'lost'),)

    condition_choices = (
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Damaged', 'Damaged'),)
    collateral_type = models.CharField(
        choices=loan_type_choices, max_length=100)
    collateral_type_choice = (
        ('Automobiles', 'Automobiles'),
        ('Electronic Items', 'Electronic Items'),
        ('Insurance Policies', 'Insurance Policies'),
        ('Investments', 'Investments'),
        ('Machineries and Equipments', 'Machineries and Equipments'),
        ('Real Estate', 'Real Estate'),
        ('Valuables and Collectibles', 'Valuables and Collectibles'),
        ('Others', 'Others')
    )
    collateral_type = models.CharField(
        choices=collateral_type_choice, max_length=100)
    #loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=400)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    register_date = models.DateField(blank=True, null=True)
    current_status = models.CharField(
        choices=current_status, max_length=100)
    item_state = models.CharField(
        choices=condition_choices, max_length=100)
    last_updated_date = models.DateField(auto_now=True)
    serial_number = models.CharField(max_length=128, blank=True, null=True)
    model_name = models.CharField(max_length=128, blank=True, null=True)
    model_number = models.CharField(max_length=128, blank=True, null=True)
    colour = models.CharField(max_length=128, blank=True, null=True)
    date_of_manufacturer = models.CharField(
        max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    reg_no = models.CharField(max_length=128, blank=True, null=True)
    mileage = models.CharField(max_length=128, blank=True, null=True)
    engine_no = models.CharField(max_length=128, blank=True, null=True)
    collateral_photo = models.FileField(validators=[validate_file_extension],
                                        upload_to="repayments", blank=True, null=True)
    collateral_files = models.FileField(validators=[validate_file_extension],
                                        upload_to="repayments", blank=True, null=True)

    def __str__(self):
        return self.name


class LoanScheduler(models.Model):
    loan_scheduler_choices = (
        ('pending', 'pending'),
        ('settled', 'settled'),
        ('overdue', 'overdue')
    )
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField()
    principal =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    interest =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    fees =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    penalty =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    due =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    paid =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    pending_due =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    total_due =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    principal_due =  models.DecimalField(max_digits=100, decimal_places=2, default = 0)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=30, choices=loan_scheduler_choices)
    principal_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    def __str__(self):
        return self.loan.account_no


class LoanGuarantor(models.Model):
    title_choices = (
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss', 'Miss'),
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
#    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=400, blank=True, null=True)
    gender = models.CharField(max_length=200,
                              choices=(('Male', 'Male'), ('Female', 'Female')))
    title = models.CharField(max_length=5, choices=title_choices)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=400)
    state = models.CharField(max_length=400)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    landline_phone = models.CharField(max_length=20, blank=True, null=True)
    working_status = models.CharField(max_length=100, choices=working_status_choices)
    photo = CloudinaryField('image', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)


class GuarantorFile(models.Model):
    guarantor = models.ForeignKey(LoanGuarantor, on_delete=models.CASCADE)
    file = models.FileField(upload_to='guarantor_files')

class OfficerLoan(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, default=None)
    loan_officer = models.ForeignKey(LoanOfficer, on_delete=models.CASCADE, default=None)
    assigned_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.loan.account_no + ' to ' + str(self.loan_officer.staff_id.user_id.user.first_name) \
        + ' ' + str(self.loan_officer.staff_id.user_id.user.last_name)
