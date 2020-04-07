from rest_framework import serializers
from .models import Loan, LoanComment, LoanOfficer, LoanFee, LoanCollateral, LoanAttachment

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
        model = LoanOfficer


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

#     class Meta:
#         fields = '__all__'
#         model = LoanRepayment

