from django.shortcuts import render
import datetime
import calendar
import math
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Q
#from fine_search.fine_search import perform_search_queryset
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
from staffs.models import Payroll
from loans.models import Loan, LoanScheduler, LoanOfficer, LoanDisbursement, LoanFee, LoanRepayment,\
    OfficerLoan
from borrowers.models import Borrower
from accounts.models import Branch
from decimal import Decimal
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

# class BorrowersReport(APIView):
#     def post(self, request, pk=None):
       
#         borrower = request.data.get('borrower')
#         borrower_instance = Borrower.objects.get(pk = int(borrower))
#         loans_released = Loan.objects.filter(borrower = borrower_instance).exclude(status = "processing").exclude(status = "denied")
#         due_loans = Loan.objects.filter(status = "past maturity").filter(borrower = borrower_instance)
#         no_loan_released = len(loans_released)
#         principal_released = 0
#         amount_paid = 0
#         due_loans_principal = 0
#         due_loans_interest = 0
#         due_loans_fees = 0
#         due_loans_penalty = 0
#         due_loans_total = 0
#         payments_principal = 0
#         payments_interest = 0
#         payments_fees = 0
#         payments_penalty = 0
#         p_i_released = 0
#         p_i_f_released = 0
#         p_i_f_p_released = 0
#         #try except to avoid breaking for people without loans released
#         # try:
#         for each_loan_released in loans_released:
#             principal_released += each_loan_released.principal_amount
#             p_i_released += (each_loan_released.principal_amount + each_loan_released.interest)
#             p_i_f_released += (each_loan_released.principal_amount + each_loan_released.interest + each_loan_released.loan_fees)
#             p_i_f_p_released += (each_loan_released.principal_amount + each_loan_released.interest + each_loan_released.loan_fees + each_loan_released.penalty_amount)
#             amount_paid += each_loan_released.amount_paid
            
#         # except:
#         #     pass
#         principal_at_risk = principal_released - amount_paid
#         #where amount paid is higher than principal released
#         if principal_at_risk < 0.00:
#             principal_at_risk = 0.00
#         # try:
#         for each_due_loan in due_loans:
#             due_loans_principal += each_due_loan.principal_amount
#             due_loans_interest += each_due_loan.interest
#             due_loans_fees += each_due_loan.loan_fees
#             due_loans_penalty += each_due_loan.penalty_amount
#             due_loans_total = due_loans_principal + due_loans_interest + due_loans_fees + due_loans_penalty
#         # except:
#         #     pass
#         if amount_paid < principal_released:
#             payments_principal = principal_released - amount_paid
#             #payments interest, fees and penalties retain values of 0.00
#         elif amount_paid > principal_released and amount_paid < p_i_released:
#             payments_principal = principal_released
#             payments_interest = p_i_released - amount_paid
#         elif amount_paid > p_i_released and amount_paid < p_i_f_released:
#             payments_principal = principal_released
#             payments_interest = p_i_released - principal_released
#             payments_fees = p_i_f_released - amount_paid
#         elif amount_paid > p_i_f_released and amount_paid < p_i_f_p_released:
#             payments_principal = principal_released
#             payments_interest = p_i_released - principal_released
#             payments_fees = p_i_f_released - p_i_released
#             payments_penalty = p_i_f_p_released - amount_paid
#         elif amount_paid > p_i_f_p_released:
#             payments_principal = principal_released
#             payments_interest = p_i_released - principal_released
#             payments_fees = p_i_f_released - p_i_released
#             payments_penalty = p_i_f_p_released - p_i_f_released
#         else:
#             pass 
#         payments_total = payments_principal + payments_interest + payments_fees + payments_penalty
#         data = {
#         'borrower': borrower,
#         'no_loan_released': no_loan_released,
#         'principal_released': principal_released,
#         'principal_at_risk' : principal_at_risk,
#         'due_loans_principal' : due_loans_principal,
#         'due_loans_interest' : due_loans_interest,
#         'due_loans_fees' : due_loans_fees,
#         'due_loans_penalty' : due_loans_penalty,
#         'due_loans_total' : due_loans_total,
#         'payments_principal': payments_principal,
#         'payments_interest' : payments_interest,
#         'payments_fees': payments_fees,
#         'payments_penalty': payments_penalty,
#         'payments_total': payments_total
#         }
#         serializer = LoanBorrowerReportSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)    
    
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanReport(APIView):
    def get(self, request, pk=None):
        loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
        #print(loans_released)
        data = []
        for each_loan_released in loans_released:
            borrower = each_loan_released.borrower
            name = borrower.first_name + ' ' + str(borrower.last_name)
            loan_type = each_loan_released.loan_type
            principal_released = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid = float(each_loan_released.amount_paid)
            payments_interest = 0
            payments_fees = 0
            payments_penalty = 0
            for each_loan_schedule in loan_schedule:
                payments_interest += each_loan_schedule.interest
                payments_fees += each_loan_schedule.fees
                payments_penalty += each_loan_schedule.penalty
            payments_principal = Decimal(amount_paid) - Decimal(payments_interest) - Decimal(payments_fees) - Decimal(payments_penalty)
            if payments_principal < 0:
                payments_principal = 0 
            principal_at_risk = Decimal(principal_released) - Decimal(payments_principal)
            principal_at_risk = math.ceil(principal_at_risk)
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan = 0
            interest_due_loan = 0
            fees_due_loan = 0
            penalty_due_loan = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan += each_due_loan_schedule.principal
                interest_due_loan += each_due_loan_schedule.interest
                fees_due_loan += each_due_loan_schedule.fees
                penalty_due_loan += each_due_loan_schedule.penalty
            total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
            datas = {
                "borrower": name,
                "loan": each_loan_released.account_no,
                "loan_type": loan_type.name,
                "principal_released": principal_released,
                "principal_at_risk": principal_at_risk,
                "due_loans_principal": principal_due_loan,
                "due_loans_interest": interest_due_loan,
                "due_loans_fees": fees_due_loan,
                "due_loans_penalty": penalty_due_loan,
                "due_loans_total": total_due_loan,
                "payments_principal":payments_principal,
                "payments_interest":payments_interest,
                "payments_fees":payments_fees,
                "payments_penalty":payments_penalty,
                "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
            }
            data.append(datas)
        return Response(data, status=status.HTTP_200_OK)
        # for each_loan_released in loans_released:
        #     borrower = each_loan_released.borrower
        #     principal_released = float(each_loan_released.principal_amount)
        #     #maturity_date__lte = datetime.date.today()
        #     loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
        #     amount_paid = float(each_loan_released.amount_paid)
        #     payments_interest = 0
        #     payments_fees = 0
            
        #     #print("name", loans_released)
        #     #print(each_loan_released.loan.account_no)
        #     payments_penalty = 0
        #     for each_loan_schedule in loan_schedule:
        #         payments_interest += each_loan_schedule.interest
        #         payments_fees += each_loan_schedule.fees
        #         payments_penalty += each_loan_schedule.penalty
        #     payments_principal = Decimal(amount_paid) - payments_interest - payments_fees - payments_penalty
        #     if payments_principal < 0:
        #         payments_principal = 0 
        #     principal_at_risk = Decimal(principal_released) - payments_principal 
        #     due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
        #     principal_due_loan = 0
        #     interest_due_loan = 0
        #     fees_due_loan = 0
        #     penalty_due_loan = 0
        #     #loans_released = 0
        #     for each_due_loan_schedule in due_loan_schedules:
        #         principal_due_loan += each_due_loan_schedule.principal
        #         interest_due_loan += each_due_loan_schedule.interest
        #         fees_due_loan += each_due_loan_schedule.fees
        #         penalty_due_loan += each_due_loan_schedule.penalty
        #     total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
        #     datas = {
                
        #         "loans_released": loans_released.account_no,
        #         "borrower": borrower.pk,
        #         "principal_released": principal_released,
        #         "principal_at_risk": principal_at_risk,
        #         "due_loans_principal": principal_due_loan,
        #         "due_loans_interest": interest_due_loan,
        #         "due_loans_fees": fees_due_loan,
        #         "due_loans_penalty": penalty_due_loan,
        #         "due_loans_total": total_due_loan,
        #         "payments_principal":payments_principal,
        #         "payments_interest":payments_interest,
        #         "payments_fees":payments_fees,
        #         "payments_penalty":payments_penalty,
        #         "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
        #     }
        #     data.append(datas)
        #     #root.append(each_loan_released)
        #     #serializer = LoanBorrowerReportSerializer(data=data)
        #     #if serializer.is_valid():
        #     #    serializer.save()
        #     #    root.append({each_loan_released.pk : serializer.data})
        # return Response(data, status=status.HTTP_200_OK) 




