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


class SavingsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsTransaction
        fields = '__all__'
