from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx',
                        '.jpg', '.png', '.xlsx', '.xls']
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
    penalty_rate = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(choices=loan_type_options, max_length=100)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Loan(models.Model):
    status_choices = (
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
        ("settled", "settled"),
        ("disbursed", "disbursed"),
        ("canceled", "canceled")
    )
    disbursement_mode_types = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Wire Transfer", "Wire Transfer"),
        ("Online Transfer", "Online Transfer")
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
    #borrower = models.ForeignKey(Borrower, on_delete=models.DO_NOTHING)
    loan_type = models.ForeignKey(LoanType, on_delete=models.DO_NOTHING)
    principal_amount = models.DecimalField(max_digits=20, decimal_places=2)
    disbursement_mode = models.CharField(
        choices=disbursement_mode_types, max_length=100)
    duration = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=30, choices=status_choices, default='pending')
    request_date = models.DateField(auto_now=True)
    loan_release_date = models.DateField(blank=True, null=True)
    direct_debit = models.BooleanField(default=False)
    interest_type = models.CharField(
        choices=interest_type_types, max_length=100)
    loan_interest_percentage = models.CharField(
        max_length=400, blank=True, null=True)
    loan_interest_fixed_amount = models.CharField(
        max_length=400, blank=True, null=True)
    loan_interest_percentage_period = models.CharField(
        choices=loan_interest_percentage_period_types, max_length=400, blank=True, null=True)
    loan_duration = models.CharField(
        max_length=400, blank=True, null=True)
    loan_duration_period = models.CharField(choices=loan_duration_period_types,
                                            max_length=400, blank=True, null=True)

    number_of_repayments = models.PositiveIntegerField(default=1)
    decimal_places = models.CharField(
        choices=decimal_places_types, max_length=400, blank=True, null=True)
    interest_start_date = models.DateField(blank=True, null=True)
    first_repayment_date = models.DateField(blank=True, null=True)
    last_repayment_date = models.DateField(blank=True, null=True)
    first_repayment_on_prorata = models.BooleanField(default=False)
    adjust_remaining_repayments = models.BooleanField(default=False)
    maturity_date = models.DateField(blank=True, null=True)
    repayment_amount = models.CharField(
        max_length=400, blank=True, null=True)
    amount_paid = models.CharField(
        max_length=400, blank=True, null=True)
    remaining_balance = models.CharField(
        max_length=400, blank=True, null=True)
    interest_on_prorata = models.BooleanField(default=False)
    #ref_id = models.CharField(max_length=100, blank=True, null=True)
    # authorization_code = models.CharField(
    #     max_length=100, blank=True, null=True)
    loan_score = models.PositiveIntegerField(blank=True, null=True)
    # authorization_code = models.CharField(
    #     max_length=100, blank=True, null=True)
    # email = models.EmailField(max_length=120, blank=True, null=True)
    penalty_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    staff_permission_disbursed = models.BooleanField(default=True)
    staff_permission_accepted = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.profile.user.username


class LoanRepayment(models.Model):
    time_to_post = (
        ("12:00am-3:59am", "12:00am-3:59am"),
        ("4:00am-7:59am", "4:00am-7:59am"),
        ("8:00am-11:59pm", "8:00am-11:59pm"),
        ("12:00pm-3:59pm", "12:00pm-3:59pm"),
        ("4:00pm-7:59pm", "4:00pm-7:59pm"),
        ("8:00pm-11.59pm", "8:00pm-11.59pm"),
    )
    repayment_mode = (
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Wire Transfer", "Wire Transfer"),
        ("Online Transfer", "Online Transfer"),
        ("PayPal", "PayPal"),
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
    loan_schedule = models.OneToOneField(
        'LoanScheduler', on_delete=models.DO_NOTHING)
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
    amount = models.DecimalField(max_digits=60, decimal_places=2)
    date = models.DateField()
    payment_type = models.CharField(
        max_length=128, blank=True, null=True, choices=payment_type_choices)
    status = models.CharField(max_length=60, choices=loan_repayment_choices)
    charge_interest = models.CharField(
        max_length=60, choices=charge_interest_choices)
    repayment_cycle = models.CharField(choices=repayment_cycle_types,
                                       max_length=400, blank=True, null=True)
    repayment_mode = models.CharField(choices=repayment_mode,
                                      max_length=400, blank=True, null=True)
    proof_of_payment = models.FileField(validators=[validate_file_extension],
                                        upload_to="repayments", blank=True, null=True)


class LoanDisbursement(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.loan.profile.user.username


class LoanComment(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=128, blank=True, null=True)
    date = models.DateField(blank=True, null=True)


class LoanGroup(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)


class LoanOfficer(models.Model):
    loan = models.ManyToManyField(Loan)
    name = models.CharField(max_length=128, blank=True, null=True)
    phonenumber = models.CharField(max_length=128, blank=True, null=True)


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
    apply_loan_fee_choices = (
        ("Principal", "Principal"),
        ("Interest", "Interest"),
        ("Principal + Interest", "Principal + Interest"),
    )
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)
    staff_initiating_it = models.ForeignKey(
        LoanOfficer, on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField(default=0)
    interest_type = models.CharField(
        choices=interest_type_types, max_length=100)
    apply_loan_fee = models.CharField(
        choices=apply_loan_fee_choices, max_length=100)


class LoanAttachments(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=400)
    attachment = models.FileField(
        upload_to='attachments', blank=True, null=True)

    def __str__(self):
        return self.name


class LoanCollateral(models.Model):
    loan_type_choice = (
        ('type1', 'type1'),
        ('type2', 'type2'),
        ('type3', 'type3')
    )
    loan_type = models.CharField(
        choices=loan_type_choice, max_length=100)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=400)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    register_date = models.DateField(blank=True, null=True)

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
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=30, choices=loan_scheduler_choices)