class BorrowersReport(APIView):
    def get(self, request, pk=None):
        loans_released = Loan.objects.exclude(status = "denied")
        all_borrowers = Borrower.objects.all()
        rez = []
        borrowers = []
        data = []
        principal_released = 0
        principal_amount = 0
        interest_due_loan = 0
        fees_due_loan = 0
        penalty_due_loan = 0
        payments_principal = 0
        payments_interest = 0
        payments_fees = 0
        payments_penalty = 0
        amount_paid = 0
        names = []
        for borrower in all_borrowers:
            name = borrower.first_name + ' ' + borrower.last_name
            borrower_name = {
                'name': name
            }
            names.append(borrower_name)
            all_loans = Loan.objects.filter(borrower=borrower).exclude(status="denied")
            due_loans = Loan.objects.filter(borrower=borrower, loan_release_date__lte = datetime.date.today()).exclude(status="denied")
            for loan in all_loans:
                loan_schedule = LoanScheduler.objects.filter(loan=loan).filter(paid__gt = 0)
                principal_released += loan.principal_amount
                amount_paid += loan.amount_paid
                penalty_due_loan += (loan.penalty_rate/100)* Decimal(loan.principal_amount)
                for schedule in loan_schedule:
                    payments_principal += schedule.principal
                    payments_interest += schedule.interest
                    payments_fees += schedule.fees
                    payments_penalty += schedule.penalty
                payments_principal = Decimal(amount_paid) - Decimal(payments_interest) - Decimal(payments_fees) - Decimal(payments_penalty)
                principal_at_risk = Decimal(principal_released) - Decimal(payments_principal)
                principal_at_risk = math.ceil(principal_at_risk)
            for due_loan in due_loans:
                principal_amount += due_loan.principal_amount
                interest_due_loan += due_loan.interest
                for due_loan_fee in due_loan.loan_fees.all():
                    fees_due_loan += (due_loan_fee.percentage/100)* Decimal(due_loan.principal_amount)
            total_due_loan = penalty_due_loan + fees_due_loan + Decimal(principal_amount) + interest_due_loan
            loans1 = {
                'name': name,
                "number_of_loans": len(all_loans),
                "principal_released": principal_released,
                "principal_at_risk": principal_at_risk,
                "due_loans_principal": principal_amount,
                "due_loans_interest": interest_due_loan,
                "due_loans_fees": fees_due_loan, "due_loans_penalty": penalty_due_loan,
                "due_loans_total": total_due_loan,
                "payments_principal": math.ceil(payments_principal),
                "payments_interest": payments_interest,
                "payments_fees": payments_fees,
                "payments_penalty": payments_penalty,
                "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
            }
            data.append(loans1)
        return Response(data, status=status.HTTP_200_OK)


# class BorrowersReport(APIView):
#     def get(self, request, pk=None):
#         loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
#         rez = []
#         borrowers = []
#         new_rez = []
#         for each_loan_released in loans_released:
#             borrower = each_loan_released.borrower
#             print("borrower name",borrower.first_name)
#             principal_released = float(each_loan_released.principal_amount)
#             #maturity_date__lte = datetime.date.today()
#             loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
#             amount_paid = float(each_loan_released.amount_paid)
#             payments_interest = 0
#             payments_fees = 0
#             payments_penalty = 0
#             for each_loan_schedule in loan_schedule:
#                 payments_interest += each_loan_schedule.interest
#                 payments_fees += each_loan_schedule.fees
#                 payments_penalty += each_loan_schedule.penalty
#             payments_principal = Decimal(amount_paid) - payments_interest - payments_fees - payments_penalty
#             if payments_principal < 0:
#                 payments_principal = 0 
#             principal_at_risk = Decimal(principal_released) - payments_principal 
#             due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
#             principal_due_loan = 0
#             interest_due_loan = 0
#             fees_due_loan = 0
            
#             penalty_due_loan = 0
#             for each_due_loan_schedule in due_loan_schedules:
#                 principal_due_loan += each_due_loan_schedule.principal
#                 interest_due_loan += each_due_loan_schedule.interest
#                 fees_due_loan += each_due_loan_schedule.fees
#                 penalty_due_loan += each_due_loan_schedule.penalty
#             total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
#             data = {
#                 "borrowers_name" : borrower.first_name,
#                 "borrower": borrower.pk,
#                 "principal_released": principal_released,
#                 "principal_at_risk": principal_at_risk,
#                 "due_loans_principal": principal_due_loan,
#                 "due_loans_interest": interest_due_loan,
#                 "due_loans_fees": fees_due_loan,
#                 "due_loans_penalty": penalty_due_loan,
#                 "due_loans_total": total_due_loan,
#                 "payments_principal":payments_principal,
#                 "payments_interest":payments_interest,
#                 "payments_fees":payments_fees,
#                 "payments_penalty":payments_penalty,
#                 "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
#             }
#             serializer = LoanBorrowerReportSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 rez.append(serializer.data)
#                 #print(serializer.data) 
#                 borrowers.append(borrower.first_name)
#                 borrowers.append(borrower.pk)
#         borrowers = (list(set(borrowers)))
#         for each_rez in rez:
#             if each_rez['borrower'] in borrowers:
#                 new_rez.append(each_rez)
#                 new_rez[0]["borroowers_name"] = borrower.first_name
#                 borrowers.remove(each_rez['borrower'])
#             else:
#                 for each_new_rez in new_rez:
#                     if each_new_rez['borrower'] == each_rez['borrower']:
#                         each_new_rez["borrowers_name"] = (each_rez["borrowers_name"])
#                         each_new_rez["principal_released"] = str(float(each_rez["principal_released"])+ float(each_new_rez["principal_released"]))
#                         each_new_rez["principal_at_risk"] = str(float(each_rez["principal_at_risk"]) + float(each_new_rez["principal_at_risk"]))
#                         each_new_rez["due_loans_principal"] = str(float(each_rez["due_loans_principal"]) + float(each_new_rez["due_loans_principal"]))
#                         each_new_rez["due_loans_interest"] = str(float(each_rez["due_loans_interest"]) + float(each_new_rez["due_loans_interest"]))
#                         each_new_rez["due_loans_fees"] = str(float(each_rez["due_loans_fees"]) + float(each_new_rez["due_loans_fees"]))
#                         each_new_rez["due_loans_penalty"] = str(float(each_rez["due_loans_penalty"]) + float(each_new_rez["due_loans_penalty"]))
#                         each_new_rez["due_loans_total"] = str(float(each_rez["due_loans_total"]) + float(each_new_rez["due_loans_total"]))
#                         each_new_rez["payments_principal"] = str(float(each_rez["payments_principal"]) + float(each_new_rez["payments_principal"]))
#                         each_new_rez["payments_interest"] = str(float(each_rez["payments_interest"]) + float(each_new_rez["payments_interest"]))
#                         each_new_rez["payments_fees"] = str(float(each_rez["payments_fees"]) + float(each_new_rez["payments_fees"]))
#                         each_new_rez["payments_penalty"] = str(float(each_rez["payments_penalty"]) + float(each_new_rez["payments_penalty"]))
#                         each_new_rez["payments_total"] = str(float(each_rez["payments_total"]) + float(each_new_rez["payments_total"]))
#         return Response(new_rez, status=status.HTTP_200_OK) 

class LoanOfficerReport(APIView):
    def get(self, request):
        staff = request.GET.get('staff')
        # Get Loan Loan Officers
        check_officer = LoanOfficer.objects.filter(id=staff).exists()
        if check_officer == False:
            return Response({"error": "staff does not exist"}, status=status.HTTP_404_NOT_FOUND)
        officers = LoanOfficer.objects.get(id=staff)
        officer_branch = officers.staff_id.user_id.branch.name
        name = officers.staff_id.user_id.user.first_name + ' ' + officers.staff_id.user_id.user.last_name
        ####
        get_officer = OfficerLoan.objects.filter(loan_officer=officers)
        ### Get all loan inside get_officer
        total_loans = 0
        total_principal = 0
        total_interest = 0
        total_fees = 0
        total_penalty = 0
        principal_released = 0
        paid = 0
        principal_due_loan = 0
        interest_due_loan = 0
        fees_due_loan = 0
        penalty_due_loan = 0
        principal_at_risk = 0
        total_due_loan = 0
        total = 0
        payments_principal = 0
        for officer in get_officer:
            loans = Loan.objects.filter(id=officer.loan.id).exclude(status='denied')
            ### get_loan_details
            total_loans += len(loans)
            for loan in loans:
                principal_released += loan.principal_amount
                get_schedule = LoanScheduler.objects.filter(loan=loan, status='settled').filter(paid__gt=0)
            for schedule in get_schedule:
                get_principal = schedule.principal
                total_principal += get_principal
                total_interest += schedule.interest
                total_fees += schedule.fees
                total_penalty += schedule.penalty
                paid += schedule.paid
            total = total_penalty + total_fees + total_interest + total_principal
            payments_principal = Decimal(paid) - Decimal(total_interest) - Decimal(total_fees) - Decimal(total_penalty)
            if payments_principal <= 0:
                payments_principal = 0
            principal_at_risk = Decimal(principal_released) - Decimal(payments_principal)
            due_loan_schedules = LoanScheduler.objects.filter(loan=loan, date__lte = datetime.date.today())
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan += each_due_loan_schedule.principal
                interest_due_loan += each_due_loan_schedule.interest
                fees_due_loan += each_due_loan_schedule.fees
                penalty_due_loan += each_due_loan_schedule.penalty
            total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan

        
        data = {
            "loans": total_loans,
            "loan_type": loan.loan_type.name,
            "principal_released": principal_released,
            "principal_at_risk": principal_at_risk,
            "due_loans_principal": principal_due_loan,
            "due_loans_interest": interest_due_loan,
            "due_loans_fees": fees_due_loan,
            "due_loans_penalty": penalty_due_loan,
            "due_loans_total": total_due_loan,
            "payments_principal": payments_principal,
            "payments_interest": total_interest,
            "payments_fees": total_fees,
            "payments_penalty": total_penalty,
            "payments_total": total,
            'branch': officer_branch,
            'name': name
        }
        # root = dict.fromkeys(staffs, data)
        return Response(data)

