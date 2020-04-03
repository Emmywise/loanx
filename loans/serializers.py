from rest_framework import serializers
from .models import Loan, LoanComment, LoanRepayment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Loan


class LoanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanComment


class LoanRepaymentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanRepayment
