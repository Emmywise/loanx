from rest_framework import serializers
from .models import (
    CalendarEvent, CalendarEventEmail, CalendarLog,
)


class CalendarLogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CalendarLog


class CalendarEventSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CalendarEvent


class CalendarEventEmailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CalendarEventEmail
