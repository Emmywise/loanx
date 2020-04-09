import calendar
import json
import requests
import hashlib
import datetime
import random

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from .models import *
from accounts.models import (
    Profile
)
from .utils import details_from_bvn, compare_dates, get_loan_score


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
            if loan.status == stat:
                loan.save()
            else:
                return Response([{"status": "invalid loan status"}],
                                status=status.HTTP_400_BAD_REQUEST)
            loan.status = "restructured"     
            serializer = LoanSerializer(loan, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
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


class LoanFeeList(APIView):
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanFeeSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        loan_for = request.GET['loan']
        loan_fee = LoanFee.objects.filter(loan=int(loan_for))
        serializer = LoanFeeSerializer(loan_fee, many=True)
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

    def get(self, request, pk):
        loan_comment = self.get_object(pk)
        serializer = LoanCommentSerializer(loan_comment)
        return Response(serializer.data)

    def put(self, request, pk):
        loan_comment = self.get_object(pk)
        serializer = LoanCommentSerializer(loan_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
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
        principal_outstanding = Loan.objects.filter(status="current")
        output = []
        for unit in principal_outstanding:
            if unit.repayment_amount is None:
                unit.repayment_amount = 0.00
            if unit.amount_paid is None:
                unit.amount_paid = 0
            if unit.repayment_amount < unit.principal_amount:
                rez = {'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
                       'principal': unit.principal_amount,
                       'principal_paid': unit.amount_paid,
                       'principal_balance': str(int(unit.principal_amount) - int(unit.amount_paid)),
                       'principal_due_till_today': unit.remaining_balance,
                       'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk)}
                output.append(rez)
            else:
                pass
        # print(principal_outstanding)
        # serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


class TotalOpenLoans(APIView):
    def get(self, request, pk=None):
        open_loans = Loan.objects.filter(
            status="current" or "due today" or "missed repayment" or "arrears" or "past maturity")
        serializer = LoanSerializer(open_loans, many=True)
        return Response(serializer.data)


class InterestOutstandingLoan(APIView):
    def get(self, request, pk=None):
        principal_outstanding = Loan.objects.filter(status="current")
        output = []
        for unit in principal_outstanding:
            if unit.repayment_amount is None:
                unit.repayment_amount = 0.00
            if unit.amount_paid is None:
                unit.amount_paid = 0
            interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
            if int(unit.amount_paid) > int(unit.principal_amount):
                interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
            if unit.repayment_amount < unit.principal_amount:
                rez = {'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
                       'principal': unit.principal_amount,
                       'principal_paid': unit.amount_paid, 'interest_oustanding': str(interest_amount),
                       'principal_due_till_today': unit.remaining_balance,
                       'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk)}
                output.append(rez)
            else:
                pass
        # print(principal_outstanding)
        # serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


# class PenaltyOutstandingLoan(APIView):
#     def get(self, request, pk=None):
#         penalty_outstanding = Loan.objects.filter(penalty_rate__gte=0)
#         output = []
#         for unit in principal_outstanding:
#             if(unit.repayment_amount == None):
#                 unit.repayment_amount = 0.00
#             if (unit.amount_paid == None):
#                 unit.amount_paid = 0
#             interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
#             if int(unit.amount_paid) > int(unit.principal_amount):
#                 interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
#             if (unit.repayment_amount < unit.principal_amount):
#                 rez = {'loan_id':unit.pk, 'released':unit.loan_release_date, 'maturity': unit.maturity_date, 'principal': unit.principal_amount,
#                 'principal_paid': unit.amount_paid, 'interest_oustanding': str(interest_amount), 'principal_due_till_today': unit.remaining_balance,
#                 'status': unit.status, 'branch':str(unit.branch.pk), 'borrower':str(unit.borrower.pk)}
#                 output.append(rez)
#             else:
#                 pass
#         #print(principal_outstanding)
#         #serializer = LoanSerializer(principal_outstanding, many=True)
#         return Response(output)


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
        fully_paid = Loan.objects.filter(status="fully paid")
        serializer = LoanSerializer(fully_paid, many=True)
        return Response(serializer.data)


class LoansByOfficers(APIView):
    def get(self, request, pk=None):  
        loan_officer = LoanOfficer.objects.filter(pk = pk)
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
        fees_outstanding = Loan.objects.filter(status="current")
        output = []
        for unit in fees_outstanding:
            if unit.repayment_amount is None:
                unit.repayment_amount = 0.00
            if unit.amount_paid is None:
                unit.amount_paid = 0
            interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
            if int(unit.amount_paid) > int(unit.principal_amount):
                interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
            if unit.repayment_amount < unit.principal_amount:
                rez = {'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
                       'principal': unit.principal_amount,
                       'principal_paid': unit.amount_paid, 'remaining_balance': unit.remaining_balance,
                       'principal_due_till_today': unit.remaining_balance,
                       'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk)}
                output.append(rez)
            else:
                pass
        # print(principal_outstanding)
        # serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


class LoanRepaymentViewSet(ModelViewSet):
    serializer_class = LoanRepaymentSerializer

    def get_queryset(self):
        queryset = LoanRepayment.objects.all()
        borrower = self.request.GET.get('borrower')
        branch = self.request.GET.get('branch')
        if branch:
            queryset.filter(branch__pk=branch)
        if borrower:
            queryset.filter(loan__borrower__pk=borrower)

        return queryset


class LoanCollateralViewSet(ModelViewSet):
    serializer_class = LoanCollateralSerializer

    def get_queryset(self):
        queryset = LoanCollateral.objects.all()
        borrower = self.request.GET.get('borrower')
        branch = self.request.GET.get('branch')
        if branch:
            queryset.filter(loan__branch__pk=branch)
        if borrower:
            queryset.filter(loan__borrower__pk=borrower)

        return queryset


class LoanGuarantorViewSet(ModelViewSet):
    serializer_class = LoanGuarantorSerializer

    def get_queryset(self):
        queryset = LoanGuarantor.objects.all()
        borrower = self.request.GET.get('borrower')
        branch = self.request.GET.get('branch')
        if branch:
            queryset.filter(loan__branch__pk=branch)
        if borrower:
            queryset.filter(loan__borrower__pk=borrower)

        return queryset


class LoanDisbursementViewSet(ModelViewSet):
    serializer_class = LoanDisbursementSerializer

    def get_queryset(self):
        queryset = LoanDisbursement.objects.all()
        borrower = self.request.GET.get('borrower')
        branch = self.request.GET.get('branch')
        if branch:
            queryset.filter(loan__branch__pk=branch)
        if borrower:
            queryset.filter(loan__borrower__pk=borrower)

        return queryset


class GuarantorFileViewSet(ModelViewSet):
    serializer_class = GuarantorFileSerializer

    def get_queryset(self):
        queryset = GuarantorFile.objects.all()

        return queryset


class RunBvnCheck(APIView):

    def post(self, request):
        borrower = request.data.get("borrower")
        bvn = request.data.get("bvn")
        dob = request.data.get("dob")
        reference_no = 'loanx' + str(random.randint(100000000, 999999999))
        rez = details_from_bvn(bvn, reference_no)
        print(rez)
        dob_check = (compare_dates(rez['date_of_birth'], dob))
        if not dob_check:
            return Response({"message": "non-matching credentials provided"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            borrower_obj = Borrower.objects.get(pk=borrower)
            try:
                borrower_obj.gender = rez['gender']
            except:
                pass
            try:
                borrower_obj.last_name = rez['last_name']
            except:
                pass
            try:
                borrower_obj.first_name = rez['first_name']
            except:
                pass
            try:
                borrower_obj.middle_name = rez['middle_name']
            except:
                pass
            try:
                borrower_obj.email = rez['email']
            except:
                pass
            try:
                borrower_obj.address = rez['residential_address']
            except:
                pass
            try:
                borrower_obj.city = rez['city']
            except:
                pass
            try:
                borrower_obj.date_of_birth = dob
            except:
                pass
            try:
                borrower_obj.bvn = bvn
            except:
                pass
            try:
                borrower_obj.email = rez['email']
            except:
                pass
            try:
                borrower_obj.phone = rez['phone_number']
            except:
                pass
            borrower_obj.save()
            return Response({"message": "successfully updated from api"}, status=status.HTTP_200_OK)
        except Borrower.DoesNotExist as err:
            return Response({"message": "borrower with the id does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class GetLoanScore(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        borrower = request.data.get('borrower')
        reference_no = 'loanx' + str(random.randint(100000000, 999999999))
        rez = get_loan_score(phone, reference_no)
        print(rez)
        try:
            borrower = Borrower.objects.get(pk=borrower)
            try:
                if rez['score']:
                    borrower.loan_score = rez['score']
                    borrower.save()
            except:
                pass
            return Response({"message": rez}, status=status.HTTP_200_OK)
        except Borrower.DoesNotExist:
            return Response({'message': 'borrower with the borrower id does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
#     def get_queryset(self):
#         queryset = LoanRepayment.objects.all()
#         borrower = self.request.GET.get('borrower')
#         if borrower:
#             queryset.filter(loan_schedule__loan__borrower__pk=borrower)

#         return queryset

class LoanCollateralList(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanCollateralSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        loan_collateral = LoanCollateral.objects.all()
        serializer = LoanCollateralSerializer(loan_collateral, many=True)
        return Response(serializer.data)

class LoanCollateralDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return LoanCollateral.objects.get(pk=pk)
        except LoanCollateral.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan_collateral = self.get_object(pk)
        serializer = LoanCollateralSerializer(loan_collateral)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan_collateral = self.get_object(pk)
        serializer = LoanCollateralSerializer(loan_collateral, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan_collateral = self.get_object(pk)
        loan_collateral.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class LoanAttachmentList(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        loan_attachment = LoanAttachment.objects.all()
        serializer = LoanAttachmentSerializer(loan_attachment, many=True)
        return Response(serializer.data)

class LoanAttachmentDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return LoanAttachment.objects.get(pk=pk)
        except LoanAttachment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        loan_attachment = self.get_object(pk)
        serializer = LoanAttachmentSerializer(loan_attachment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        loan_attachment = self.get_object(pk)
        serializer = LoanAttachmentSerializer(loan_attachment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        loan_attachment = self.get_object(pk)
        loan_attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApproveOrDeclineLoan(APIView):
    
    def post(self, request):
        loan = request.data.get('loan')
        loan_status = request.data.get('status')

        loan_obj = Loan.objects.filter(pk=loan).first()
        if not loan_obj:
            return Response({"message": "Loan with the loan id cannot be fount"},
                            status=status.HTTP_404_NOT_FOUND)
        if loan_status and loan_status == 'current':
            default_interest_rate = loan_obj.loan_type.interest_rate
            if default_interest_rate:
                default_interest_rate = float(default_interest_rate)
            overridden_interest_rate = loan_obj.loan_interest_percentage
            if overridden_interest_rate:
                overridden_interest_rate = float(overridden_interest_rate)
            default_fixed_amount = loan_obj.loan_interest_fixed_amount
            if default_fixed_amount:
                default_fixed_amount = float(default_fixed_amount)
            duration = loan_obj.duration
            loan_fees = loan_obj.loanfee_set.all()
            total_repayment_amount = float(loan_obj.principal_amount)
            if (not default_fixed_amount) and (not overridden_interest_rate):
                total_repayment_amount += float(default_interest_rate) * total_repayment_amount
            if overridden_interest_rate and (not default_fixed_amount):
                total_repayment_amount += float(overridden_interest_rate) * total_repayment_amount
            if default_fixed_amount and (not overridden_interest_rate):
                total_repayment_amount += default_fixed_amount
            try:
                existing_schedules = LoanScheduler.objects.filter(loan = loan).delete()
            except:
                pass
            for loan_fee in loan_fees:
                total_repayment_amount += float(loan_fee.amount)
            loan_obj.repayment_amount = total_repayment_amount
            loan_obj.remaining_balance = total_repayment_amount
            loan_obj.status = loan_status
            loan_obj.save()
            total_repayment_amount_per_schedule = total_repayment_amount / duration
            current_time = timezone.now()
            for i in range(1, duration + 1):
                payment_date = current_time
                if loan_obj.loan_duration_period == 'Days':
                    payment_date = current_time + relativedelta(days=i)
                elif loan_obj.loan_duration_period == 'Weeks':
                    payment_date = current_time + relativedelta(weeks=i)
                elif loan_obj.loan_duration_period == 'Months':
                    payment_date = current_time + relativedelta(months=i)
                else:
                    payment_date = current_time + relativedelta(years=i)

                #check if there are original schedules
                loan_scheduler = LoanScheduler.objects.create(
                    loan=loan_obj,
                    date=payment_date,
                    amount=total_repayment_amount_per_schedule,
                    status='pending'
                )
            return Response({"message": "loan has been approved"})
        elif loan_status and loan_status == 'denied':
            loan_obj.status = 'denied'
            loan_obj.save()
            return Response({"message": "loan has been declined"})
        return Response({"message": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class EarlySettledLoans(APIView):
    def get(self, request, pk=None):
        balanced_loans = Loan.objects.filter(status = "fully paid")
        result = []
        for loan in balanced_loans:
            loan_repayments = LoanRepayment.objects.filter(loan=loan, last_repayment_date__lt = loan.maturity_date)
            for repayment in loan_repayments:
                result.append(loan)
        serializer = LoanSerializer(result, many=True)
        result = None
        return Response(serializer.data)


class DueLoansBetween(APIView):
    def get(self, request, pk=None):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        filtered_loans = Loan.objects.filter(maturity_date__gt = start_date).filter(maturity_date__lt = end_date)
        serializer = LoanSerializer(filtered_loans, many=True)
        result = None
        return Response(serializer.data)


class DueLoansNoPayment(APIView):
    def get(self, request, pk=None):
        filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(amount_paid__lte = 0)
        serializer = LoanSerializer(filtered_loans, many=True)
        result = None
        return Response(serializer.data)


class DueLoansPartPayment(APIView):
    def get(self, request, pk=None):
        filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(amount_paid__gte = 0).exclude(status= "fully paid")
        serializer = LoanSerializer(filtered_loans, many=True)
        result = None
        return Response(serializer.data)


class GetDueLoansByDays(APIView):
    def get(self, request, pk=None):
        days_due = request.GET.get("days_due")
        filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today())
        data = []
        for filtered_loan in filtered_loans:
            if ((datetime.date.today() - filtered_loans[0].maturity_date).days) >= int(days_due):
                data.append(filtered_loan)
        serializer = LoanSerializer(data, many=True)
        return Response(serializer.data)


class ManualRepayment(APIView):
    def post(self, request, pk=None):
        amount = int(request.data.get('amount'))
        loan = request.data.get('loan')
        repayment_mode = request.data.get('repayment_mode')
        payment_type = request.data.get('payment_type')
        proof_of_payment = request.FILES.get('proof_of_payment')
        collector = request.data.get('collector')
        comment = request.data.get('comment')
        collector = LoanOfficer.objects.get(pk = int(collector))
        sent_amount = amount
        the_loan = Loan.objects.get(pk = loan)
        try:
            if(the_loan.amount_paid == None):
                the_loan.amount_paid = 0.00
            the_loan.amount_paid += amount
            the_loan.save()
        except:
            pass
        get_schedule = LoanScheduler.objects.filter(loan = loan).order_by("date")
        if len(get_schedule) == 0:
            return Response({"msg":"open loan found"})
        for unit in get_schedule:
            if(unit.status != "settled"):
                if(int(amount) < unit.amount):
                    unit.amount -= int(amount)
                    amount = 0
                    unit.save()
                else:
                    unit.status = "settled"
                    amount -= unit.amount
                    unit.save()
            else:
                pass

        #deduct schedule
        #deduct balance
        #order_by("-id")
        loan_payment = LoanRepayment.objects.create(
            loan=the_loan,\
            date=datetime.date.today(),\
            amount=sent_amount,\
            repayment_mode = repayment_mode,\
            payment_type = payment_type,\
            proof_of_payment = proof_of_payment,\
            collector = collector,\
            comment = comment
        )
        serializer = LoanSchedulerSerializer(get_schedule, many=True)
        return Response({"msg":"repayment was successful","schedule": serializer.data})