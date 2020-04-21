from django.shortcuts import render
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.schedules import crontab
from celery import shared_task
from .serializers import (
    SavingsTransactionSerializer, SavingsProductSerializer,
    SavingsAccountSerializer, TellerSerializer,
    CashSourceSerializer, TransferCashSerializer,
    SavingsProductReportSerializer, TellerReportSerializer,
    TransferFundSerializer
)
from .models import (
    SavingsTransaction, SavingsProduct,
    SavingsAccount, Teller,
    CashSource, TransferCash,
    FundTransferLog
)
# Create your views here.


class SavingsProductViewSet(ModelViewSet):
    # serializer_class = SavingsProductSerializer

    def get_serializer_class(self):
        report = self.request.GET.get("report")
        if report and (report == 'true'):
            return SavingsProductReportSerializer
        return SavingsProductSerializer

    def get_queryset(self):
        queryset = SavingsProduct.objects.all()

        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__pk=branch)

        return queryset


class SavingsAccountViewSet(ModelViewSet):
    serializer_class = SavingsAccountSerializer

    def get_queryset(self):
        queryset = SavingsAccount.objects.all()

        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__pk=branch)

        savings_product = self.request.GET.get('savings_product')
        if savings_product:
            queryset = queryset.filter(savings_product__id=savings_product)

        return queryset


class TellerViewSet(ModelViewSet):
    # serializer_class = TellerSerializer

    def get_serializer_class(self):
        report = self.request.GET.get("report")
        if report and (report == 'true'):
            return TellerReportSerializer
        return TellerSerializer

    def get_queryset(self):
        queryset = Teller.objects.all()

        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(cash_safe_management__branch__pk=branch)

        return queryset


class SavingsTransactionViewSet(ModelViewSet):
    serializer_class = SavingsTransactionSerializer

    def get_queryset(self):
        queryset = SavingsTransaction.objects.all()

        savings_account = self.request.GET.get("savings_account")
        if savings_account:
            queryset = queryset.filter(savings_account__pk=savings_account)

        branch = self.request.GET.get("branch")
        if branch:
            queryset = queryset.filter(branch__pk=branch)

        date_from = self.request.GET.get("date_from")
        if date_from:
            queryset = queryset.filter(date_time__gte=date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            queryset = queryset.filter(date_time__lte=date_to)

        approved = self.request.GET.get("approved")
        if approved and (approved == 'true'):
            queryset = queryset.filter(approved=True)

        return queryset


class CashSourceViewSet(ModelViewSet):
    serializer_class = CashSourceSerializer

    def get_queryset(self):
        queryset = CashSource.objects.all()

        branch = self.request.GET.get("branch")
        if branch:
            queryset = queryset.filter(cash_safe_management__branch__pk=branch)

        return queryset


class TransferCashViewSet(ModelViewSet):
    serializer_class = TransferCashSerializer

    def get_queryset(self):
        queryset = TransferCash.objects.all()

        return queryset


class FundTransferLogViewSet(ModelViewSet):
    serializer_class = TransferFundSerializer

    def get_queryset(self):
        queryset = FundTransferLog.objects.all()

        branch = self.request.GET.get("branch")
        if branch:
            queryset = queryset.filter(branch__pk=branch)

        teller = self.request.GET.get("teller")
        if teller:
            queryset = queryset.filter(teller__pk=teller)

        date_from = self.request.GET.get("date_from")
        if date_from:
            queryset = queryset.filter(date_time__gte=date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            queryset = queryset.filter(date_time__lte=date_to)

        return queryset
        
