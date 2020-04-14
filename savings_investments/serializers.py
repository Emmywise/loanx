from rest_framework import serializers
from .models import *


class SavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = '__all__'


class SavingsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProduct
        fields = '__all__'


class CashSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashSource
        fields = '__all__'


class TellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teller
        fields = '__all__'


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
