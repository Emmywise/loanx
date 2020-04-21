from django.shortcuts import render
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .models import (AssetType, Asset, AssetDocument, AssetValuation,
                     Expense, ExpensesType, ExpenseDocument)
from .serializers import (AssetTypeSerializer, AssetSerializer,
                          AssetDocumentSerializer, AssetValuationSerializer,
                          ExpensesTypeSerializer, ExpenseSerializer, ExpenseDocumentSerializer)
# Create your views here.


class AssetTypeViewSet(ModelViewSet):
    serializer_class = AssetTypeSerializer

    def get_queryset(self):
        queryset = AssetType.objects.all()

        return queryset


class AssetViewSet(ModelViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        queryset = Asset.objects.all()

        branch = self.request.GET.get("branch")
        if branch:
            queryset = queryset.filter(branch__pk=branch)

        date_from = self.request.GET.get("date_from")
        if date_from:
            queryset = queryset.filter(purchased_date__gte=date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            queryset = queryset.filter(purchased_date__lte=date_to)

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(serial_number__icontains=q) |
                Q(bought_from__icontains=q)
            ).distinct()

        return queryset


class AssetDocumentViewSet(ModelViewSet):
    serializer_class = AssetDocumentSerializer

    def get_queryset(self):
        queryset = AssetDocument.objects.all()

        asset = self.request.GET.get("asset")
        if asset:
            queryset = queryset.filter(asset__pk=asset)

        return queryset


class AssetValuationViewSet(ModelViewSet):
    serializer_class = AssetValuationSerializer

    def get_queryset(self):
        queryset = AssetValuation.objects.all()

        asset = self.request.GET.get("asset")
        if asset:
            queryset = queryset.filter(asset__pk=asset)

        return queryset


class ExpenseTypeViewSet(ModelViewSet):
    serializer_class = ExpensesTypeSerializer

    def get_queryset(self):
        queryset = ExpensesType.objects.all()

        return queryset


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        queryset = Expense.objects.all()

        branch = self.request.GET.get("branch")
        if branch:
            queryset = queryset.filter(branch__pk=branch)

        date_from = self.request.GET.get("date_from")
        if date_from:
            queryset = queryset.filter(purchased_date__gte=date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            queryset = queryset.filter(purchased_date__lte=date_to)

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(serial_number__icontains=q) |
                Q(bought_from__icontains=q)
            ).distinct()

        return queryset


class ExpenseDocumentViewSet(ModelViewSet):
    serializer_class = ExpenseDocumentSerializer

    def get_queryset(self):
        queryset = ExpenseDocument.objects.all()

        asset = self.request.GET.get("asset")
        if asset:
            queryset = queryset.filter(asset__pk=asset)

        return queryset
