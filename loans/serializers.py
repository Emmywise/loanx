from rest_framework import serializers
from .models import Loan, LoanComment, LoanOfficer, LoanFee, LoanCollateral, LoanAttachment
from .models import (
    Loan, LoanComment, LoanRepayment,
    LoanCollateral, LoanGuarantor,
    GuarantorFile, LoanDisbursement, LoanScheduler, LoanMembership
)

from .models import (Loan, LoanComment, LoanOfficer, LoanFee,
LoanCollateral, LoanAttachment, LoanRepayment, GuarantorFile, LoanGuarantor, LoanDisbursement)

class LoanSerializer(serializers.ModelSerializer):
    # remaining_balance = serializers.ReadOnlyField(source="self.get_balance")
    # released = serializers.ReadOnlyField(source="self.released")
    # maturity = serializers.ReadOnlyField(source="self.maturity")
    class Meta:
        fields = '__all__'
        model = Loan


class LoanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanComment

class LoanOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanOfficer

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


class LoanFeeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanFee


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


class LoanRepaymentSerializer(serializers.ModelSerializer):

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