# class LoanOfficerReport(APIView):
#     def get(self, request, pk=None):
#         loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
#         #print(loans_released)
#         root = []
#         total_output = []
#         for each_loan_released in loans_released:
#             borrower = each_loan_released.borrower
#             principal_released = float(each_loan_released.principal_amount)
#             #maturity_date__lte = datetime.date.today()
#             loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
#             amount_paid = float(each_loan_released.amount_paid)
#             payments_interest = 0
#             payments_fees = 0
#             payments_penalty = 0
#             for each_loan_schedule in loan_schedule:
#                 payments_interest += each_loan_schedule.interest
#                 payments_fees += each_loan_schedule.fees
#                 payments_penalty += each_loan_schedule.penalty
#             payments_principal = amount_paid - payments_interest - payments_fees - payments_penalty
#             if payments_principal < 0:
#                 payments_principal = 0 
#             principal_at_risk = principal_released - payments_principal 
#             due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
#             principal_due_loan = 0
#             interest_due_loan = 0
#             fees_due_loan = 0
#             penalty_due_loan = 0
#             for each_due_loan_schedule in due_loan_schedules:
#                 principal_due_loan += each_due_loan_schedule.principal
#                 interest_due_loan += each_due_loan_schedule.interest
#                 fees_due_loan += each_due_loan_schedule.fees
#                 penalty_due_loan += each_due_loan_schedule.penalty
#             total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
#             data = {
#                 "loan": each_loan_released.pk,
#                 "borrower": borrower.pk,
#                 "principal_released": principal_released,
#                 "principal_at_risk": principal_at_risk,
#                 "due_loans_principal": principal_due_loan,
#                 "due_loans_interest": interest_due_loan,
#                 "due_loans_fees": fees_due_loan,
#                 "due_loans_penalty": penalty_due_loan,
#                 "due_loans_total": total_due_loan,
#                 "payments_principal":payments_principal,
#                 "payments_interest":payments_interest,
#                 "payments_fees":payments_fees,
#                 "payments_penalty":payments_penalty,
#                 "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
#             }
#             return Response (data, status = status.HTTP_200_OK)
        #     root.append(data)
        # loan_officer = LoanOfficer.objects.all()
        # # print(loan_officer)
        # for each_loan_officer in loan_officer:
        #     l_loans = []
        #     each_members = each_loan_officer.members.all()
        #     # print(each_loan_officer)
        #     # print(each_members)
        #     if len(each_members) == 0:
        #         continue
        #     print(each_members)
        #     for e in each_members:
        #         collection = []
        #         l_loans.append(e.pk)
        #     print(l_loans)
        #     for each_l_loan in l_loans:
        #         for each_root in root:
        #             if int(each_root["loan"]) == (each_l_loan):
        #                 collection.append(each_root)
        #     total_output.append({each_loan_officer.name: collection}) 
                    
                    

        # #print(root)
        # return Response(total_output, status = status.HTTP_200_OK) 



