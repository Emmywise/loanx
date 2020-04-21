from rest_framework import serializers
from .models import (
    AssetType, Asset, AssetDocument, 
    AssetValuation, Expense, ExpenseDocument,
    ExpensesType
    )


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AssetType


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Asset


class AssetDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AssetDocument


class AssetValuationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AssetValuation


class ExpensesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ExpensesType


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Expense


class ExpenseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ExpenseDocument
