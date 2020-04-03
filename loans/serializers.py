from rest_framework import serializers
from .models import Loan, LoanComment, LoanOfficer

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