class ReportsBetween(APIView):
    def get(self, request, pk=None):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        filtered_reports = LoanBorrowerReport.objects.filter(date__gt = start_date).filter(date__lt = end_date)
        serializer = LoanBorrowerReportSerializer(filtered_reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PortfolioRisk(APIView):
    def get(self, request, pk=None):
        total_loans = Loan.objects.all().count()
        defaulted_loans_thirty = Loan.objects.all().filter(maturity_date__lt = datetime.date.today() - timedelta(days=28)).filter(amount_paid__lte = 0).exclude(status="fully paid").filter(disbursed=True)
        defaulted_loans_sixty = Loan.objects.all().filter(maturity_date__lt = datetime.date.today() - timedelta(days=48)).filter(amount_paid__lte = 0).exclude(status="fully paid").filter(disbursed=True)
        defaulted_loans_ninety = Loan.objects.all().filter(maturity_date__lt = datetime.date.today() - timedelta(days=90)).filter(amount_paid__lte = 0).exclude(status="fully paid").filter(disbursed=True)
        thirty = 0
        sixty = 0
        ninety = 0
        if defaulted_loans_thirty:
            thirty += defaulted_loans_thirty.count()
            thirty = (thirty/total_loans)*100
        else:
            thirty = 0
        if defaulted_loans_sixty:
            sixty += defaulted_loans_sixty.count()
            sixty = (sixty/total_loans)*100
        else:
            sixty = 0
        if defaulted_loans_ninety:
            ninety += defaulted_loans_ninety.count()
            ninety = (ninety/total_loans)*100
        else:
            ninety = 0

        data = {
            'PAR_30': math.ceil(thirty),
            'PAR_60': math.ceil(sixty),
            'PAR_90': math.ceil(ninety),
        }

        return Response({"results": data})


class PortfolioRiskDays(APIView):
    def get(self, request):
        day = request.GET.get('day')
        if day=='' or not day:
            return Response({'invalid': 'invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
        day = int(day)
        total_loans = Loan.objects.all().count()
        defaulted_loans_day = Loan.objects.all().filter(maturity_date__lt = datetime.date.today() - timedelta(days=day)).filter(amount_paid__lte = 0).exclude(status="fully paid").filter(disbursed=True)
        days = 0
        if defaulted_loans_day:
            days += defaulted_loans_day.count()
            days = (days/total_loans)*100
        else:
            days = 0

        data = {
            'PAR_DURATION': math.ceil(days)
        }

        return Response({"results": data})


class LoanArrearsAgingReport(APIView):
    def post(self, request, pk=None):
        first_day = request.data.get("first_day")
        last_day = request.data.get("last_day")
        filtered_loans_released = []
        loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied").filter(maturity_date__lte = datetime.date.today())
        for elr in loans_released:
            if ((datetime.date.today() - filtered_loans[0].maturity_date).days) >= int(first_day) and ((datetime.date.today() - filtered_loans[0].maturity_date).days) < int(last_day):
                filtered_loans_released.append(elr)
        root = []
        for each_loan_released in filtered_loans_released:
            borrower = each_loan_released.borrower
            principal_released = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid = float(each_loan_released.amount_paid)
            payments_interest = 0
            payments_fees = 0
            payments_penalty = 0
            for each_loan_schedule in loan_schedule:
                payments_interest += each_loan_schedule.interest
                payments_fees += each_loan_schedule.fees
                payments_penalty += each_loan_schedule.penalty
            payments_principal = amount_paid - payments_interest - payments_fees - payments_penalty
            if payments_principal < 0:
                payments_principal = 0 
            principal_at_risk = principal_released - payments_principal 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan = 0
            interest_due_loan = 0
            fees_due_loan = 0
            penalty_due_loan = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan += each_due_loan_schedule.principal
                interest_due_loan += each_due_loan_schedule.interest
                fees_due_loan += each_due_loan_schedule.fees
                penalty_due_loan += each_due_loan_schedule.penalty
            total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
            data = {
                "borrower": borrower.pk,
                "principal_released": principal_released,
                "principal_at_risk": principal_at_risk,
                "due_loans_principal": principal_due_loan,
                "due_loans_interest": interest_due_loan,
                "due_loans_fees": fees_due_loan,
                "due_loans_penalty": penalty_due_loan,
                "due_loans_total": total_due_loan,
                "payments_principal":payments_principal,
                "payments_interest":payments_interest,
                "payments_fees":payments_fees,
                "payments_penalty":payments_penalty,
                "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
            }
            serializer = LoanBorrowerReportSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                root.append({each_loan_released.pk : serializer.data})
        return Response(root, status=status.HTTP_201_CREATED) 



class LoanProductReport(APIView):
    def get(self, request, pk=None):
        loans_released = Loan.objects.exclude(status = "denied")
        rez = []
        loan_type = []
        data = []
        for each_loan_released in loans_released:
            borrower = each_loan_released.borrower
            principal_released = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid = float(each_loan_released.amount_paid)
            payments_interest = 0
            payments_fees = 0
            payments_penalty = 0
            for each_loan_schedule in loan_schedule:
                payments_interest += each_loan_schedule.interest
                payments_fees += each_loan_schedule.fees
                payments_penalty += each_loan_schedule.penalty
            payments_principal = Decimal(amount_paid) - Decimal(payments_interest) - Decimal(payments_fees) - Decimal(payments_penalty)
            if payments_principal < 0:
                payments_principal = 0 
            principal_at_risk = Decimal(principal_released) - Decimal(payments_principal)
            principal_at_risk = math.ceil(principal_at_risk)
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan = 0
            interest_due_loan = 0
            fees_due_loan = 0
            penalty_due_loan = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan += each_due_loan_schedule.principal
                interest_due_loan += each_due_loan_schedule.interest
                fees_due_loan += each_due_loan_schedule.fees
                penalty_due_loan += each_due_loan_schedule.penalty
            total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
            datas = {
                "loan_type": each_loan_released.loan_type.name,
                "borrower": borrower.first_name + ' '+ borrower.last_name,
                "principal_released": principal_released,
                "principal_at_risk": principal_at_risk,
                "due_loans_principal": principal_due_loan,
                "due_loans_interest": interest_due_loan,
                "due_loans_fees": fees_due_loan,
                "due_loans_penalty": penalty_due_loan,
                "due_loans_total": total_due_loan,
                "payments_principal":payments_principal,
                "payments_interest":payments_interest,
                "payments_fees":payments_fees,
                "payments_penalty":payments_penalty,
                "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
            }
            data.append(datas)
        return Response(data, status = status.HTTP_200_OK)


# class LoanProductReport(APIView):
#     def get(self, request, pk=None):
#         loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
#         rez = []
#         loan_type = []
#         new_rez = []
#         for each_loan_released in loans_released:
#             borrower = each_loan_released.borrower
#             principal_released = float(each_loan_released.principal_amount)
#             #maturity_date__lte = datetime.date.today()
#             loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
#             amount_paid = float(each_loan_released.amount_paid)
#             payments_interest = 0
#             payments_fees = 0
#             payments_penalty = 0
#             for each_loan_schedule in loan_schedule:
#                 payments_interest += each_loan_schedule.interest
#                 payments_fees += each_loan_schedule.fees
#                 payments_penalty += each_loan_schedule.penalty
#             payments_principal = Decimal(amount_paid) - payments_interest - payments_fees - payments_penalty
#             if payments_principal < 0:
#                 payments_principal = 0 
#             principal_at_risk = Decimal(principal_released) - payments_principal 
#             due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
#             principal_due_loan = 0
#             interest_due_loan = 0
#             fees_due_loan = 0
#             penalty_due_loan = 0
#             for each_due_loan_schedule in due_loan_schedules:
#                 principal_due_loan += each_due_loan_schedule.principal
#                 interest_due_loan += each_due_loan_schedule.interest
#                 fees_due_loan += each_due_loan_schedule.fees
#                 penalty_due_loan += each_due_loan_schedule.penalty
#             total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
#             data = {
#                 "loan_type": each_loan_released.loan_type.name,
#                 "borrower": borrower.pk,
#                 "principal_released": principal_released,
#                 "principal_at_risk": principal_at_risk,
#                 "due_loans_principal": principal_due_loan,
#                 "due_loans_interest": interest_due_loan,
#                 "due_loans_fees": fees_due_loan,
#                 "due_loans_penalty": penalty_due_loan,
#                 "due_loans_total": total_due_loan,
#                 "payments_principal":payments_principal,
#                 "payments_interest":payments_interest,
#                 "payments_fees":payments_fees,
#                 "payments_penalty":payments_penalty,
#                 "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
#             }
#             serializer = LoanBorrowerReportSerializer(data=data)
#             if serializer.is_valid():
#                 #serializer.save()
#                 rez.append(serializer.data)
#             #rez.append(data)
#             loan_type.append(each_loan_released.loan_type.name)
#         loan_type = (list(set(loan_type)))
#         # print(rez)
#         # print(loan_type)
#         # print(new_rez)
#         n_rez = []
#         for each_rez in rez:
#             print("le") 
#             outputs = []
#             if each_rez['loan_type'] in loan_type:
#                 outputs.append(each_rez)
#             n_rez.append(outputs)
#         new_rez.append({each_rez['loan_type']:n_rez})
#             #     new_rez.append(each_rez)
#             #     #loan_type.remove(each_rez['loan_type'])
#             # else:
#             #     for each_new_rez in new_rez:
#             #         if each_new_rez['loan_type'] == each_rez['loan_type']:
#             #             new_rez.append(each_new_rez)

#         # print(new_rez)
#         # return Response(new_rez, status = status.HTTP_200_OK) 
#         return Response(new_rez, status = status.HTTP_200_OK) 


class CollectionReport(APIView):
    def get(self, request, pk=None):
        root = []
        loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
        print(loans_released)
        for each_loan_released in loans_released:
            principal_released = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid = float(each_loan_released.amount_paid)
            payments_interest = 0
            payments_fees = 0
            payments_penalty = 0
            for each_loan_schedule in loan_schedule:
                payments_interest += each_loan_schedule.interest
                payments_fees += each_loan_schedule.fees
                payments_penalty += each_loan_schedule.penalty
            payments_principal = amount_paid - payments_interest - payments_fees - payments_penalty
            if payments_principal < 0:
                payments_principal = 0 
            principal_at_risk = principal_released - payments_principal 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan = 0
            interest_due_loan = 0
            fees_due_loan = 0
            penalty_due_loan = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan += each_due_loan_schedule.principal
                interest_due_loan += each_due_loan_schedule.interest
                fees_due_loan += each_due_loan_schedule.fees
                penalty_due_loan += each_due_loan_schedule.penalty
            total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
            principal_due_loan += principal_due_loan
            interest_due_loan += interest_due_loan
            fees_due_loan += fees_due_loan
            penalty_due_loan += penalty_due_loan
            total_due_loan += total_due_loan
            payments_principal += payments_principal
            payments_interest += payments_interest
            payments_fees += payments_fees
            payments_penalty += payments_penalty
        data1 = {
            "gross_due_principal": principal_due_loan,
            "gross_due_interest": interest_due_loan,
            "gross_due_fees": fees_due_loan,
            "gross_due_penalty": penalty_due_loan,
            "gross_due_total": total_due_loan,
            "paid_principal":payments_principal,
            "paid_interest":payments_interest,
            "paid_fees":payments_fees,
            "paid_penalty":payments_penalty,
            "paid_total": payments_principal + payments_interest + payments_fees + payments_penalty
        }
        root.append({"Open Loans": data1})
            # serializer = LoanBorrowerReportSerializer(data=data)
            # if serializer.is_valid():
            #     serializer.save()
        #root.append(serializer.data)

        loans_released = Loan.objects.filter(status="missed repayment")
        print(loans_released)
        principal_due_loan2, interest_due_loan2, fees_due_loan2, penalty_due_loan2, total_due_loan2, payments_principal2, payments_interest2,\
        payments_fees2, payments_penalty2 =  0, 0, 0,0,0,0,0,0,0
        for each_loan_released in loans_released:
            principal_released2 = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid2 = float(each_loan_released.amount_paid)
            payments_interest2 = 0
            payments_fees2 = 0
            payments_penalty2 = 0
            for each_loan_schedule in loan_schedule:
                payments_interest2 += each_loan_schedule.interest
                payments_fees2 += each_loan_schedule.fees
                payments_penalty2 += each_loan_schedule.penalty
            payments_principal2 = amount_paid2 - payments_interest2 - payments_fees2 - payments_penalty2
            if payments_principal2 < 0:
                payments_principal2 = 0 
            principal_at_risk2 = principal_released2 - payments_principal2 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan2 = 0
            interest_due_loan2 = 0
            fees_due_loan2 = 0
            penalty_due_loan2 = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan2 += each_due_loan_schedule.principal
                interest_due_loan2 += each_due_loan_schedule.interest
                fees_due_loan2 += each_due_loan_schedule.fees
                penalty_due_loan2 += each_due_loan_schedule.penalty
            total_due_loan2 = principal_due_loan2 + interest_due_loan2 + fees_due_loan2 + penalty_due_loan2
            principal_due_loan2 += principal_due_loan2
            interest_due_loan2 += interest_due_loan2
            fees_due_loan2 += fees_due_loan2
            penalty_due_loan2 += penalty_due_loan2
            total_due_loan2 += total_due_loan2
            payments_principal2 += payments_principal2
            payments_interest2 += payments_interest2
            payments_fees2 += payments_fees2
            payments_penalty2 += payments_penalty2
        data2 = {
            "gross_due_principal": principal_due_loan2,
            "gross_due_interest": interest_due_loan2,
            "gross_due_fees": fees_due_loan2,
            "gross_due_penalty": penalty_due_loan2,
            "gross_due_total": total_due_loan2,
            "paid_principal":payments_principal2,
            "paid_interest":payments_interest2,
            "paid_fees":payments_fees2,
            "paid_penalty":payments_penalty2,
            "paid_total": payments_principal2 + payments_interest2 + payments_fees2 + payments_penalty2
        }
        root.append({"Missed Repayment": data2})

        loans_released = Loan.objects.filter(status="past maturity")
        print(loans_released)
        principal_due_loan3, interest_due_loan3, fees_due_loan3, penalty_due_loan3, total_due_loan3, payments_principal3, payments_interest3,\
        payments_fees3, payments_penalty3 =  0, 0, 0,0,0,0,0,0,0
        for each_loan_released in loans_released:
            principal_released3 = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid3 = float(each_loan_released.amount_paid)
            payments_interest3 = 0
            payments_fees3 = 0
            payments_penalty3 = 0
            for each_loan_schedule in loan_schedule:
                payments_interest3 += each_loan_schedule.interest
                payments_fees3 += each_loan_schedule.fees
                payments_penalty3 += each_loan_schedule.penalty
            payments_principal3 = amount_paid3 - payments_interest3 - payments_fees3 - payments_penalty3
            if payments_principal3 < 0:
                payments_principal3 = 0 
            principal_at_risk3 = principal_released3 - payments_principal3 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan3 = 0
            interest_due_loan3 = 0
            fees_due_loan3 = 0
            penalty_due_loan3 = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan3 += each_due_loan_schedule.principal
                interest_due_loan3 += each_due_loan_schedule.interest
                fees_due_loan3 += each_due_loan_schedule.fees
                penalty_due_loan3 += each_due_loan_schedule.penalty
            total_due_loan3 = principal_due_loan3 + interest_due_loan3 + fees_due_loan3 + penalty_due_loan3
            principal_due_loan3 += principal_due_loan3
            interest_due_loan3 += interest_due_loan3
            fees_due_loan3 += fees_due_loan3
            penalty_due_loan3 += penalty_due_loan3
            total_due_loan3 += total_due_loan3
            payments_principal3 += payments_principal3
            payments_interest3 += payments_interest3
            payments_fees3 += payments_fees3
            payments_penalty3 += payments_penalty3
        data3 = {
            "gross_due_principal": principal_due_loan3,
            "gross_due_interest": interest_due_loan3,
            "gross_due_fees": fees_due_loan3,
            "gross_due_penalty": penalty_due_loan3,
            "gross_due_total": total_due_loan3,
            "paid_principal":payments_principal3,
            "paid_interest":payments_interest3,
            "paid_fees":payments_fees3,
            "paid_penalty":payments_penalty3,
            "paid_total": payments_principal3 + payments_interest3 + payments_fees3 + payments_penalty3
        }
        root.append({"Past Maturity": data3})

        loans_released = Loan.objects.filter(status="fully paid")
        print(loans_released)
        principal_due_loan4, interest_due_loan4, fees_due_loan4, penalty_due_loan4, total_due_loan4, payments_principal4, payments_interest4,\
        payments_fees4, payments_penalty4 =  0, 0, 0,0,0,0,0,0,0
        for each_loan_released in loans_released:
            principal_released4 = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid4 = float(each_loan_released.amount_paid)
            payments_interest4 = 0
            payments_fees4 = 0
            payments_penalty4 = 0
            for each_loan_schedule in loan_schedule:
                payments_interest4 += each_loan_schedule.interest
                payments_fees4 += each_loan_schedule.fees
                payments_penalty4 += each_loan_schedule.penalty
            payments_principal4 = amount_paid4 - payments_interest4 - payments_fees4 - payments_penalty4
            if payments_principal4 < 0:
                payments_principal4 = 0 
            principal_at_risk4 = principal_released4 - payments_principal4 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan4 = 0
            interest_due_loan4 = 0
            fees_due_loan4 = 0
            penalty_due_loan4 = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan4 += each_due_loan_schedule.principal
                interest_due_loan4 += each_due_loan_schedule.interest
                fees_due_loan4 += each_due_loan_schedule.fees
                penalty_due_loan4 += each_due_loan_schedule.penalty
            total_due_loan4 = principal_due_loan4 + interest_due_loan4 + fees_due_loan4 + penalty_due_loan4
            principal_due_loan4 += principal_due_loan4
            interest_due_loan4 += interest_due_loan4
            fees_due_loan4 += fees_due_loan4
            penalty_due_loan4 += penalty_due_loan4
            total_due_loan4 += total_due_loan4
            payments_principal4 += payments_principal4
            payments_interest4 += payments_interest4
            payments_fees4 += payments_fees4
            payments_penalty4 += payments_penalty4
        data4 = {
            "gross_due_principal": principal_due_loan4,
            "gross_due_interest": interest_due_loan4,
            "gross_due_fees": fees_due_loan4,
            "gross_due_penalty": penalty_due_loan4,
            "gross_due_total": total_due_loan4,
            "paid_principal":payments_principal4,
            "paid_interest":payments_interest4,
            "paid_fees":payments_fees4,
            "paid_penalty":payments_penalty4,
            "paid_total": payments_principal4 + payments_interest4 + payments_fees4 + payments_penalty4
        }
        root.append({"Fully Paid": data4})

        loans_released = Loan.objects.filter(status="restructed")
        print(loans_released)
        principal_due_loan5, interest_due_loan5, fees_due_loan5, penalty_due_loan5, total_due_loan5, payments_principal5, payments_interest5,\
        payments_fees5, payments_penalty5 =  0, 0, 0,0,0,0,0,0,0
        for each_loan_released in loans_released:

            principal_released5 = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid5 = float(each_loan_released.amount_paid)
            payments_interest5 = 0
            payments_fees5 = 0
            payments_penalty5 = 0
            for each_loan_schedule in loan_schedule:
                payments_interest5 += each_loan_schedule.interest
                payments_fees5 += each_loan_schedule.fees
                payments_penalty5 += each_loan_schedule.penalty
            payments_principal5 = amount_paid5 - payments_interest5 - payments_fees5 - payments_penalty5
            if payments_principal5 < 0:
                payments_principal5 = 0 
            principal_at_risk5 = principal_released5 - payments_principal5 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan5 = 0
            interest_due_loan5 = 0
            fees_due_loan5 = 0
            penalty_due_loan5 = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan5 += each_due_loan_schedule.principal
                interest_due_loan5 += each_due_loan_schedule.interest
                fees_due_loan5 += each_due_loan_schedule.fees
                penalty_due_loan5 += each_due_loan_schedule.penalty
            total_due_loan5 = principal_due_loan5 + interest_due_loan5 + fees_due_loan5 + penalty_due_loan5
            principal_due_loan5 += principal_due_loan5
            interest_due_loan5 += interest_due_loan5
            fees_due_loan5 += fees_due_loan5
            penalty_due_loan5 += penalty_due_loan5
            total_due_loan5 += total_due_loan5
            payments_principal5 += payments_principal5
            payments_interest5 += payments_interest5
            payments_fees5 += payments_fees5
            payments_penalty5 += payments_penalty5
        data5 = {
            "gross_due_principal": principal_due_loan5,
            "gross_due_interest": interest_due_loan5,
            "gross_due_fees": fees_due_loan5,
            "gross_due_penalty": penalty_due_loan5,
            "gross_due_total": total_due_loan5,
            "paid_principal":payments_principal5,
            "paid_interest":payments_interest5,
            "paid_fees":payments_fees5,
            "paid_penalty":payments_penalty5,
            "paid_total": payments_principal5 + payments_interest5 + payments_fees5 + payments_penalty5
        }
        root.append({"Restructured": data5})
        return Response(root, status=status.HTTP_200_OK) 

class CollectorReportStaff(APIView):
    def get(self, request):
        staff = request.GET.get('staff')
        # Get Loan Loan Officers
        check_officer = LoanOfficer.objects.filter(id=staff).exists()
        if check_officer == False:
            return Response({"error": "Staff does not exists with such staff"}, status=status.HTTP_404_NOT_FOUND)
        officers = LoanOfficer.objects.get(id=staff)
        officer_branch = officers.staff_id.user_id.branch.name
        name = officers.staff_id.user_id.user.first_name + ' ' + officers.staff_id.user_id.user.last_name
        ####
        get_officer = OfficerLoan.objects.filter(loan_officer=officers)
        ### Get all loan inside get_officer
        total_loans = 0
        total_principal = 0
        total_interest = 0
        total_fees = 0
        total_penalty = 0
        total = 0
        for officer in get_officer:
            loans = Loan.objects.filter(id=officer.loan.id).exclude(status='denied')
            ### get_loan_details
            total_loans += len(loans)
            for loan in loans:
                get_schedule = LoanScheduler.objects.filter(loan=loan.id, status='settled').filter(paid__gt=0)
            for schedule in get_schedule:
                get_principal = schedule.principal
                total_principal += get_principal
                total_interest += schedule.interest
                total_fees += schedule.fees
                total_penalty += schedule.penalty
            total = total_penalty + total_fees + total_interest + total_principal

        
        data = {
            'total_loans': total_loans,
            'total_principal': total_principal,
            'total_interest': total_interest,
            'total_fees': total_fees,
            'total_penalty': total_penalty,
            'total': total,
            'branch': officer_branch,
            'name': name
        }
        # root = dict.fromkeys(staffs, data)
        return Response(data)


# class CollectorReportStaff(APIView):
#     def get(self, request):
#         staff = request.GET.get('staff')
#         # Get Loan Loan Officers
#         check_officer = LoanOfficer.objects.filter(id=staff).exists()
#         if check_officer == False:
#             return Response({"error": "staff does not exist"}, status=status.HTTP_404_NOT_FOUND)
#         officers = LoanOfficer.objects.get(id=staff)
#         officer_branch = officers.staff_id.user_id.branch.name
#         name = officers.staff_id.user_id.user.first_name + ' ' + officers.staff_id.user_id.user.last_name
#         ####
#         get_officer = OfficerLoan.objects.filter(loan_officer=officers)
#         ### Get all loan inside get_officer
#         total_loans = 0
#         total_principal = 0
#         total_interest = 0
#         total_fees = 0
#         total_penalty = 0
#         total = 0
#         for officer in get_officer:
#             loans = Loan.objects.filter(id=officer.loan.id).exclude(status='denied')
#             ### get_loan_details
#             total_loans += len(loans)
#             for loan in loans:
#                 get_schedule = LoanScheduler.objects.filter(loan=loan.id, status='settled').filter(paid__gt=0)
#             for schedule in get_schedule:
#                 get_principal = schedule.principal
#                 total_principal += get_principal
#                 total_interest += schedule.interest
#                 total_fees += schedule.fees
#                 total_penalty += schedule.penalty
#             total = total_penalty + total_fees + total_interest + total_principal

        
#         data = {
#             'total_loans': total_loans,
#             'total_principal': total_principal,
#             'total_interest': total_interest,
#             'total_fees': total_fees,
#             'total_penalty': total_penalty,
#             'total': total,
#             'branch': officer_branch,
#             'name': name
#         }
#         # root = dict.fromkeys(staffs, data)
#         return Response(data)




# class CollectorReportStaff(APIView):
#     def get(self, request, pk=None):
#         loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
#         #print(loans_released)
#         root = []
#         total_output = []
#         payments_principal = 0
#         total_payments_principal, total_payments_interest, total_payments_fees,\
#         total_payments_penalty = 0,0,0,0
#         root_payments_principal, root_payments_interest, root_payments_fees, root_payments_penalty = 0,0,0,0
#         for each_loan_released in loans_released:
#             borrower = each_loan_released.borrower
#             principal_released = float(each_loan_released.principal_amount)
#             #maturity_date__lte = datetime.date.today()
#             loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
#             amount_paid = float(each_loan_released.amount_paid)
#             payments_interest = 0
#             payments_fees = 0
#             payments_penalty = 0
#             for each_loan_schedule in loan_schedule:
#                 payments_interest += each_loan_schedule.interest
#                 payments_fees += each_loan_schedule.fees
#                 payments_penalty += each_loan_schedule.penalty
#             payments_principal = amount_paid - payments_interest - payments_fees - payments_penalty
#             if payments_principal < 0:
#                 payments_principal = 0 
#             principal_at_risk = principal_released - payments_principal 
#             due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
#             principal_due_loan = 0
#             interest_due_loan = 0
#             fees_due_loan = 0
#             penalty_due_loan = 0
#             for each_due_loan_schedule in due_loan_schedules:
#                 principal_due_loan += each_due_loan_schedule.principal
#                 interest_due_loan += each_due_loan_schedule.interest
#                 fees_due_loan += each_due_loan_schedule.fees
#                 penalty_due_loan += each_due_loan_schedule.penalty
#             total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
#             data = {
#                 "loan": each_loan_released.pk,
#                 "total_principal":payments_principal,
#                 "total_interest":payments_interest,
#                 "total_fees":payments_fees,
#                 "total_penalty":payments_penalty,
#                 "total_collections": payments_principal + payments_interest + payments_fees + payments_penalty
#             }
#             root.append(data)
#             root_payments_principal += payments_principal
#             root_payments_interest += payments_interest
#             root_payments_fees += payments_fees
#             root_payments_penalty += payments_penalty
#             print(payments_principal)
        
#         print(root_payments_principal)
#         total_payments_principal += root_payments_principal
#         total_payments_interest += root_payments_interest
#         total_payments_fees += root_payments_fees
#         total_payments_penalty += root_payments_penalty
#         loan_officer = LoanOfficer.objects.all()
        # print(loan_officer)
        # for each_loan_officer in loan_officer:
        #     l_loans = []
        #     each_members = each_loan_officer.members.all()
        #     # print(each_loan_officer)
        #     # print(each_members)
        #     if len(each_members) == 0:
        #         continue
        #     print(each_members)
        #     for e in each_members:
        #         collection = []
        #         l_loans.append(e.pk)
        #     print(l_loans)
        #     for each_l_loan in l_loans:
        #         for each_root in root:
        #             if int(each_root["loan"]) == (each_l_loan):
        #                 collection.append(each_root)
        #     total_output.append(({each_loan_officer.name: collection}, {"System Generated":{"total_principal":\
        #     total_payments_principal,"total_interest": total_payments_interest,"total_fees": total_payments_fees,\
        #     "total_penalty": total_payments_penalty, "total_collections": (total_payments_principal + total_payments_interest\
        #          + total_payments_fees + total_payments_penalty)}})) 
                    
                    

        # #print(root)
        return Response(total_output, status = status.HTTP_200_OK) 


class DisbursementReport(APIView):
    def get(self, request, pk=None):
        loan_disbursements = LoanDisbursement.objects.all()
        root = []
        for each_loan_released in loan_disbursements:
            data = {
                "disbursed_date": each_loan_released.date_disbursed,
                "borrower": each_loan_released.loan.borrower.first_name +\
                     each_loan_released.loan.borrower.last_name,
                "loan_product":each_loan_released.loan.loan_type.name,
                "loan":each_loan_released.loan.account_no,
                "loan_interest_percentage":each_loan_released.loan.loan_interest_percentage,
                "loan_interest_fixed_amount": each_loan_released.loan.loan_interest_fixed_amount,
                "loan_interest_percentage_period": each_loan_released.loan.loan_interest_percentage_period,
                "duration": each_loan_released.loan.duration,
                "loan_duration_period": each_loan_released.loan.loan_duration_period,
                "disbursed": each_loan_released.disbursed_amount,
                "status": each_loan_released.status,
                "outstanding": each_loan_released.loan.remaining_balance

            }
            root.append(data)
        return Response(root, status = status.HTTP_200_OK)


# class DisbursementReport(APIView):
#     def get(self, request, pk=None):
#         loan_disbursements = LoanDisbursement.objects.all()
#         root = []
#         for each_loan_released in loan_disbursements:
#              data = {
#                 "disbursed_date": each_loan_released.date_disbursed,
#                 "borrower": each_loan_released.loan.borrower.first_name +\
#                      each_loan_released.loan.borrower.last_name,
#                 "loan_product":each_loan_released.loan.loan_type.name,
#                 "loan#":each_loan_released.loan.pk,
#                 "loan_interest_percentage":each_loan_released.loan_interest_percentage,
#                 "loan_interest_fixed_amount": each_loan_released.loan_interest_fixed_amount,
#                 "loan_interest_percentage_period": each_loan_released.loan_interest_percentage_period,
#                 "duration": each_loan_released.duration,
#                 "loan_duration_period": each_loan_released.loan_duration_period,
#                 "disbursed": each_loan_released.disbursed_amount,
#                 "status": each_loan_released.status,
#                 "outstanding": each_loan_released.loan.remaining_balance

#             }
#         root.append(data)
#         return Response(root, status = status.HTTP_200_OK) 


class FeesReport(APIView):
    def get(self, request, pk=None):
        root = []
        net_fees_due = 0
        net_fees_payment = 0
        net_fees_due_res = 0
        net_fees_payment_res = 0
        total_fees_due = 0
        total_fees_payment = 0
        loan_price = 0
        # each_loan_released = []
        loans_released = Loan.objects.all().exclude(status="denied")
        if loans_released:
            for each_loan_released in loans_released:
                if each_loan_released.status == "past maturity":
                    for each_fee in each_loan_released.loan_fees.all():
                        total_fees_due += each_fee.amount
                for each_fee in each_loan_released.loan_fees.all():
                    loan_price += each_fee.amount

            total_loan_fee = 0
            loan_fees = LoanFee.objects.filter(loan=each_loan_released)
            for loan_fee in loan_fees:
                total_loan_fee += float(loan_fee.amount)
                # print(total_loan_fee)
            the_fee = 0.0
            for t_fee in each_loan_released.loan_fees.all():
                the_fee += float(t_fee.amount)
            total_fees_payment += total_loan_fee
            net_fees_due += total_fees_due
            net_fees_payment += loan_price


            loans_released = Loan.objects.filter(status="restructured")
            total_fees_due_res = 0
            total_fees_payment_res = 0
            loan_price_res = 0
            for each_loan_released in loans_released:
                if each_loan_released.status == "past maturity":
                    for each_fee in each_loan_released.loan_fees.all():
                        total_fees_due_res += each_fee.amount
                for each_fee in each_loan_released.loan_fees.all():
                    loan_price_res += each_fee.amount
            total_loan_fee_res = 0
            loan_fees = LoanFee.objects.filter(loan = each_loan_released)
            for loan_fee in loan_fees:
                total_loan_fee_res += loan_fee.amount
            total_fees_payment_res += (total_loan_fee_res)
            net_fees_due_res += total_fees_due
            net_fees_payment_res += total_fees_payment
                # total_fees_payment += 
                 
            data = {
                "all_released_total_fees_due": net_fees_due,
                "all_released_total_fees_payments": net_fees_payment,
                "restructured_total_fees_due": net_fees_due_res,
                "restructured_total_fees_payments": net_fees_payment_res,
            }
            #root.append(data)
        else:
            data = {
                "result": "No data yet"
            }
        return Response(data, status = status.HTTP_200_OK)


# class FeesReport(APIView):
#     def get(self, request, pk=None):
#         root = []
#         net_fees_due = 0
#         net_fees_payment = 0
#         net_fees_due_res = 0
#         net_fees_payment_res = 0
#         loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
#         for each_loan_released in loans_released:
#             total_fees_due = 0
#             total_fees_payment = 0
#             if each_loan_released.status == "passed maturity":
#                 total_fees_due += each_loan_released.loan_fees
#             total_loan_fee = 0
#             loan_fees = LoanFee.objects.filter(loan = each_loan_released)
#             for loan_fee in loan_fees:
#                 total_loan_fee += loan_fee.amount
#             total_fees_payment += (total_loan_fee - each_loan_released.loan_fees)
#             net_fees_due += total_fees_due
#             net_fees_payment += total_fees_payment


#         loans_released = Loan.objects.filter(status = "restructured")
#         for each_loan_released in loans_released:
#             total_fees_due_res = 0
#             total_fees_payment_res = 0
#             if each_loan_released.status == "passed maturity":
#                 total_fees_due_res += each_loan_released.loan_fees
#             total_loan_fee_res = 0
#             loan_fees = LoanFee.objects.filter(loan = each_loan_released)
#             for loan_fee in loan_fees:
#                 total_loan_fee_res += loan_fee.amount
#             total_fees_payment_res += (total_loan_fee_res - each_loan_released.loan_fees)
#             net_fees_due_res += total_fees_due
#             net_fees_payment_res += total_fees_payment
#             # total_fees_payment += 
             
#             data = {
#                 "all_released_total_fees_due": net_fees_due,
#                 "all_released_total_fees_payments": net_fees_payment,
#                 "restructured_total_fees_due": net_fees_due_res,
#                 "restructured_total_fees_payments": net_fees_payment_res,
#             }
#         #root.append(data)
#         return Response(data, status = status.HTTP_200_OK) 



class OutstandingReport(APIView):
    def get(self, request, pk=None):
        c_date = datetime.datetime.strptime(request.GET.get("date"), '%Y-%m-%d')
        loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied").filter(loan_release_date__lte = c_date)
        rez = []
        borrowers = []
        new_rez = []
        for each_loan_released in loans_released:
            borrower = each_loan_released.borrower
            principal_released = float(each_loan_released.principal_amount)
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid = float(each_loan_released.amount_paid)
            payments_interest = 0
            payments_fees = 0
            payments_penalty = 0
            for each_loan_schedule in loan_schedule:
                payments_interest += each_loan_schedule.interest
                payments_fees += each_loan_schedule.fees
                payments_penalty += each_loan_schedule.penalty
            payments_principal = amount_paid - payments_interest - payments_fees - payments_penalty
            if payments_principal < 0:
                payments_principal = 0 
            principal_at_risk = principal_released - payments_principal 
            due_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            principal_due_loan = 0
            interest_due_loan = 0
            fees_due_loan = 0
            penalty_due_loan = 0
            for each_due_loan_schedule in due_loan_schedules:
                principal_due_loan += each_due_loan_schedule.principal
                interest_due_loan += each_due_loan_schedule.interest
                fees_due_loan += each_due_loan_schedule.fees
                penalty_due_loan += each_due_loan_schedule.penalty
            total_due_loan = principal_due_loan + interest_due_loan + fees_due_loan + penalty_due_loan
            data = {
                "borrower": borrower.pk,
                "principal_released": principal_released,
                "principal_at_risk": principal_at_risk,
                "due_loans_principal": principal_due_loan,
                "due_loans_interest": interest_due_loan,
                "due_loans_fees": fees_due_loan,
                "due_loans_penalty": penalty_due_loan,
                "due_loans_total": total_due_loan,
                "payments_principal":payments_principal,
                "payments_interest":payments_interest,
                "payments_fees":payments_fees,
                "payments_penalty":payments_penalty,
                "payments_total": payments_principal + payments_interest + payments_fees + payments_penalty
            }
            serializer = LoanBorrowerReportSerializer(data=data)
            if serializer.is_valid():
                #serializer.save()
                rez.append(serializer.data)
                borrowers.append(borrower.pk)
        borrowers = (list(set(borrowers)))
        for each_rez in rez:
            if each_rez['borrower'] in borrowers:
                new_rez.append(each_rez)
                borrowers.remove(each_rez['borrower'])
            else:
                for each_new_rez in new_rez:
                    if each_new_rez['borrower'] == each_rez['borrower']:
                        each_new_rez["principal_released"] = str(float(each_rez["principal_released"])+ float(each_new_rez["principal_released"]))
                        each_new_rez["principal_at_risk"] = str(float(each_rez["principal_at_risk"]) + float(each_new_rez["principal_at_risk"]))
                        each_new_rez["due_loans_principal"] = str(float(each_rez["due_loans_principal"]) + float(each_new_rez["due_loans_principal"]))
                        each_new_rez["due_loans_interest"] = str(float(each_rez["due_loans_interest"]) + float(each_new_rez["due_loans_interest"]))
                        each_new_rez["due_loans_fees"] = str(float(each_rez["due_loans_fees"]) + float(each_new_rez["due_loans_fees"]))
                        each_new_rez["due_loans_penalty"] = str(float(each_rez["due_loans_penalty"]) + float(each_new_rez["due_loans_penalty"]))
                        each_new_rez["due_loans_total"] = str(float(each_rez["due_loans_total"]) + float(each_new_rez["due_loans_total"]))
                        each_new_rez["payments_principal"] = str(float(each_rez["payments_principal"]) + float(each_new_rez["payments_principal"]))
                        each_new_rez["payments_interest"] = str(float(each_rez["payments_interest"]) + float(each_new_rez["payments_interest"]))
                        each_new_rez["payments_fees"] = str(float(each_rez["payments_fees"]) + float(each_new_rez["payments_fees"]))
                        each_new_rez["payments_penalty"] = str(float(each_rez["payments_penalty"]) + float(each_new_rez["payments_penalty"]))
                        each_new_rez["payments_total"] = str(float(each_rez["payments_total"]) + float(each_new_rez["payments_total"]))
        return Response(new_rez, status=status.HTTP_200_OK) 



class AtAGlanceReport(APIView):
    def get(self, request, pk=None):
        loans_released = Loan.objects.exclude(status = "processing").exclude(status = "denied")
        fully_paid_loans = Loan.objects.filter(status="fully paid")
        default_loans = Loan.objects.filter(status="past maturity")
        de_amount = 0
        for r in default_loans:
            de_amount += r.remaining_balance
        percentage_default_loans = (len(default_loans)/len(loans_released)) * 100
        all_borrowers = len(Borrower.objects.all())
        rez = []
        borrowers = []
        new_rez = []
        balance = 0
        total_payments_principal = 0
        total_payments_interest = 0
        total_payments_fees = 0
        total_payments_penalty = 0
        for each_loan_released in loans_released:
            borrower = each_loan_released.borrower
            principal_released = float(each_loan_released.principal_amount)
            balance += each_loan_released.remaining_balance
            #maturity_date__lte = datetime.date.today()
            loan_schedule = LoanScheduler.objects.filter(loan = each_loan_released).filter(paid__gt = 0)
            amount_paid = float(each_loan_released.amount_paid)
            payments_interest = 0
            payments_fees = 0
            payments_penalty = 0
            for each_loan_schedule in loan_schedule:
                payments_interest += each_loan_schedule.interest
                payments_fees += each_loan_schedule.fees
                payments_penalty += each_loan_schedule.penalty
            payments_principal = amount_paid - payments_interest - payments_fees - payments_penalty
            #rez.append(serializer.data)
            borrowers.append(borrower.pk)
            total_payments_principal += payments_principal
            total_payments_interest += payments_interest
            total_payments_fees += payments_fees
            total_payments_penalty += payments_penalty
        borrowers = (list(set(borrowers)))
        data = {
            "no_of_registered_borrowers": all_borrowers,
            "no_of_active_borrowers": len(borrowers),
            "fully paid loans": len(fully_paid_loans),
            "open loans": len(loans_released),
            "balance": balance,
            "default loans":len(default_loans),
            "amount_of_past_due": de_amount,
            "percentage_default_loans":percentage_default_loans,
            "payments_principal":total_payments_principal,
            "payments_interest":total_payments_interest,
            "payments_fees":total_payments_fees,
            "payments_penalty":total_payments_penalty,
        }

        return Response(data, status=status.HTTP_200_OK) 


class MonthlyReport(APIView):
    def get(self, request, pk=None):
        branch = request.GET.get("branch")
        check_branch = Loan.objects.filter(branch=branch).exists()
        if check_branch == False:
            return Response({'not_found': 'Branch does not exists'}, status=status.HTTP_404_NOT_FOUND)
        jan, feb, mar, apr, may, jun, jul, aug, sept, octo, nov, dec = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        today = datetime.datetime.today()
        total_month = 12
        current_month = datetime.datetime.now().month
        datas = []
        for i in range(current_month):
            month = current_month - i
            all_loan = Loan.objects.filter(branch=branch, request_date__lte=datetime.datetime.now() - relativedelta(months=month))
            number_of_fully_paid = Loan.objects.filter(branch=branch, status="fully paid")
            loans = Loan.objects.filter(branch=branch, request_date__lte=datetime.datetime.now() - relativedelta(months=month)).count()
            new_loans = Loan.objects.filter(branch=branch, request_date__lte=datetime.datetime.now() - relativedelta(months=month))
            pending_due = Loan.objects.filter(branch=branch, status= "current", request_date__lte=datetime.datetime.now() - relativedelta(months=month))
            get_fully_paid = Loan.objects.filter(branch=branch, status="fully paid", loan_release_date__lt = datetime.date.today() - relativedelta(months=month))
            get_fully_paid = get_fully_paid.count()
            new_loans = new_loans.count()
            pending_due = pending_due.count()
            monthinteger = month
            year = datetime.datetime.now().year
            d_month = datetime.date(year, monthinteger, 1).strftime('%B')

            repayment = 0
            penalty = 0
            fees = 0
            interest = 0
            principal_received = 0
            principal_balance = 0
            for loan in all_loan:
                number_of_repayments = LoanRepayment.objects.filter(loan=loan, date__lte=datetime.datetime.now() - relativedelta(months=month))
                loan_schedule = LoanScheduler.objects.filter(loan=loan, date__lte=datetime.datetime.now() - relativedelta(months=month))
                loan_schedule1 = LoanScheduler.objects.filter(loan=loan, paid__gt=0, status="settled", date__lte=datetime.datetime.now() - relativedelta(months=month))
                principal_received += loan.amount_paid
                for sch1 in loan_schedule1:
                    interest += sch1.interest
                for sch in loan_schedule:
                    penalty += sch.penalty
                    fees += sch.fees
                repayment += number_of_repayments.count()
                principal_balance = loan.branch.remaining_capital
            total_received = principal_received + fees + interest + penalty

            data = {
                'fully_paid_loans': get_fully_paid,
                'number_of_repayments': repayment,
                'new_loans': new_loans,
                'penalty_received':penalty,
                'principal_balance': principal_balance,
                'principal_received': principal_received,
                'fees_received': fees,
                'interest_received': interest,
                'pending_due': pending_due,
                'total_received': total_received,
                'month_of': d_month

            }
            datas.append(data)

        
        return Response({"monthly_reports": datas}, status=status.HTTP_200_OK) 


# class MonthlyReport(APIView):
#     def get(self, request, pk=None):
#         branch = request.GET.get("branch")
#         all_loan = Loan.objects.all()
#         number_of_repayments = LoanRepayment.objects.all()
#         number_of_fully_paid = Loan.objects.filter(status="fully paid")
#         new_loans = Loan.objects.filter(request_date__lte=datetime.datetime.now() - timedelta(days=30))
#         pending_due = 0
#         total_principal_received = 0
#         total_interest_received = 0
#         total_fees_received = 0
#         total_penalty_received = 0
#         total_amount_received = 0
#         for each_loan in all_loan:
#             total_received = each_loan.amount_paid
#             principal_received = (each_loan.total_due_principal - each_loan.interest)\
#                  - each_loan.loan_fees - each_loan.penalty_amount
#             interest_received = each_loan.total_due_interest - each_loan.interest
#             fees_received = each_loan.total_due_loan_fee - each_loan.loan_fees
#             penalty_received = each_loan.total_due_penalty - each_loan.penalty_amount
#             pending_due += each_loan.remaining_balance
#         total_amount_received += total_received
#         total_principal_received += principal_received
#         total_interest_received += interest_received
#         total_fees_received += fees_received
#         total_penalty_received += penalty_received
#         queried_branch = Branch.objects.get(pk=branch)
#         if total_interest_received < 0:
#             total_interest_received = 0
#         if total_principal_received < 0:
#             total_principal_received = 0
#         data = {
#             "principal_balance": queried_branch.capital,
#             "principal_received": total_principal_received,
#             "interest received": total_interest_received,
#             "fees received": total_fees_received,
#             "penalty received": total_penalty_received,
#             "total_received": total_amount_received,
#             "new loans": len(new_loans),
#             "number of repayments": len(number_of_repayments),
#             "pending due": pending_due,
#             "number of fully paid": len(number_of_fully_paid)
#         }        
#         return Response(data, status=status.HTTP_200_OK) 

class AllEnteries(APIView):
    def get(self, request, pk=None):
        all = []
        branch = request.GET.get("branch")
        disbursements = LoanDisbursement.objects.all()
        repayments = LoanRepayment.objects.all()
        if len(repayments)>0:
            for r in repayments:
                repayment = r.amount
        else:
            repayment = 0
        globe = []
        for d in disbursements:
            data = {
            "d_type" : "Loan Released",
            "category" : d.loan.loan_type.name,
            "transaction_details" : d.loan.borrower.first_name + " " + d.loan.borrower.last_name + " - " + str(d.loan.id),
            "d_in" : repayment,
            "d_out" : d.disbursed_amount
            }
            globe.append(data)


        payroll = Payroll.objects.all()
        for p in payroll:
            data2 = {
            "d_type" : "Pay roll",
            "category" : p.staff.user.username,
            "transaction_details" : "",
            "d_in" : "",
            "d_out" : p.net_pay
            }
            globe.append(data2)
    
        return Response(globe, status=status.HTTP_200_OK)

# class AllEnteries(APIView):
#     def get(self, request, pk=None):
#         all = []
#         branch = request.GET.get("branch")
#         disbursements = LoanDisbursement.objects.all()
#         globe = []
#         for d in disbursements:
#             data = {
#             "d_type" : "Loan Released",
#             "category" : d.loan.loan_type.name,
#             "transaction_details" : d.loan.borrower.first_name + " " + d.loan.borrower.last_name + " " + str(d.loan.pk),
#             "d_in" : " ",
#             "d_out" : d.disbursed_amount
#             }
#             globe.append(data)


#         payroll = Payroll.objects.all()
#         for p in payroll:
#             data2 = {
#             "d_type" : "Pay roll",
#             "category" : p.staff.user.username,
#             "transaction_details" : "",
#             "d_in" : "",
#             "d_out" : p.net_pay
#             }
#             globe.append(data2)
    
#         return Response(globe, status=status.HTTP_200_OK) 