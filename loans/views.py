import calendar
import json
import requests
import hashlib
import datetime

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
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
        if ref:
            try:
                loan = Loan.objects.get(ref_id=ref)
                serializer = LoanSerializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"message": "loan does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
        q = Loan.objects.all()
        serializer = LoanSerializer(q, many=True)
        return Response(serializer.data)
        q = Loan.objects.all()
        if loan_status:
            q = q.filter(status=loan_status)
        response = [LoanSerializer(loan).data for loan in q]
        return Response(response, status=status.HTTP_200_OK)

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
        loan_comment = LoanComment.objects.all()
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


class FullyPaidLoans(APIView):
    def get(self, request, pk=None):
        fully_paid = Loan.objects.filter(status = "fully paid")
        serializer = LoanSerializer(fully_paid, many=True)
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