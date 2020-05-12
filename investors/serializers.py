from rest_framework import serializers
from .models import (
    Investor, InvestorDocuments, InvestorInvitation,
    LoanInvestmentProduct, LoanInvestment,
    InvestorProduct, InvestorAccount,
    InvestorTransaction
)


class InvestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investor
        fields = '__all__'


class InvestorDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorDocuments
        fields = '__all__'


class InvestorInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorInvitation
        fields = '__all__'


class LoanInvestmentProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanInvestmentProduct
        fields = '__all__'


class LoanInvestmentSerializer(serializers.ModelSerializer):
    loan_investment_product_detail = serializers.SerializerMethodField()

    class Meta:
        model = LoanInvestment
        fields = '__all__'

    def get_loan_investment_product_detail(self, obj):
        return LoanInvestmentProductSerializer(obj.loan_investment_product).data


class InvestorProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorProduct
        fields = '__all__'


class InvestorAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorAccount
        fields = '__all__'


class InvestorTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorTransaction
        fields = '__all__'
