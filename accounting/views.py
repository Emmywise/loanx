from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import Branch

# class SaveCashFlow(APIView):
#     # def post(self, request, pk=None):
#         # first_date = request.data.get('first_date')
#         # last_date = request.data.get('last_date')
#         # branch = request.data.get('branch')
#         for each_branch in Branch:
#             branch_capital = Branch.objects.get(pk=each_branch).capital
#             expenses = 