from rest_framework import serializers
<<<<<<< HEAD
from .models import Loan, LoanComment, LoanOfficer
=======
from .models import Loan, LoanComment, LoanRepayment

>>>>>>> 5a310ee418f568dbd8cb38483d9804b8206152c6

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Loan


class LoanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanComment

<<<<<<< HEAD
class LoanOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LoanOfficer
=======

class LoanRepaymentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = LoanRepayment
>>>>>>> 5a310ee418f568dbd8cb38483d9804b8206152c6
