from rest_framework import serializers
from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    staff_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Payroll

    def get_staff_name(self, obj):
        return obj.staff.user.username

    def get_branch_name(self, obj):
        return obj.branch.name
