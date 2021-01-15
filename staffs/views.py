from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import PayrollSerializer, StaffSerializer
from .models import Payroll, Staff
from accounts.models import *
from django.db.models import Q
from rest_framework import status
from loan_management_system import permissions as perms

from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


class PayrollViewSet(ModelViewSet):

    serializer_class = PayrollSerializer

    def get_queryset(self):
        queryset = Payroll.objects.all()
        params = self.request.GET
        branch = params.get('branch')
        date_from = params.get('date_from')
        date_to = params.get('date_to')
        staff = params.get('staff')
        multiple_staffs = params.get('multiple_staffs')
        if branch:
            queryset = queryset.filter(branch__pk=branch)
        if staff:
            queryset = queryset.filter(staff__pk=staff)
        if date_from:
            queryset = queryset.filter(pay_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(pay_date__lte=date_to)
        if multiple_staffs:
            staffs = multiple_staffs.split(',')
            validated_staffs = []
            for staff in staffs:
                try:
                    User.objects.get(id=staff)
                    validated_staffs.append(staff)
                except User.DoesNotExist:
                    pass
            if len(validated_staffs) > 0:
                queryset = queryset.filter(pk__in=validated_staffs)

        return queryset


@api_view(['GET', 'DELETE', 'PATCH', 'POST'])
def get_delete_update_staff(request, pk):
    try:
        staff = Staff.objects.get(pk=pk)
    except Staff.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        permission_classes = (perms.IsStaffOrAdmin,)
        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        permission_classes = (perms.IsStaffOrAdmin,)
        serializer = StaffSerializer(staff, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        borrower.delete()
        return Response("Borrower deleted successfully", status=204)


@api_view(['GET', 'POST'])
def get_post_staff(request):
    # get all restaurants
    if request.method == 'GET':
        permission_classes = (perms.IsStaffOrAdmin,)
        ref = request.GET.get("staff_search")
        if ref:
            staff = Staff.objects.filter(Q(user_id__user__first_name__startswith=ref))
            serializer = StaffSerializer(staff, many=True)
            return Response(serializer.data)
        staffs = Staff.objects.all()
        serializer = StaffSerializer(staffs, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant
    elif request.method == 'POST':
        data = {
            'user_id': request.data.get('user_id'),
        }
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
