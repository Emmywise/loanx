from rest_framework import serializers
from .models import *


class SavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = '__all__'
