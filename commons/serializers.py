from rest_framework import serializers
from .models import AssetType, Asset, AssetDocument, AssetValuation


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
