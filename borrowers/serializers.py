from rest_framework import serializers
from .models import *
from loans.models import Loan


class BorrowerSerializer(serializers.ModelSerializer):
    loan_officer = serializers.SerializerMethodField()
    # date_of_birth = serializers.SerializerMethodField()
    existing_loans = serializers.SerializerMethodField()
    total_paid_loans = serializers.SerializerMethodField()

    class Meta:
        model = Borrower
        read_only_fields = ('is_activated',)
        fields = '__all__'

    def get_loan_officer(self, obj):
        if obj.loan_officer:
            name = obj.loan_officer.staff_id.user_id.user.first_name + ' ' + str(obj.loan_officer.staff_id.user_id.user.last_name)
            return name

    # def get_date_of_birth(self, obj):
    #     if obj.date_of_birth:
    #         if obj.profile.profile.branch.date_format == 'dd/mm/yyyy':
    #             date_is = obj.date_of_birth.strftime('%d-%m-%Y')
    #             return date_is
    #         elif obj.profile.profile.branch.date_format == 'mm/dd/yyyy':
    #             date_is = obj.date_of_birth.strftime('%m-%d-%Y')
    #             return date_is
    #         else:
    #             date_is = obj.date_of_birth.strftime('%Y-%m-%d')
    #             return date_is

    def get_existing_loans(self, obj):
        counts = Loan.objects.all().filter(borrower=obj.id).count()
        return counts

    def get_total_paid_loans(self, obj):
        counts = Loan.objects.all().filter(borrower=obj.id).filter(status="fully paid").count()
        return counts

class BorrowerSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        read_only_fields = ('is_activated',)
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class BorrowerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowerGroup
        fields = '__all__'


class InviteBorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteBorrower
        fields = '__all__'