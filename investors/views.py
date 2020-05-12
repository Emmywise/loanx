from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import (
    Investor, InvestorDocuments, InvestorInvitation,
    LoanInvestmentProduct, LoanInvestment,
    InvestorProduct, InvestorAccount,
    InvestorTransaction
)
from .serializers import (
    InvestorSerializer, InvestorDocumentsSerializer, InvestorInvitationSerializer,
    LoanInvestmentProductSerializer, LoanInvestmentSerializer,
    InvestorProductSerializer, InvestorAccountSerializer,
    InvestorTransactionSerializer
)
# Create your views here.


class InvestorViewSet(ModelViewSet):
    serializer_class = InvestorSerializer

    def get_queryset(self):
        queryset = Investor.objects.all()
        investor_id = self.request.GET.get("investor_id")
        if investor_id:
            queryset = queryset.filter(investor_id=investor_id)
        return queryset


class InvestorDocumentsViewSet(ModelViewSet):
    serializer_class = InvestorDocumentsSerializer

    def get_queryset(self):
        queryset = InvestorDocuments.objects.all()
        investor = self.request.GET.get('investor')
        if investor:
            queryset = queryset.filter(investor__id=investor)

        return queryset


class InvestorInvitationViewSet(ModelViewSet):
    serializer_class = InvestorInvitationSerializer

    def get_queryset(self):
        queryset = InvestorInvitation.objects.all()

        return queryset


class LoanInvestmentProductViewSet(ModelViewSet):
    serializer_class = LoanInvestmentProductSerializer

    def get_queryset(self):
        queryset = LoanInvestmentProduct.objects.all()
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__id=branch)
        return queryset


class LoanInvestmentViewSet(ModelViewSet):
    serializer_class = LoanInvestmentSerializer

    def get_queryset(self):
        queryset = LoanInvestment.objects.all()
        
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__id=branch)
        
        return queryset


class InvestorProductViewSet(ModelViewSet):
    serializer_class = InvestorProductSerializer

    def get_queryset(self):
        queryset = InvestorProduct.objects.all()

        return queryset


class InvestorAccountViewSet(ModelViewSet):
    serializer_class = InvestorAccountSerializer

    def get_queryset(self):
        queryset = InvestorAccount.objects.all()
        
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(investor_product__branch__id=branch)
        investor = self.request.GET.get('investor')
        if investor:
            queryset = queryset.filter(investor__id=investor)

        return queryset


class InvestorTransactionViewSet(ModelViewSet):
    serializer_class = InvestorTransactionSerializer

    def get_queryset(self):
        queryset = InvestorTransaction.objects.all()

        return queryset
