from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import PayrollSerializer
from .models import Payroll
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
