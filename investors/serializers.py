from rest_framework import serializers
#from django_restql.mixins import DynamicFieldsMixin
from .models import (
    Investor, InvestorDocuments, InvestorInvitation,
    LoanInvestmentProduct, LoanInvestment, InvestorInvite,
    InvestorProduct, InvestorAccount,
    InvestorTransaction
)


class InvestorSerializer(serializers.ModelSerializer):

    investor_documents = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()

    class Meta:
        model = Investor
        fields = '__all__'

    def get_investor_documents(self, obj):
        investor_documents = []
        for file in obj.investordocuments_set.all():
            investor_documents.append(InvestorDocumentsSerializer(file).data)
        return investor_documents

    def get_date_of_birth(self, obj):
        if obj.date_of_birth:
            if obj.profile.branch.date_format == 'dd/mm/yyyy':
                date_is = obj.date_of_birth.strftime('%d-%m-%Y')
                return date_is
            elif obj.profile.branch.date_format == 'mm/dd/yyyy':
                date_is = obj.date_of_birth.strftime('%m-%d-%Y')
                return date_is
            else:
                date_is = obj.date_of_birth.strftime('%Y-%m-%d')
                return date_is


class InvestorDocumentsSerializer(serializers.ModelSerializer):
    investor = serializers.SerializerMethodField()

    class Meta:
        model = InvestorDocuments
        fields = '__all__'

    def get_investor(self, obj):
        name = obj.investor.first_name + ' ' + str(obj.investor.last_name)
        return name


class InvestorInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorInvitation
        fields = '__all__'


class InvestorInviteSerializer( serializers.ModelSerializer):

    class Meta:
        model = InvestorInvite
        fields = '__all__'

class LoanInvestmentProductSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = LoanInvestmentProduct
        fields = '__all__'

    def get_branch(self, obj):
        if obj.branch:
            name = obj.branch.name
            return name

    def get_date(self, obj):
        if obj.branch:
            if obj.date:
                if obj.branch.date_format == 'dd/mm/yyyy':
                    date_is = obj.date.strftime('%d-%m-%Y')
                    return date_is
                elif obj.branch.date_format == 'mm/dd/yyyy':
                    date_is = obj.date.strftime('%m-%d-%Y')
                    return date_is
                else:
                    date_is = obj.date.strftime('%m-%d-%Y')
                    return date_is


class LoanInvestmentSerializer(serializers.ModelSerializer):
    loan_investment_product_detail = serializers.SerializerMethodField()
    loan_investment_product = serializers.SerializerMethodField()
    loan = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = LoanInvestment
        fields = '__all__'

    def get_loan_investment_product_detail(self, obj):
        return LoanInvestmentProductSerializer(obj.loan_investment_product).data

    def get_loan_investment_product(self, obj):
        name = obj.loan_investment_product.name
        return name

    def get_loan(self, obj):
        name = obj.loan.loan_title + ' - ' + str(obj.loan.account_number)
        return name

    def get_start_date(self, obj):
        if obj.loan.branch.date_format == 'dd/mm/yyyy':
            date_is = obj.start_date.strftime('%d-%m-%Y')
            return date_is
        elif obj.loan.branch.date_format == 'mm/dd/yyyy':
            date_is = obj.start_date.strftime('%m-%d-%Y')
            return date_is
        else:
            date_is = obj.start_date.strftime('%Y-%m-%d')
            return date_is

    def get_end_date(self, obj):
        if obj.loan.branch.date_format == 'dd/mm/yyyy':
            date_is = obj.end_date.strftime('%d-%m-%Y')
            return date_is
        elif obj.loan.branch.date_format == 'mm/dd/yyyy':
            date_is = obj.end_date.strftime('%m-%d-%Y')
            return date_is
        else:
            date_is = obj.end_date.strftime('%Y-%m-%d')
            return date_is


class InvestorProductSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = InvestorProduct
        fields = '__all__'

    def get_branch(self, obj):
        if obj.branch:
            name = obj.branch.name
            return name

    def get_date(self, obj):
        if obj.branch.date_format == 'dd/mm/yyyy':
            date_is = obj.date.strftime('%d-%m-%Y')
            return date_is
        elif obj.branch.date_format == 'mm/dd/yyyy':
            date_is = obj.date.strftime('%m-%d-%Y')
            return date_is
        else:
            date_is = obj.date.strftime('%Y-%m-%d')
            return date_is

class InvestorAccountSerializer(serializers.ModelSerializer):
    investor = serializers.SerializerMethodField()
    investor_product = serializers.SerializerMethodField()

    class Meta:
        model = InvestorAccount
        fields = '__all__'

    def get_investor(self, obj):
        name = obj.investor.first_name + ' ' + str(obj.investor.last_name)
        return name

    def get_investor_product(self, obj):
        name = obj.investor_product.title
        return name


class InvestorTransactionSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    investor_account = serializers.SerializerMethodField()
    date_time = serializers.SerializerMethodField()

    class Meta:
        model = InvestorTransaction
        fields = '__all__'

    def get_branch(self, obj):
        name = obj.branch.name
        return name

    def get_investor_account(self, obj):
        name = obj.investor_account.investor.first_name + ' ' + str(obj.investor_account.investor.last_name)
        return name

    def get_date_time(self, obj):
        if obj.branch.date_format == 'dd/mm/yyyy':
            date_is = obj.date_time.strftime('%d-%m-%Y, %I:%M:%p')
            return date_is
        elif obj.branch.date_format == 'mm/dd/yyyy':
            date_is = obj.date_time.strftime('%m-%d-%Y, %I:%M:%p')
            return date_is
        else:
            date_is = obj.date_time.strftime('%Y-%m-%d, %I:%M:%p')
            return date_is
