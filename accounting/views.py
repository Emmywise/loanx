#import datetime
from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
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
        #date_str = '09-19-2018'
        start_object = datetime.strptime(start_date, '%m-%d-%Y').date()    
        end_object = datetime.strptime(end_date, '%m-%d-%Y').date()
        first_cash_flow = CashFlow.objects.filter(date=start_object)
        last_cash_flow = CashFlow.objects.filter(date=end_object)     
        print(first_cash_flow)
        print("leke")
        print(last_cash_flow) 
        # filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today())
        # data = []
        # for filtered_loan in filtered_loans:
        #     if ((datetime.date.today() - filtered_loans[0].maturity_date).days) >= int(days_due):
        #         data.append(filtered_loan)
        #serializer = LoanSerializer(data, many=True)
        #return Response(serializer.data)
        #return "Leke"