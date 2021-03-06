from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser
from rest_framework import status
from rest_framework.views import APIView
from .models import *
import requests
from loans.models import Loan, LoanRepayment
from loans.serializers import LoanSerializer, LoanRepaymentSerializer
from .serializers import *
from savings_investments.models import SavingsAccount
from savings_investments.serializers import SavingsAccountSerializer
import cloudinary.uploader
from loan_management_system import permissions as perms
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets


@api_view(['GET', 'DELETE', 'PATCH'])
def get_delete_update_borrower(request, pk):
    try:
        borrower = Borrower.objects.get(pk=pk)
    except Borrower.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BorrowerSerializer(borrower)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = BorrowerSerializer2(borrower, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        borrower.delete()
        return Response("Borrower deleted successfully", status=204)


@api_view(['GET', 'POST'])
def get_post_borrower(request):
    # get all restaurants
    if request.method == 'GET':
        ref = request.GET.get("borrower_search")
        if ref:
            borrower = Borrower.objects.filter(Q(first_name__startswith=ref) | Q(middle_name__startswith=ref) | Q(last_name__startswith=ref))
            serializer = BorrowerSerializer(borrower, many=True)
            return Response(serializer.data)
        borrowers = Borrower.objects.all()
        serializer = BorrowerSerializer(borrowers, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant
    elif request.method == 'POST':
        data = {
            'profile': request.data.get('profile'),
            'first_name': request.data.get('first_name'),
            'middle_name': request.data.get('middle_name'),
            'last_name': request.data.get('last_name'),
            'business_name': request.data.get('business_name'),
            'gender': request.data.get('gender'),
            'title': request.data.get('title'),
            'mobile': request.data.get('mobile'),
            'email': request.data.get('email'),
            'date_of_birth': request.data.get('date_of_birth'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            'state': request.data.get('state'),
            'zip_code': request.data.get('zip_code'),
            'land_line': request.data.get('land_line'),
            'working_status': request.data.get('working_status'),
            'borrower_photo': request.data.get('borrower_photo'),
            'description': request.data.get('description'),
            'is_activated': request.data.get('is_activated'),
            'borrower_group': request.data.get('borrower_group'),
            'loan_officer': request.data.get('loan_officer')
        }
        if data['borrower_photo'] != '':
            upload_data = cloudinary.uploader.upload(data['borrower_photo'])
            data['borrower_photo'] = upload_data['url']
        print(data['loan_officer'])
        serializer = BorrowerSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowerFileList(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request):
        serializer = BorrowerFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        queryset = Borrower_File.objects.all()
        borrower = self.request.GET.get('borrower')
        # if borrower:
        #     return LoanCollateral.objects.filter(branch=branch)
        borrower_files = Borrower_File.objects.filter(borrowers_id=borrower)
        print(borrower_files)
        serializer = BorrowerFileSerializer(borrower_files, many=True)
        return Response(serializer.data)

class BorrowerFileDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Borrower_File.objects.get(pk=pk)
        except Borrower_File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        borrower_files = self.get_object(pk)
        serializer = BorrowerFileSerializer(borrower_files)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        borrower_files = self.get_object(pk)
        serializer = BorrowerFileSerializer(borrower_files, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        borrower_files = self.get_object(pk)
        borrower_files.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'DELETE', 'PATCH'])
def get_delete_update_borrower_group(request, pk):
    try:
        borrower_group = BorrowerGroup.objects.get(pk=pk)
    except BorrowerGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BorrowerGroupSerializer(borrower_group)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = BorrowerGroupSerializer(borrower_group, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        borrower_group.delete()
        return Response("Borrower group deleted successfully", status=204)


@api_view(['GET', 'POST'])
def get_post_borrower_group(request):
    # get all restaurants
    if request.method == 'GET':
        borrower_groups = BorrowerGroup.objects.all()
        serializer = BorrowerGroupSerializer(borrower_groups, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant
    elif request.method == 'POST':
        data = {
            'group_name': request.data.get('group_name'),
            'group_leader': request.data.get('group_leader'),
            'meeting_date': request.data.get('meeting_date'),
            'description': request.data.get('description'),
        }
        serializer = BorrowerGroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def add_to_group(request):
    # get all restaurants
    if request.method == 'GET':
        membership = Membership.objects.all()
        serializer = MembershipSerializer(membership, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant
    elif request.method == 'POST':
        data = {
            'borrower': request.data.get('borrower'),
            'borrower_group': request.data.get('borrower_group'),

        }
        serializer = MembershipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def SearchBorrowerGroup(request):
    # get all restaurants
    ref = request.GET.get("ref")
    if request.method == 'GET':
        borrower_groups = BorrowerGroup.objects.filter(Q(group_name__startswith=ref))
        serializer = BorrowerGroupSerializer(borrower_groups, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant

@api_view(['GET'])
def IndividualOpenLoans(request):
    id = request.GET.get("id")
    # get all restaurants
    if request.method == 'GET':
        members_loan = []
        borrower_group = BorrowerGroup.objects.get(pk=int(id))
        group_members = borrower_group.members.all()
        for g in group_members:
            member_loan = []
            member_loan = Loan.objects.filter(borrower=g.pk).exclude(status="denied").exclude(status="processing").exclude(status="fully paid")
            if(len(member_loan)>0):
                for unit in member_loan:               
                    members_loan.append(unit)  
            else:
                return Response("No response")  
        serializer = LoanSerializer(members_loan, many=True)
        return Response({unit.borrower.id: serializer.data})

@api_view(['GET'])
def IndividualRepayments(request):
    id = request.GET.get("id")
    # get all restaurants
    if request.method == 'GET':
        total = []
        members_loan = []
        result = []
        borrower_group = BorrowerGroup.objects.get(pk=int(id))
        group_members = borrower_group.members.all()
        for g in group_members:
            member_loan = []
            repayments = []
            member_loan = Loan.objects.filter(borrower=g.pk).exclude(status="denied").exclude(status="processing").exclude(status="fully paid")
            for each_loan in member_loan:
                loan_rts = []
                loan_repayments = LoanRepayment.objects.filter(loan=each_loan)
                if len(loan_repayments) > 0:
                    unit_r = []
                    for each_loan_repayment in loan_repayments:
                        unit_r.append(each_loan_repayment)
                    loan_rts.append({each_loan_repayment.pk: LoanRepaymentSerializer(unit_r, many=True).data})
                total.append(({g.id: loan_rts}))

            # if(len(member_loan)>0):
            #     for unit in member_loan:               
        #             members_loan.append(unit)  
        #     else:
        #         return Response("No response")  
        # serializer = LoanSerializer(members_loan, many=True)
        return Response(total)


@api_view(['GET'])
def BorrowersSavings(request):
    id = request.GET.get("id")
    if request.method == 'GET':
        saving_account = []
        borrower = Borrower.objects.filter(pk=int(id))[0]
        print(Borrower.objects.filter(pk=int(id)))
        print(Borrower.objects.filter(pk=int(id))[0])
        savings_account = SavingsAccount.objects.filter(profile=borrower.profile.pk)
        serializer = SavingsAccountSerializer(savings_account, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def SearchByWorkingStatus(request, status=None):
    #id = request.GET.get("id")
    # get all restaurants
    if request.method == 'GET':
        #members_loan = []
        borrower = Borrower.objects.filter(working_status = status)
        # for unit in borrower_group:
        #     print(unit.member)
        #     members_loan.append(unit.member)
        #print(members_loan)
        # members = borrower_group.member
        # print(members)
        serializer = BorrowerSerializer(borrower, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def MembersOfGroupLoans(request, pk=None):
    if request.method == 'GET':
        borrower = Borrower.objects.filter(pk=pk)
        serializer = SavingsAccountSerializer(savings_account, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_invite_borrower(request, pk):
    try:
        invite_borrower = InviteBorrower.objects.get(pk=pk)
    except InviteBorrower.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = InviteBorrowerSerializer(invite_borrower)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = InviteBorrowerSerializer(invite_borrower, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        invite_borrower.delete()
        return Response("Prospective Borrower deleted successfully", status=204)


@api_view(['GET', 'POST'])
def get_post_invite_borrower(request):
    # get all restaurants
    if request.method == 'GET':
        invite_borrower = InviteBorrower.objects.all()
        serializer = InviteBorrowerSerializer(invite_borrower, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant
    elif request.method == 'POST':
        data = {
            'email_address': request.data.get('email_address'),
        }
        serializer = InviteBorrowerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)