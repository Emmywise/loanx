from django.shortcuts import render
import datetime
import calendar
from django.utils import timezone
from django.db.models import Q
from fine_search.fine_search import perform_search_queryset
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    CalendarEventEmail, CalendarEvent, CalendarLog,
    OtherIncomeType, OtherIncome, OtherIncomeDocuments, LoanBorrowerReport
)

from .serializers import (
    CalendarEventEmailSerializer, CalendarEventSerializer, 
    CalendarLogSerializer, OtherIncomeTypeSerializer,
    OtherIncomeSerializer, OtherIncomeDocumentsSerializer,
    LoanBorrowerReportSerializer
)
from loans.models import Loan
from borrowers.models import Borrower

# Create your views here.


def filter_date(request, queryset):
    view = request.GET.get('view')
    date = request.GET.get('date')
    if date:
        date_split = date.split('-')
        date_split = list(map(int, date_split))
        current_date_lower = datetime.datetime(date_split[0], date_split[1], date_split[2],
                                               tzinfo=timezone.utc)
        current_date_upper = datetime.datetime(date_split[0], date_split[1], date_split[2],
                                               23, 59, 59,
                                               tzinfo=timezone.utc)
        lower_date_week = current_date_lower + datetime.timedelta(days=-current_date_lower.weekday())
        upper_date_week = current_date_upper + datetime.timedelta(days=6 - current_date_upper.weekday())
        lower_date_month = datetime.datetime(date_split[0], date_split[1], 1, tzinfo=timezone.utc)
        upper_date_month = datetime.datetime(date_split[0], date_split[1],
                                             calendar.monthrange(date_split[0], date_split[1])[1], tzinfo=timezone.utc)

        if view and (view == 'daily'):
            queryset = queryset.filter(
                Q(date__day=current_date_lower.day) &
                Q(date__month=current_date_lower.month) &
                Q(date__year=current_date_lower.year)
            )

        if view and (view == 'weekly'):
            queryset = queryset.filter(
                Q(date__gte=lower_date_week) &
                Q(date__lte=upper_date_week)
            )
        if view and (view == 'monthly'):
            queryset = queryset.filter(
                Q(date__gte=lower_date_month) &
                Q(date__lte=upper_date_month)
            )

    return queryset


class CalenderEventEmailViewSet(ModelViewSet):
    serializer_class = CalendarEventEmailSerializer

    def get_queryset(self):
        queryset = CalendarEventEmail.objects.all()
        if self.request.GET.get('calendar_event'):
            queryset = queryset.filter(
                calendar__pk=self.request.GET.get('calendar_event')
            )
        return queryset


class CalendarEventViewSet(ModelViewSet):
    serializer_class = CalendarEventSerializer

    def get_queryset(self):
        queryset = CalendarEvent.objects.all()

        branch = self.request.GET.get('branch')
        date_from = self.request.GET.get('date_from')
        till_date = self.request.GET.get('till_date')
        q = self.request.GET.get('q')

        if branch:
            queryset = queryset.filter(branch__pk=branch)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if till_date:
            queryset = queryset.filter(date__lte=till_date)
        queryset = filter_date(self.request, queryset)
        if q:
            queryset = perform_search_queryset(queryset, q, ['title', 'description'])
        return queryset


class CalendarLogViewSet(ModelViewSet):
    serializer_class = CalendarLogSerializer

    def get_queryset(self):
        queryset = CalendarLog.objects.all()
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__pk=branch)
        queryset = filter_date(self.request, queryset)
        return queryset


class OtherIncomeTypeViewSet(ModelViewSet):
    serializer_class = OtherIncomeTypeSerializer

    def get_queryset(self):
        queryset = OtherIncomeType.objects.all()

        return queryset


class OtherIncomeViewSet(ModelViewSet):
    serializer_class = OtherIncomeSerializer

    def get_queryset(self):
        queryset = OtherIncome.objects.all()
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__pk=branch)
        queryset = filter_date(self.request, queryset)
        return queryset


