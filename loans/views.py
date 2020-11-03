import calendar
import json
import requests
import hashlib
import datetime
import random
import decimal
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
from .serializers import *
from .models import *
from accounts.models import (
    Profile
)
from borrowers.serializers import BorrowerSerializer
from .utils import details_from_bvn, compare_dates, get_loan_score, get_account_name
from .save_auth_code import ddebitCode
from .direct_debit import directDebit


class LoanView(APIView):

    def post(self, request):
        # initialize a loan by customer
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            res = serializer.data
            return Response(res, status=status.HTTP_200_OK)
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
            loan = Loan.objects.filter(borrower=borrower)
            rez = []
            for each_loan in loan:             
                serializer = LoanSerializer(each_loan).data
                rez.append(serializer)
            return Response(rez, status=status.HTTP_200_OK)
        q = Loan.objects.all()
        serializer = LoanSerializer(q, many=True)
        return Response(serializer.data)

    # def get_object(self, pk):
    #     return Loan.objects.get(pk=pk)

    def patch(self, request, pk):
        # approved/decline loan by admin/staff
        # data = request.data
        # loan_id = data.get('id')
        try:
            loan = Loan.objects.get(pk=pk)
            loan.status = "restructured" 
            loan.save()    
            serializer = LoanSerializer(loan, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"message": "loan has been updated successful"})
        except ObjectDoesNotExist as error:
            return Response({"message": "loan with the id does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        loan = Loan.objects.get(pk=pk)
        loan.delete()
        return Response({"message": "loan deleted successfully!"})


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

class LoanToOfficer(APIView):
    def post(self, request):
        # initialize a loan by customer
        serializer = LoanMembershipSerializer(data=request.data)
        if serializer.is_valid():
            # save loan and send loan application email.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        #loan_for = request.GET['loan']
        loan_membership = LoanMembership.objects.filter(loan=pk)
        serializer = LoanMembershipSerializer(loan_membership, many=True)
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
        principal_outstanding = Loan.objects.exclude(status="denied").exclude(status = "fully paid").exclude(status = "processing")
        output = []
        for unit in principal_outstanding:
            if unit.amount_paid < unit.principal_amount:
                principal_paid = unit.principal_amount - unit.amount_paid
            else:
                principal_paid = unit.principal_amount

            principal_due_till_today = 0
            filtered_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
            for filtered_loan_schedule in filtered_loan_schedules:
                principal_due_till_today += principal_due

            

            rez = {'name': (unit.borrower.title + " "+ unit.borrower.first_name + " " + unit.borrower.last_name), 'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
                    'principal': unit.principal_amount,
                    'principal_paid': principal_paid,
                    'principal_balance': str(int(unit.principal_amount) - int(unit.amount_paid)),
                    'principal_due_till_today': principal_due_till_today,
                    'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk),
                    'principal_paid_till_today': principal_paid, 'principal_balance_till_today': (principal_due_till_today - principal_paid)}
            output.append(rez)
        # print(principal_outstanding)
        # serializer = LoanSerializer(principal_outstanding, many=True)
        return Response(output)


class TotalOpenLoans(APIView):
    def get(self, request, pk=None):
        open_loans = Loan.objects.exclude(status="denied").exclude(status = "fully paid").exclude(status="missed repayment")
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
        serializer = LoanSerializer(rez, many=True)         
        return Response(serializer.data)


class FeesOutstandingLoan(APIView):
    def get(self, request, pk=None):
        fees_outstanding = Loan.objects.filter(loan_fees__gt = 0)
        # output = []
        # for unit in fees_outstanding:
        #     if unit.repayment_amount is None:
        #         unit.repayment_amount = 0.00
        #     if unit.amount_paid is None:
        #         unit.amount_paid = 0
        #     interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
        #     if int(unit.amount_paid) > int(unit.principal_amount):
        #         interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
        #     if unit.repayment_amount < unit.principal_amount:
        #         rez = {'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
        #                'principal': unit.principal_amount,
        #                'principal_paid': unit.amount_paid, 'remaining_balance': unit.remaining_balance,
        #                'principal_due_till_today': unit.remaining_balance,
        #                'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk)}
        #         output.append(rez)

            # else:
            #     pass
        # print(principal_outstanding)
        serializer = LoanSerializer(fees_outstanding, many=True).data
        return Response(serializer)


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

class LoanTypeViewSet(ModelViewSet):
    serializer_class = LoanTypeSerializer

    def get_queryset(self):
        queryset = LoanType.objects.all()
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


class GetAccountName(APIView):

    def post(self, request):
        account_number = request.data.get("account_number")
        bank_code = request.data.get("bank_code")
        ref = 'loanx' + str(random.randint(100000000, 999999999))
        rez = get_account_name(account_number, bank_code, ref)
        if rez == False:
            return Response({"message": "Either Account Number/Selected Bank does not match."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": rez},status=status.HTTP_200_OK)


class GetLoanScore(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        borrower = request.data.get('borrower')
        phone = request.data.get('phone')
        reference_no = 'loanx' + str(random.randint(100000000, 999999999))
        borrower = Borrower.objects.get(pk=borrower)
        rez = get_loan_score(phone, reference_no, borrower.first_name, borrower.last_name, borrower.email, amount)
        print(rez)
        try:
            try:
                if rez['score']:
                    borrower.loan_score = rez['score']
                    borrower.save()
            except:
                pass
            serializer = BorrowerSerializer(borrower).data
            #borrower_groups = Loan.objects.filter(borrower=borrower).update()
            # return Response({"message": rez}, status=status.HTTP_200_OK)
            return Response(serializer, status=status.HTTP_200_OK)
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
        loan_attachment = LoanAttachment.objects.filter(loan = loan)
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
        decision = request.data.get('decision')
        #loan_status = request.data.get('status')
        if decision == "approve":
            loan_obj = Loan.objects.filter(pk=loan).first()
            loan_status = loan_obj.status
            print(loan_status)
            if not loan_obj:
                return Response({"message": "Loan with the loan id cannot be found"},
                                status=status.HTTP_404_NOT_FOUND)
            if loan_status and (loan_status == 'processing' or loan_status == 'restructured'):
                default_interest_rate = loan_obj.loan_type.interest_rate
                if default_interest_rate:
                    interest_rate = float(default_interest_rate)
                overridden_interest_rate = loan_obj.loan_interest_percentage
                if overridden_interest_rate:
                    interest_rate = float(overridden_interest_rate)
                default_fixed_amount = loan_obj.loan_interest_fixed_amount
                if default_fixed_amount:
                    default_fixed_amount = float(default_fixed_amount)
                duration = loan_obj.duration
                loan_fees = loan_obj.loanfee_set.all()
                total_repayment_amount = float(loan_obj.principal_amount)
                # for loan_fee in loan_fees:
                #     total_repayment_amount += float(loan_fee.amount)
                current_time = timezone.now()
                if loan_obj.interest_method == "Flat Rate":
                    total_repayment_amount = total_repayment_amount / duration
                    if (not default_fixed_amount) and (not interest_rate):
                        total_repayment_amount = total_repayment_amount + ((interest_rate/100)*float(loan_obj.principal_amount))
                    loan_obj.interest = (interest_rate/100)*float(loan_obj.principal_amount)
                    #loan_fees = 0                
                    for loan_fee in loan_fees:
                        loan_obj.loan_fees += float(loan_fee.amount)
                    if interest_rate and (not default_fixed_amount):
                        total_repayment_amount = total_repayment_amount + ((interest_rate/100)*float(loan_obj.principal_amount))
                    if default_fixed_amount and (not interest_rate):
                        total_repayment_amount += default_fixed_amount/ duration
                    principal_plus_interest = total_repayment_amount

                    try:
                        existing_schedules = LoanScheduler.objects.filter(loan = loan).delete()
                    except:
                        pass
                    total_loan_fees = 0.0
                    for loan_fee in loan_fees:
                        total_loan_fees += loan_fee
                        total_repayment_amount += float(loan_fee.amount)
                    loan_obj.loan_fees = total_loan_fees
                    loan_obj.repayment_amount = total_repayment_amount
                    loan_obj.remaining_balance = total_repayment_amount 
                    loan_obj.status = loan_status
                    loan_obj.loan_release_date = current_time
                    loan_obj.interest_start_date = current_time
                    if loan_obj.loan_duration_period == 'Days':
                        loan_obj.maturity_date = current_time + relativedelta(days=duration)
                    elif loan_obj.loan_duration_period == 'Weeks':
                        loan_obj.maturity_date = current_time + relativedelta(weeks=duration)
                    elif loan_obj.loan_duration_period == 'Months':
                        loan_obj.maturity_date= current_time + relativedelta(months=duration)
                    else:
                        loan_obj.maturity_date = current_time + relativedelta(years=duration)
                    loan_interest = 0
                    loan_obj.save()
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

                        loan_scheduler = LoanScheduler.objects.create(
                            loan=loan_obj,
                            description = "Repayment",
                            date=payment_date,
                            principal = loan_obj.principal_amount/loan_obj.duration,
                            interest = loan_obj.principal_amount * (loan_obj.interest_rate/100),
                            fees = loan_obj.loan_fees/duration,
                            penalty = loan_obj.penalty_amount/duration,
                            due = total_repayment_amount,
                            paid = 0.00,
                            pending_due = total_repayment_amount,
                            total_due = total_repayment_amount, 
                            principal_due = loan_obj.principal_amount/loan_obj.duration,
                            amount=total_repayment_amount,
                            status='pending'
                        )
                        loan_interest += loan_obj.principal_amount * (loan_obj.interest_rate/100)
                    loan_obj.interest = loan_interest
                    loan_obj.total_due_principal = loan_obj.principal_amount
                    loan_obj.total_due_interest = loan_obj.principal_amount * (loan_obj.interest_rate/100) * duration
                    loan_obj.total_due_fees = loan_obj.loan_fees
                    loan_obj.total_due_penalty = loan_obj.penalty_amount

                    loan_obj.save()
                    loan_schedules = LoanScheduler.objects.filter(loan = loan_obj)
                    serializer = LoanSchedulerSerializer(loan_schedules, many=True)
                    return Response({"message": "loan has been approved", "schedules":serializer.data})


                elif loan_obj.interest_method == "Reducing Balance - Equal Principal":
                    principal_outstanding = float(loan_obj.principal_amount)
                    try:
                        total_loan_fees = 0.0
                        for loan_fee in loan_fees:
                            total_loan_fees += loan_fee
                            principal_outstanding += float(loan_fee.amount)
                    except:
                        pass
                    default_interest_rate = loan_obj.loan_type.interest_rate
                    if default_interest_rate:
                        interest_rate = float(default_interest_rate)
                    overridden_interest_rate = loan_obj.loan_interest_percentage
                    if overridden_interest_rate != None:
                        interest_rate = float(overridden_interest_rate)
                    total_repayment_amount_per_schedule = principal_outstanding / duration
                    try:
                        existing_schedules = LoanScheduler.objects.filter(loan = loan).delete()
                    except:
                        pass
                    loan_obj.loan_fees = total_loan_fees
                    loan_obj.status = loan_status
                    loan_obj.loan_release_date = current_time
                    loan_obj.interest_start_date = current_time
                    if loan_obj.loan_duration_period == 'Days':
                        loan_obj.maturity_date = current_time + relativedelta(days=duration)
                    elif loan_obj.loan_duration_period == 'Weeks':
                        loan_obj.maturity_date = current_time + relativedelta(weeks=duration)
                    elif loan_obj.loan_duration_period == 'Months':
                        loan_obj.maturity_date= current_time + relativedelta(months=duration)
                    else:
                        loan_obj.maturity_date = current_time + relativedelta(years=duration)
                    loan_obj.save()  
                    principal_plus_interest = 0.0
                    total_interest = 0             
                    for i in range(1, duration + 1):
                        payment_date = current_time
                        repayment_schedule = total_repayment_amount_per_schedule + (principal_outstanding * (interest_rate / 100))
                        principal_plus_interest += repayment_schedule
                        if loan_obj.loan_duration_period == 'Days':
                            payment_date = current_time + relativedelta(days=i)
                        elif loan_obj.loan_duration_period == 'Weeks':
                            payment_date = current_time + relativedelta(weeks=i)
                        elif loan_obj.loan_duration_period == 'Months':
                            payment_date = current_time + relativedelta(months=i)
                        else:
                            payment_date = current_time + relativedelta(years=i)

                        loan_scheduler = LoanScheduler.objects.create(
                            loan=loan_obj,
                            description = "Repayment",
                            date=payment_date,
                            principal = loan_obj.principal_amount/loan_obj.duration,
                            interest = (repayment_schedule - loan_obj.principal_amount/loan_obj.duration),
                            fees = total_loan_fees/duration,
                            penalty = 0.00,
                            due=repayment_schedule,
                            paid = 0.00,
                            pending_due = repayment_schedule,
                            total_due = repayment_schedule,
                            principal_due = loan_obj.principal_amount/loan_obj.duration,
                            amount = repayment_schedule,
                            status='pending')
                        total_interest += (repayment_schedule - loan_obj.principal_amount/loan_obj.duration)
                        principal_outstanding -= total_repayment_amount_per_schedule
                        total_loan_fees = 0.0
                        for loan_fee in loan_fees:
                            total_loan_fee += loan_fee
                        loan_obj.loan_fees = total_loan_fee 
                        loan_obj.interest = total_interest
                    loan_obj.total_due_principal = loan_obj.principal_amount/loan_obj.duration * duration
                    loan_obj.total_due_interest = (repayment_schedule - loan_obj.principal_amount/loan_obj.duration) * duration
                    loan_obj.total_due_fees = total_loan_fees
                    loan_obj.total_due_penalty = 0.00
                    loan_obj.save()               
                    loan_schedules = LoanScheduler.objects.filter(loan = loan_obj)
                    serializer = LoanSchedulerSerializer(loan_schedules, many=True)
                    return Response({"message": "loan has been approved", "schedules":serializer.data})

                    
                elif loan_obj.interest_method == "Interest-Only":
                    t = 0
                    total_loan_fees = 0.0
                    for loan_fee in loan_fees:
                        total_loan_fees += loan_fee
                        total_repayment_amount += float(loan_fee.amount)
                    t = total_repayment_amount
                    total_repayment_amount = total_repayment_amount / duration
                    if (not default_fixed_amount) and (not overridden_interest_rate):
                        total_repayment_amount = (default_interest_rate/100)*float(loan_obj.principal_amount)
                        t = t + total_repayment_amount
                    if overridden_interest_rate and (not default_fixed_amount):
                        total_repayment_amount = (float(overridden_interest_rate)/100)*float(loan_obj.principal_amount)
                        print(total_repayment_amount)
                        t = t + total_repayment_amount
                    if default_fixed_amount and (not overridden_interest_rate):
                        total_repayment_amount += default_fixed_amount/ duration

                    try:
                        existing_schedules = LoanScheduler.objects.filter(loan = loan).delete()
                    except:
                        pass
                    loan_obj.loan_fees = total_loan_fees
                    loan_obj.repayment_amount = total_repayment_amount
                    loan_obj.remaining_balance = total_repayment_amount 
                    loan_obj.status = loan_status
                    loan_obj.loan_release_date = current_time
                    loan_obj.interest_start_date = current_time
                    if loan_obj.loan_duration_period == 'Days':
                        loan_obj.maturity_date = current_time + relativedelta(days=duration)
                    elif loan_obj.loan_duration_period == 'Weeks':
                        loan_obj.maturity_date = current_time + relativedelta(weeks=duration)
                    elif loan_obj.loan_duration_period == 'Months':
                        loan_obj.maturity_date= current_time + relativedelta(months=duration)
                    else:
                        loan_obj.maturity_date = current_time + relativedelta(years=duration)
                    loan_interest = 0
                    loan_obj.save()
                    other_principal = 0
                    principal_plus_interest = 0
                    for i in range(1, duration + 1):

                        payment_date = current_time
                        if i==1:
                            other_principal = total_repayment_amount
                        if i == duration:
                            total_repayment_amount = t
                        principal_plus_interest += total_repayment_amount
                        if loan_obj.loan_duration_period == 'Days':
                            payment_date = current_time + relativedelta(days=i)
                        elif loan_obj.loan_duration_period == 'Weeks':
                            payment_date = current_time + relativedelta(weeks=i)
                        elif loan_obj.loan_duration_period == 'Months':
                            payment_date = current_time + relativedelta(months=i)
                        else:
                            payment_date = current_time + relativedelta(years=i)
                        total_loan_fees = 0.0
                        for loan_fee in loan_fees:
                            total_loan_fees += loan_fee
                        loan_obj.loan_fees = total_loan_fees 
                        #check if there are original schedules
                        loan_scheduler = LoanScheduler.objects.create(
                            loan=loan_obj,
                            description = "Repayment", 
                            date = payment_date,
                            principal = total_repayment_amount - other_principal,
                            interest = other_principal, 
                            fees = total_loan_fees/duration,
                            penalty = 0.00,
                            due = total_repayment_amount,
                            paid = 0.00,
                            pending_due = total_repayment_amount, 
                            total_due = total_repayment_amount,
                            principal_due = total_repayment_amount - other_principal,
                            amount=total_repayment_amount,
                            status='pending'
                        )

                    loan_obj.interest = decimal.Decimal(principal_plus_interest) - decimal.Decimal(loan_obj.principal_amount)  
                    loan_obj.total_due_principal = (total_repayment_amount - other_principal) * duration
                    loan_obj.total_due_interest = (other_principal) * duration
                    loan_obj.total_due_fees = total_loan_fees
                    loan_obj.total_due_penalty = 0.00                       
                    loan_obj.save()
                    loan_schedules = LoanScheduler.objects.filter(loan = loan_obj)
                    serializer = LoanSchedulerSerializer(loan_schedules, many=True)
                    return Response({"message": "loan has been approved", "schedules":serializer.data})






                elif loan_obj.interest_method == "Reducing Balance - Equal Installments":
                    # principal_outstanding = float(loan_obj.principal_amount)
                    # try:
                    #     total_loan_fees = 0
                    #     for loan_fee in loan_fees:
                    #         total_loan_fees += loan_fee
                    #         principal_outstanding += float(loan_fee.amount)
                    # except:
                    #     pass
                    # default_interest_rate = loan_obj.loan_type.interest_rate
                    # if default_interest_rate:
                    #     interest_rate = float(default_interest_rate)
                    # overridden_interest_rate = loan_obj.loan_interest_percentage
                    # if overridden_interest_rate != None:
                    #     interest_rate = float(overridden_interest_rate)
                    # total_repayment_amount_per_schedule = principal_outstanding / duration
                    # try:
                    #     existing_schedules = LoanScheduler.objects.filter(loan = loan).delete()
                    # except:
                    #     pass               
                    # for i in range(1, duration + 1):
                    #     payment_date = current_time
                    #     repayment_schedule = total_repayment_amount_per_schedule + (principal_outstanding * (interest_rate / 100))
                    #     principal_plus_interest += repayment_schedule                    
                    #     if loan_obj.loan_duration_period == 'Days':
                    #         payment_date = current_time + relativedelta(days=i)
                    #     elif loan_obj.loan_duration_period == 'Weeks':
                    #         payment_date = current_time + relativedelta(weeks=i)
                    #     elif loan_obj.loan_duration_period == 'Months':
                    #         payment_date = current_time + relativedelta(months=i)
                    #     else:
                    #         payment_date = current_time + relativedelta(years=i)
                    #     loan_scheduler = LoanScheduler.objects.create(
                    #         loan=loan_obj,
                    #         date=payment_date,
                    #         amount=repayment_schedule,
                    #         status='pending')
                    #     principal_outstanding -= total_repayment_amount_per_schedule
                    #     total_loan_fees = 0.0
                    #     for loan_fee in loan_fees:
                    #         total_loan_fee += loan_fee
                    #     loan_obj.loan_fees = total_loan_fee 
                    #     loan_obj.interest = principal_plus_interest - total_loan_fee
                    # loan_obj.loan_release_date = current_time
                    # loan_obj.interest_start_date = current_time
                    # if loan_obj.loan_duration_period == 'Days':
                    #     loan_obj.maturity_date = current_time + relativedelta(days=duration)
                    # elif loan_obj.loan_duration_period == 'Weeks':
                    #     loan_obj.maturity_date = current_time + relativedelta(weeks=duration)
                    # elif loan_obj.loan_duration_period == 'Months':
                    #     loan_obj.maturity_date= current_time + relativedelta(months=duration)
                    # else:
                    #     loan_obj.maturity_date = current_time + relativedelta(years=duration)
                    # loan_obj.save()               
                    # return Response({"message": "loan has been approved"})
                    return Response({"message": "Pending work to be done on formulae"})








        elif decision == 'decline':
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
            if(the_loan.remaining_balance == 0.00):
                the_loan.status = "fully paid"
            the_loan.amount_paid += amount
            the_loan.remaining_balance -= amount
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
                    unit.paid += int(amount)
                    unit.pending_due -= int(amount)
                    unit.total_due -= int(amount)
                    unit.principal_due -= int(amount)
                    amount = 0
                    unit.save()
                else:
                    unit.status = "settled"
                    unit.paid = unit.due
                    unit.pending_due = 0
                    unit.total_due = 0
                    unit.principal_due = 0
                    amount -= unit.amount
                    unit.amount = 0
                    unit.save()
            else:
                pass
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


class AutomaticRepayment(APIView):
    #directDebit("AUTH_nbd2sdkqkb","lexmill99@gmail.com","500000")
    def post(self, request, pk=None):
        amount = int(request.data.get('amount'))
        loan = request.data.get('loan')
        comment = "Direct Debit"
        repayment_mode = "Wire Transfer"
        payment_type = "card"
        proof_of_payment = request.FILES.get('proof_of_payment')
        # collector = "Not Applicable(Automatic repayment)"
        sent_amount = amount
        the_loan = Loan.objects.get(pk = loan)
        email = the_loan.email
        if email is None:
            return Response({"msg":"pls provide an email address to continue"}, status=status.HTTP_400_BAD_REQUEST)
        if (the_loan.authorization_code == None):
            return Response({"msg":"pls register for direct debit service as you do not have an authorization code"}, status=status.HTTP_400_BAD_REQUEST)
        direct_debit_status = directDebit(the_loan.authorization_code, email , float(amount))
        if (direct_debit_status['data']['status'] != "success"):
            return Response({"msg":"pls retry with better network or verify your account has enough funds"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if(the_loan.amount_paid == None):
                the_loan.amount_paid = 0.00
            if(the_loan.remaining_balance == 0.00):
                the_loan.status = "fully paid"
            the_loan.amount_paid += amount
            the_loan.remaining_balance -= amount
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
                    unit.paid += int(amount)
                    unit.pending_due -= int(amount)
                    unit.total_due -= int(amount)
                    unit.principal_due -= int(amount)
                    if unit.principal_due < 0:
                        unit.principal_due = 0
                    amount = 0
                    unit.save()
                else:
                    unit.status = "settled"
                    unit.paid = unit.due
                    unit.pending_due = 0
                    unit.total_due = 0
                    unit.principal_due = 0
                    amount -= unit.amount
                    unit.amount = 0
                    unit.save()
            else:
                pass
        loan_payment = LoanRepayment.objects.create(
            loan=the_loan,\
            date=datetime.date.today(),\
            amount=sent_amount,\
            repayment_mode = repayment_mode,\
            payment_type = payment_type,\
            proof_of_payment = proof_of_payment,\
            comment = comment
        )
        serializer = LoanSchedulerSerializer(get_schedule, many=True)
        return Response({"msg":"repayment was successful","schedule": serializer.data})


class SaveAuthCode(APIView):
    def post(self, request, pk=None):
        try:
            loan = request.data.get('loan')
            card_number = request.data.get('card_number')
            cvv = request.data.get('cvv')
            month = request.data.get('month')
            year = request.data.get('year')
            loan_instance = Loan.objects.get(pk = int(loan))
            if (loan_instance.email != None):
                email = loan_instance.email
            else:
                return Response({"msg":"pls provide an email address to continue"})
            #ddebitCode("lexmill99@gmail.com", "1.00", "4084084084084081", "408", "02", "22")
            auth_code = ddebitCode(email, "2500", card_number, cvv, month, year)
            loan_instance.authorization_code = auth_code
            loan_instance.save()
            return Response({"msg":"authorization code has been saved and 2500 was deducted from your account"}, status = status.HTTP_200_OK)    
        except:
            return Response({"msg":"charge was not successful, retry with enough balance and good network"}, status=status.HTTP_400_BAD_REQUEST) 



class OverrideLoanMaturity(APIView):
    def post(self, request):
        loan = request.data.get("loan")
        new_date = request.data.get('new_date')
        new_date = parse_date(new_date)
        print(new_date)
        filtered_loan = Loan.objects.get(pk=loan)
        print(filtered_loan)
        loan_schedule = LoanScheduler.objects.filter(date = filtered_loan.maturity_date).get(loan = loan)
        filtered_loan.maturity_date = new_date
        loan_schedule.date = new_date
        filtered_loan.save()
        loan_schedule.save()
        return Response({"Payment date overriden to "+str(new_date)}, status=status.HTTP_200_OK) 
