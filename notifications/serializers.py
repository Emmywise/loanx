from rest_framework import serializers
from .models import *


class SendSMSSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = SMS

class SendEmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = SMS
        