class OtherIncomeDocumentsViewSet(ModelViewSet):
    serializer_class = OtherIncomeDocumentsSerializer

    def get_queryset(self):
        queryset = OtherIncomeDocuments.objects.all()
        income = self.request.GET.get('income')
        if income:
            queryset = queryset.filter(income__pk=income)
        queryset = filter_date(self.request, queryset)
        return queryset

class BorrowersReport(APIView):
    def post(self, request, pk=None):
       
        borrower = request.data.get('borrower')
        borrower_instance = Borrower.objects.get(pk = int(borrower))
        loans_released = Loan.objects.filter(borrower = borrower_instance).exclude(status = "processing").exclude(status = "denied")
        due_loans = Loan.objects.filter(status = "past maturity")
        no_loan_released = len(loans_released)
        principal_released = 0
        amount_paid = 0
        due_loans_principal = 0
        due_loans_interest = 0
        due_loans_fees = 0
        due_loans_penalty = 0
        due_loans_total = 0
        payments_principal = 0
        payments_interest = 0
        payments_fees = 0
        payments_penalty = 0
        p_i_released = 0
        p_i_f_released = 0
        p_i_f_p_released = 0
        #try except to avoid breaking for people without loans released
        # try:
        for each_loan_released in loans_released:
            principal_released += each_loan_released.principal_amount
            p_i_released += (each_loan_released.principal_amount + each_loan_released.interest)
            p_i_f_released += (each_loan_released.principal_amount + each_loan_released.interest + each_loan_released.loan_fees)
            p_i_f_p_released += (each_loan_released.principal_amount + each_loan_released.interest + each_loan_released.loan_fees + each_loan_released.penalty_amount)
            amount_paid += each_loan_released.amount_paid
            
        # except:
        #     pass
        principal_at_risk = principal_released - amount_paid
        #where amount paid is higher than principal released
        if principal_at_risk < 0.00:
            principal_at_risk = 0.00
        # try:
        for each_due_loan in due_loans:
            due_loans_principal += each_due_loan.principal_amount
            due_loans_interest += each_due_loan.interest
            due_loans_fees += each_due_loan.loan_fees
            due_loans_penalty += each_due_loan.penalty_amount
            due_loans_total = due_loans_principal + due_loans_interest + due_loans_fees + due_loans_penalty
        # except:
        #     pass
        if amount_paid < principal_released:
            payments_principal = principal_released - amount_paid
            #payments interest, fees and penalties retain values of 0.00
        elif amount_paid > principal_released and amount_paid < p_i_released:
            payments_principal = principal_released
            payments_interest = p_i_released - amount_paid
        elif amount_paid > p_i_released and amount_paid < p_i_f_released:
            payments_principal = principal_released
            payments_interest = p_i_released - principal_released
            payments_fees = p_i_f_released - amount_paid
        elif amount_paid > p_i_f_released and amount_paid < p_i_f_p_released:
            payments_principal = principal_released
            payments_interest = p_i_released - principal_released
            payments_fees = p_i_f_released - p_i_released
            payments_penalty = p_i_f_p_released - amount_paid
        elif amount_paid > p_i_f_p_released:
            payments_principal = principal_released
            payments_interest = p_i_released - principal_released
            payments_fees = p_i_f_released - p_i_released
            payments_penalty = p_i_f_p_released - p_i_f_released
        else:
            pass 
        payments_total = payments_principal + payments_interest + payments_fees + payments_penalty
        data = {
        'borrower': borrower,
        'no_loan_released': no_loan_released,
        'principal_released': principal_released,
        'principal_at_risk' : principal_at_risk,
        'due_loans_principal' : due_loans_principal,
        'due_loans_interest' : due_loans_interest,
        'due_loans_fees' : due_loans_fees,
        'due_loans_penalty' : due_loans_penalty,
        'due_loans_total' : due_loans_total,
        'payments_principal': payments_principal,
        'payments_interest' : payments_interest,
        'payments_fees': payments_fees,
        'payments_penalty': payments_penalty,
        'payments_total': payments_total
        }
        serializer = LoanBorrowerReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportsBetween(APIView):
    def get(self, request, pk=None):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        filtered_reports = LoanBorrowerReport.objects.filter(date__gt = start_date).filter(date__lt = end_date)
        serializer = LoanBorrowerReportSerializer(filtered_reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)