import calendar
import json
import requests
import hashlib
import datetime

from django.http import Http404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from .models import *
from accounts.models import (
    Profile
)

class LoanView(APIView):
    
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            res = serializer.data
            return Response(dict(id=res['id'], message='Loan initialized successful'), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def get(self, request, pk=None):
    #     loan = Loan.objects.all()
    #     serializer = LoanSerializer(loan, many=True)
    #     return Response(serializer.data)
    def get(self, request):
        ref = request.GET.get("ref")
        loan_status = request.GET.get("status")
        borrower = request.GET.get("borrower")
        if ref:
            try:
                loan = Loan.objects.get(pk=ref)
                serializer = LoanSerializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"message": "loan does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
        if loan_status:
            try:
                loan = Loan.objects.get(status=loan_status)
                serializer = LoanSerializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"message": "loan does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
        if borrower:
            try:
                loan = Loan.objects.get(borrower=borrower)
                serializer = LoanSerializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"message": "loan does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
        q = Loan.objects.all()
        serializer = LoanSerializer(q, many=True)
        return Response(serializer.data)
        # q = Loan.objects.all()
        # if loan_status:
        #     q = q.filter(status=loan_status)
        # response = [LoanSerializer(loan).data for loan in q]
        # return Response(response, status=status.HTTP_200_OK)

    def patch(self, request):
        # approved/decline loan by admin/staff
        data = request.data
        errors = []
        stat = data.get('status')
        if not stat:
            errors.append({"status": "status field is required"})
        loan_id = data.get('id')
        if not loan_id:
            errors.append({"id": "loan id is required"})
        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            loan = Loan.objects.get(id=loan_id)
            if(loan.status == stat):
                loan.save()
            else:
                return Response([{"status": "invalid loan status"}],
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "loan has been updated successful"})
        except ObjectDoesNotExist as error:
            return Response({"message": "loan with the id does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        pass


class LoanCommentList(APIView):
    
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanCommentSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        loan_for = request.GET['loan']
        loan_comment = LoanComment.objects.filter(loan=int(loan_for))
        serializer = LoanCommentSerializer(loan_comment, many=True)
        return Response(serializer.data)

class LoanCommentDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return LoanComment.objects.get(pk=pk)
        except LoanComment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan_comment = self.get_object(pk)
        serializer = LoanCommentSerializer(loan_comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan_comment = self.get_object(pk)
        serializer = LoanCommentSerializer(loan_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan_comment = self.get_object(pk)
        loan_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoanOfficerList(APIView):
    
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanOfficerSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        loan_officer = LoanOfficer.objects.all()
        serializer = LoanOfficerSerializer(loan_officer, many=True)
        return Response(serializer.data)

class LoanOfficerDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return LoanOfficer.objects.get(pk=pk)
        except LoanOfficer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan_officer = self.get_object(pk)
        serializer = LoanOfficerSerializer(loan_officer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan_officer = self.get_object(pk)
        serializer = LoanOfficerSerializer(loan_officer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan_officer = self.get_object(pk)
        loan_officer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PrincipalOutstandingLoan(APIView):
    def get(self, request, pk=None):
        principal_outstanding = Loan.objects.filter(status = "current")
        output = []
        for unit in principal_outstanding:
            if(unit.repayment_amount == None):
                unit.repayment_amount = 0.00
            if (unit.amount_paid == None):
                unit.amount_paid = 0
            if (unit.repayment_amount < unit.principal_amount):
                rez = {'loan_id':unit.pk, 'released':unit.loan_release_date, 'maturity': unit.maturity_date, 'principal': unit.principal_amount,
                'principal_paid': unit.amount_paid, 'principal_balance': str(int(unit.principal_amount)-int(unit.amount_paid)), 'principal_due_till_today': unit.remaining_balance,
                'status': unit.status, 'branch':str(unit.branch.pk), 'borrower':str(unit.borrower.pk)}
                output.append(rez)
            else:
                pass
        #print(principal_outstanding)
        #serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


class TotalOpenLoans(APIView):
    def get(self, request, pk=None):
        open_loans = Loan.objects.filter(status = "current" or "due today" or "missed repayment" or "arrears" or "past maturity")
        serializer = LoanSerializer(open_loans, many=True)
        return Response(serializer.data)

class InterestOutstandingLoan(APIView):
    def get(self, request, pk=None):
        principal_outstanding = Loan.objects.filter(status = "current")
        output = []
        for unit in principal_outstanding:
            if(unit.repayment_amount == None):
                unit.repayment_amount = 0.00
            if (unit.amount_paid == None):
                unit.amount_paid = 0
            interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
            if int(unit.amount_paid) > int(unit.principal_amount):
                interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
            if (unit.repayment_amount < unit.principal_amount):
                rez = {'loan_id':unit.pk, 'released':unit.loan_release_date, 'maturity': unit.maturity_date, 'principal': unit.principal_amount,
                'principal_paid': unit.amount_paid, 'interest_oustanding': str(interest_amount), 'principal_due_till_today': unit.remaining_balance,
                'status': unit.status, 'branch':str(unit.branch.pk), 'borrower':str(unit.borrower.pk)}
                output.append(rez)
            else:
                pass
        #print(principal_outstanding)
        #serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


#getting the loan by category
class SearchLoanType(APIView):
    def get(self, request, pk=None):
        loan_type = request.GET.get("loan_type")
        #loans = LoanType.objects.filter(status = loan_type.name)[0]
        category = LoanType.objects.get(name=loan_type)
        loans = Loan.objects.filter(loan_type = category)
        serializer = LoanSerializer(loans[0])
        return Response(serializer.data)


        
class FullyPaidLoans(APIView):
    def get(self, request, pk=None):
        fully_paid = Loan.objects.filter(status = "fully paid")
        serializer = LoanSerializer(fully_paid, many=True)
        return Response(serializer.data)


class LoansByOfficers(APIView):
    def get(self, request, pk=None):
        print(".......")
        print(".......")
        print(pk)   
        print(".......")
        print(".......")     
        loan_officer = LoanOfficer.objects.filter(pk = pk)
        print(".......")
        print(".......")
        total = []
        rez = []
        loan_officer_loans = loan_officer[0].loan.all()
        for loan_officer_loan in loan_officer_loans:
            total.append(loan_officer_loan.pk)
        for unit in total:
            rez.append(Loan.objects.filter(pk = int(unit))[0])
        print(rez)
        # print(loan_officer[0].loan.all()[0].pk)   
        # print(".......")
        # print(".......")  
        serializer = LoanSerializer(rez, many=True)         
        #return Response(serializer.data)
        return Response(serializer.data)


class FeesOutstandingLoan(APIView):
    def get(self, request, pk=None):
        fees_outstanding = Loan.objects.filter(status = "current")
        output = []
        for unit in fees_outstanding:
            if(unit.repayment_amount == None):
                unit.repayment_amount = 0.00
            if (unit.amount_paid == None):
                unit.amount_paid = 0
            interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
            if int(unit.amount_paid) > int(unit.principal_amount):
                interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
            if (unit.repayment_amount < unit.principal_amount):
                rez = {'loan_id':unit.pk, 'released':unit.loan_release_date, 'maturity': unit.maturity_date, 'principal': unit.principal_amount,
                'principal_paid': unit.amount_paid, 'remaining_balance': unit.remaining_balance, 'principal_due_till_today': unit.remaining_balance,
                'status': unit.status, 'branch':str(unit.branch.pk), 'borrower':str(unit.borrower.pk)}
                output.append(rez)
            else:
                pass
        #print(principal_outstanding)
        #serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


# class LoanRepaymentViewSet(ModelViewSet):
#     serializer_class = LoanRepaymentSerializer

#     def get_queryset(self):
#         queryset = LoanRepayment.objects.all()
#         borrower = self.request.GET.get('borrower')
#         if borrower:
#             queryset.filter(loan_schedule__loan__borrower__pk=borrower)

#         return queryset

