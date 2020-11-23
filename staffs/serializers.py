from rest_framework import serializers
from .models import Payroll, Staff


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

class StaffSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	branch = serializers.SerializerMethodField()

	class Meta:
		fields = '__all__'
		model = Staff

	def get_name(self, obj):
		name = obj.user_id.user.first_name + ' ' + str(obj.user_id.user.last_name)
		return name

	def get_email(self, obj):
		return obj.user_id.user.email

	def get_branch(self, obj):
		return obj.user_id.branch.name
