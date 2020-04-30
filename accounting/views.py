import datetime
import calendar

from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Branch
from accounting.models import CashFlow

# class SaveCashFlow(APIView):
#     # def post(self, request, pk=None):
#         # first_date = request.data.get('first_date')
#         # last_date = request.data.get('last_date')
#         # branch = request.data.get('branch')
#         for each_branch in Branch:
#             branch_capital = Branch.objects.get(pk=each_branch).capital
#             expenses = 


class CashFlowAccumlated(APIView):
    def get(self, request, pk=None):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        branch = request.GET.get("branch")
        try:
            #http://127.0.0.1:8000/api/cash_flow_accumulated/?start_date=09-27-2020&&end_date=09-28-2020&&branch?1
            start_object = datetime.strptime(start_date, '%m-%d-%Y').date()    
            end_object = datetime.strptime(end_date, '%m-%d-%Y').date()
            first_cash_flow = CashFlow.objects.filter(branch=branch).filter(date=start_object)[0] 
            last_cash_flow = CashFlow.objects.filter(branch=branch).filter(date=end_object)[0]  
            branch_capital = first_cash_flow.branch_capital
            expenses = last_cash_flow.expenses - first_cash_flow.expenses
            payroll = last_cash_flow.payroll - first_cash_flow.payroll
            loan_released = last_cash_flow.loan_released - first_cash_flow.loan_released
            loan_repayment = last_cash_flow.loan_repayment - first_cash_flow.loan_repayment
            deposit = last_cash_flow.deposit - first_cash_flow.deposit
            withdrawal = last_cash_flow.withdrawal - first_cash_flow.withdrawal
            date = str(start_date) + " " + "to" + " " + str(end_date)
            result = {"branch": branch, "branch_capital": branch_capital, "expenses": expenses, "payroll": payroll, "loan_released": loan_released, "loan_repayment": loan_repayment, "deposit": deposit, "withdrawal": withdrawal, "date": date}
            return Response(result)
        except:
            return Response("Your input is not valid")


class CashFlowMonthly(APIView):
    def get(self, request, pk=None):
        branch = request.GET.get("branch")
        month = request.GET.get("month")
        year = request.GET.get("year")

        helper = calendar.monthrange(int(year), int(month))
        last_day = helper[1]
        if len(month) == 1:
            month = "0" + month

        start_date = month+"-"+"01"+"-"+year
        end_date = month+"-"+str(last_day)+"-"+year
        print(start_date)
        print(end_date)
        try:
            #http://127.0.0.1:8000/api/cash_flow_monthly/?month=4&year=2020&branch=1
            start_object = datetime.strptime(start_date, '%m-%d-%Y').date()    
            end_object = datetime.strptime(end_date, '%m-%d-%Y').date()
            first_cash_flow = CashFlow.objects.filter(branch=branch).filter(date=start_object)[0] 
            last_cash_flow = CashFlow.objects.filter(branch=branch).filter(date=end_object)[0]  
            branch_capital = first_cash_flow.branch_capital
            expenses = last_cash_flow.expenses - first_cash_flow.expenses
            payroll = last_cash_flow.payroll - first_cash_flow.payroll
            loan_released = last_cash_flow.loan_released - first_cash_flow.loan_released
            loan_repayment = last_cash_flow.loan_repayment - first_cash_flow.loan_repayment
            deposit = last_cash_flow.deposit - first_cash_flow.deposit
            withdrawal = last_cash_flow.withdrawal - first_cash_flow.withdrawal
            date = str(start_date) + " " + "to" + " " + str(end_date)
            result = {"branch": branch, "branch_capital": branch_capital, "expenses": expenses, "payroll": payroll, "loan_released": loan_released, "loan_repayment": loan_repayment, "deposit": deposit, "withdrawal": withdrawal, "date": date}
            return Response(result)
        except:
            return Response("Your input is not valid")


class CashFlowAccumlated(APIView):
    def get(self, request, pk=None):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        branch = request.GET.get("branch")
        try:
            return Response("result")
        except:
            return "Your input is not valid"