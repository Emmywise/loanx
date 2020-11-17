from rest_framework import serializers
from .models import Loan, LoanComment, LoanOfficer, LoanFee, LoanCollateral, LoanAttachment, LoanType
from .models import (
    Loan, LoanComment, LoanRepayment,
    LoanCollateral, LoanGuarantor,
    GuarantorFile, LoanDisbursement, LoanScheduler, LoanMembership
)
from .serializers import *
from staffs.models import Staff
from .models import (Loan, LoanComment, LoanOfficer, LoanFee,
LoanCollateral, LoanAttachment, LoanRepayment, GuarantorFile, LoanGuarantor, LoanDisbursement)




class LoanSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = '__all__'


class ApproveLoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
#        fields = '__all__'
        fields = (['amount_paid'])
        model = Loan


class LoanFeeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanFee


class LoanGuarantorSerializer(serializers.ModelSerializer):
    guarantor_files = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = LoanGuarantor

    def get_guarantor_files(self, obj):
        guarantor_files = []
        for file in obj.guarantorfile_set.all():
            guarantor_files.append(GuarantorFileSerializer(file).data)
        return guarantor_files

class LoanSerializer(serializers.ModelSerializer):
    # remaining_balance = serializers.ReadOnlyField(source="self.get_balance")
    # released = serializers.ReadOnlyField(source="self.released")
    # maturity = serializers.ReadOnlyField(source="self.maturity")
    borrower = serializers.SerializerMethodField()
    borrower_mobile = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    loan_type = serializers.SerializerMethodField()
    loan_collateral = serializers.SerializerMethodField()
    loan_guarantor = LoanGuarantorSerializer(many=True)
    loan_fees = LoanFeeSerializer(many=True)
    request_date = serializers.SerializerMethodField()
    loan_release_date = serializers.SerializerMethodField()
    interest_start_date = serializers.SerializerMethodField()
    maturity_date = serializers.SerializerMethodField()
    first_approval_name = serializers.SerializerMethodField()
    second_approval_name = serializers.SerializerMethodField()
    third_approval_name = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = Loan

    def get_borrower(self, obj):
        if obj.borrower:
            borrower = obj.borrower.first_name + ' ' + str(obj.borrower.last_name)
            return borrower

    def get_borrower_mobile(self, obj):
        if obj.borrower:
            borrower = obj.borrower.mobile
            return borrower

    def get_first_approval_name(self, obj):
        if obj.first_approval:
            name = obj.first_approval.user_id.user.first_name + ' ' + obj.first_approval.user_id.user.last_name
            return name

    def get_second_approval_name(self, obj):
        if obj.second_approval:
            name = obj.second_approval.user_id.user.first_name + ' ' + obj.second_approval.user_id.user.last_name
            return name

    def get_third_approval_name(self, obj):
        if obj.third_approval:
            name = obj.third_approval.user_id.user.first_name + ' ' + obj.third_approval.user_id.user.last_name
            return name

    def get_branch(self, obj):
        if obj.branch:
            branch = obj.branch.name
            return branch

    def get_loan_type(self, obj):
        loan_type = obj.loan_type.name
        return loan_type

    def get_loan_collateral(self, obj):
        if obj.loan_collateral:
            loan_collateral = obj.loan_collateral.name
            return loan_collateral

    def get_loan_guarantor(self, obj):
        names = []
        for name in obj.loanguarantor_set.all():
            names.append(LoanGuarantorSerializer(name).data)
        return names

    def get_loan_fees(self, obj):
        names = []
        for name in obj.loan_fees_set.all():
            names.append(LoanFeeSerializer(name).data)
        return names

    def get_request_date(self, obj):
        if obj.branch.date_format == 'dd/mm/yyyy':
            date_is = obj.request_date.strftime('%d-%m-%Y')
            return date_is
        elif obj.branch.date_format == 'mm/dd/yyyy':
            date_is = obj.request_date.strftime('%m-%d-%Y')
            return date_is
        else:
            date_is = obj.request_date.strftime('%Y-%m-%d')
            return date_is

    def get_loan_release_date(self, obj):
        if obj.loan_release_date:
            if obj.branch.date_format == 'dd/mm/yyyy':
                date_is = obj.loan_release_date.strftime('%d-%m-%Y')
                return date_is
            elif obj.branch.date_format == 'mm/dd/yyyy':
                date_is = obj.loan_release_date.strftime('%m-%d-%Y')
                return date_is
            else:
                date_is = obj.loan_release_date.strftime('%Y-%m-%d')
                return date_is

    def get_interest_start_date(self, obj):
        if obj.interest_start_date:
            if obj.branch.date_format == 'dd/mm/yyyy':
                date_is = obj.interest_start_date.strftime('%d-%m-%Y')
                return date_is
            elif obj.branch.date_format == 'mm/dd/yyyy':
                date_is = obj.interest_start_date.strftime('%m-%d-%Y')
                return date_is
            else:
                date_is = obj.interest_start_date.strftime('%Y-%m-%d')
                return date_is

    def get_maturity_date(self, obj):
        if obj.maturity_date:
            if obj.branch.date_format == 'dd/mm/yyyy':
                date_is = obj.maturity_date.strftime('%d-%m-%Y')
                return date_is
            elif obj.branch.date_format == 'mm/dd/yyyy':
                date_is = obj.maturity_date.strftime('%m-%d-%Y')
                return date_is
            else:
                date_is = obj.maturity_date.strftime('%Y-%m-%d')
                return date_is
    
class LoanGuarantorSerializer2(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanGuarantor



class LoanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanType


class LoanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanComment

class LoanOfficerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'
        model = LoanOfficer
    def get_name(self, obj):
        name = obj.staff_id.user_id.user.first_name
        return name

class LoanDisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanDisbursement

class LoanMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanMembership

class LoanCollateralSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanCollateral




class LoanCollateralSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanCollateral

class LoanAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanAttachment
# class LoanRepaymentSerializer(serializers.ModelSerializer):
class GuarantorFileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GuarantorFile





class LoanRepaymentSerializer(serializers.ModelSerializer):
    loan = serializers.SerializerMethodField()
    collector = serializers.SerializerMethodField()


    class Meta:
        fields = '__all__'
        model = LoanRepayment

    def get_loan(self, obj):
        name = obj.loan.loan_title
        return name

    def get_collector(self, obj):
        if obj.collector:
            name = obj.collector.staff_id.user_id.user.first_name + ' ' + str(obj.collector.staff_id.user_id.user.last_name)
            return name
        else:
            return False

class LoanRepaymentSerializer2(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanRepayment


class LoanDisbursementSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanDisbursement

class LoanSchedulerSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = LoanScheduler