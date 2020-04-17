from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.schedules import crontab
from celery import shared_task
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



class InitiateCreditSavings(APIView):
    def post(self, request, pk=None):
        """collect id of savings account"""
        savings_account = SavingsAccount.objects.get(pk = int(request.data.get('savings_account')))
        posting_frequency = savings_account.savings_product.interest_posting_frequency
        total_annual_interest = (((float(savings_account.savings_product.interest_rate_per_annum)/100))*(float(savings_account.available_balance)))
        match_selection = {"Every 1 Month":12,"Every 2 Month":6,"Every 3 Month":4,"Every 4 Month":3,"Every 6 Month":2,"Every 12 Month":1}
        def check_freq(freq):
            return match_selection[freq]
        @shared_task
        def credit_savings_account():
            savings_account.available_balance += (total_annual_interest/check_freq(savings_account.savings_product.interest_rate_per_annum))
            savings_account.ledger_balance += (total_annual_interest/check_freq(savings_account.savings_product.interest_rate_per_annum))
            savings_account.save()
            return "code ran successfully"

        if(savings_account.savings_product.interest_posting_frequency == 'Every 1 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/12', **kwargs),
                },
            }
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 2 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    #'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/6', **kwargs),
                    'schedule': crontab(minute='03', hour='19', day_of_month='14', month_of_year='*/6', **kwargs),
                },
            }
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 3 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/4', **kwargs),
                },
            }
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 4 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/3', **kwargs),
                },
            }
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 6 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/2', **kwargs),
                },
            }
        elif(savings_account.savings_product.interest_rate_per_annum == 'Every 12 Month'):
            app.conf.beat_schedule = {
                'add-every-monday-morning': {
                    'task': 'credit_savings_account',
                    'schedule': crontab(minute='00', hour='00', day_of_month='1', month_of_year='*/1', **kwargs),
                },
            }
        return Response({"msg":"successful"})