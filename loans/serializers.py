from rest_framework import serializers
<<<<<<< HEAD
from .models import Loan, LoanComment, LoanOfficer, LoanFee, LoanCollateral, LoanAttachment
=======
from .models import (
    Loan, LoanComment, LoanRepayment,
    LoanCollateral, LoanGuarantor,
    GuarantorFile, LoanDisbursement
)

>>>>>>> 977292559276aba1dda602b31ba9bb19a22d234c

class LoanSerializer(serializers.ModelSerializer):
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
        model = LoanRepayment


class LoanCollateralSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanCollateral


<<<<<<< HEAD
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
=======
class GuarantorFileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GuarantorFile
>>>>>>> 977292559276aba1dda602b31ba9bb19a22d234c


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
