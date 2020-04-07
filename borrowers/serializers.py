from rest_framework import serializers
from .models import *


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'


# class BorrowerGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BorrowerGroup
#         fields = '__all__'