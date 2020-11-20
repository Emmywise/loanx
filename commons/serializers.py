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
    branch = serializers.SerializerMethodField()
    asset_type = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Asset

    def get_branch(self, obj):
        name = obj.branch.name
        return name

    def get_asset_type(self, obj):
        name = obj.asset_type.name
        return name

class AssetSerializer2(serializers.ModelSerializer):
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
