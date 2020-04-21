from rest_framework import serializers
from .models import (
    CalendarEvent, CalendarEventEmail, CalendarLog,
    OtherIncomeType, OtherIncome, OtherIncomeDocuments
)


class CalendarLogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CalendarLog


class CalendarEventSerializer(serializers.ModelSerializer):
    emails = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = CalendarEvent

    def get_emails(self, obj):
        emails = []
        for email in obj.calendareventemail_set.all():
            emails.append(CalendarEventEmailSerializer(email).data)
        return emails


class CalendarEventEmailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CalendarEventEmail


class OtherIncomeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = OtherIncomeType


class OtherIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = OtherIncome


class OtherIncomeDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = OtherIncomeDocuments
