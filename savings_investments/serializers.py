from rest_framework import serializers
from .models import *


class SavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = '__all__'


class SavingsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProduct
        # fields = '__all__'
        exclude = ['name', 'deposit', 'transfer_in', 'withdrawal', 'fees',
                   'interest', 'dividend', 'transfer_out', 'commission',
                   'balance']


class SavingsProductReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProduct
        fields = ['deposit', 'transfer_in', 'withdrawal', 'fees',
                  'interest', 'dividend', 'transfer_out', 'commission',
                  'balance']


class CashSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashSource
        fields = '__all__'


class TellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teller
        exclude = ['report_deposit', 'report_transfer_in', 'report_withdrawal', 'report_fees',
                   'report_interest', 'report_dividend', 'report_transfer_out', 'report_commission',
                   'report_balance']


class TellerReportSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Teller
        fields = ['name', 'report_deposit', 'report_transfer_in', 'report_withdrawal', 'report_fees',
                  'report_interest', 'report_dividend', 'report_transfer_out', 'report_commission',
                  'report_balance']

    def get_name(self, obj):
        return obj.staff.user.username


class TransferCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferCash
        fields = '__all__'

    def raise_error(self):
        raise ValidationError("Incorrect request, transfer should"
                              " occur between 'from_cash_source' - 'to_cash_source', "
                              "'from_cash_source' - 'to_teller', 'from_teller' - 'to_teller', "
                              "or 'from_teller' - 'to_cash_source'")

    def validate(self, attrs):
        # validate transfer cash
        transfer_counter = 0
        if attrs.get("from_cash_source"):
            transfer_counter += 1
        if attrs.get("to_cash_source"):
            transfer_counter += 1
        if attrs.get("from_teller"):
            transfer_counter += 1
        if attrs.get("to_teller"):
            transfer_counter += 1
        if transfer_counter != 2:
            self.raise_error()
        if (attrs.get("from_cash_source") and attrs.get("to_cash_source")) or \
                (attrs.get("from_cash_source") and attrs.get("to_teller")) or \
                (attrs.get("from_teller") and attrs.get("to_teller")) or \
                (attrs.get("from_teller") and attrs.get("to_cash_source")):

            if (attrs.get('to_cash_source') is not None) and (attrs.get('from_cash_source') is not None):
                if attrs.get("to_cash_source") == attrs.get("from_cash_source"):
                    raise ValidationError("impossible to transfer cash from same cash source")

            if (attrs.get('to_teller') is not None) and (attrs.get('from_teller') is not None):
                if attrs.get("to_teller") == attrs.get("from_teller"):
                    raise ValidationError("impossible to transfer cash from same teller")
            return attrs
        self.raise_error()


class SavingsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsTransaction
        fields = '__all__'


class TransferFundSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = FundTransferLog

    def validate(self, attrs):
        if attrs['from_account'] == attrs['to_account']:
            raise serializers.ValidationError("cannot transfer fund from/to same account")
        return attrs


class SavingsFeeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = SavingsFee
