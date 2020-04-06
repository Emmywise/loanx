from rest_framework import serializers
from .models import (
    Loan, LoanComment, LoanRepayment,
    LoanCollateral, LoanGuarantor,
    GuarantorFile
)


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
        model = LoanOfficer


class LoanRepaymentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanRepayment

