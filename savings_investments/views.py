from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    SavingsTransactionSerializer, SavingsProductSerializer,
    SavingsAccountSerializer, TellerSerializer,
    CashSourceSerializer, TransferCashSerializer
)
from .models import (
    SavingsTransaction, SavingsProduct,
    SavingsAccount, Teller,
    CashSource, TransferCash
)
# Create your views here.


class SavingsProductViewSet(ModelViewSet):
    serializer_class = SavingsProductSerializer

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
    serializer_class = TellerSerializer

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
