from rest_framework import serializers
from .models import Loan, LoanComment

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Loan

class LoanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanComment