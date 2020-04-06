from django.shortcuts import render
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status

from .models import *
from loans.models import Loan
from .serializers import *
from savings_investments.models import SavingsAccount
from savings_investments.serializers import SavingsAccountSerializer
import cloudinary.uploader

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_borrower(request, pk):
    try:
        borrower = Borrower.objects.get(pk=pk)
    except Borrower.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single restaurant
    if request.method == 'GET':
        serializer = RestaurantSerializer(borrower)
        return Response(serializer.data)
    # delete a single restaurant
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single restaurant
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_borrower(request):
    # get all restaurants
    if request.method == 'GET':
        ref = request.GET.get("borrower_search")
        if ref:
            borrower = Borrower.objects.filter(Q(first_name__startswith=ref) | Q(last_name__startswith=ref))
            serializer = BorrowerSerializer(borrower, many=True)
            return Response(serializer.data)
        borrowers = Borrower.objects.all()
        serializer = BorrowerSerializer(borrowers, many=True)
        return Response(serializer.data)
    # insert a new record for a restaurant
    elif request.method == 'POST':
        data = {
            'user': request.data.get('user'),
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
            'borrower_group': request.data.get('borrower_group')
        }
        print(data['borrower_photo'])
        upload_data = cloudinary.uploader.upload(data['borrower_photo'])
        data['borrower_photo'] = upload_data['url']
        print(data)
        serializer = BorrowerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_borrower_group(request, pk):
    try:
        borrower_group = BorrowerGroup.objects.get(pk=pk)
    except BorrowerGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BorrowerGroupSerializer(borrower)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        return Response({})
    elif request.method == 'PUT':
        return Response({})


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
        group_members = borrower_group.member.all()
        for g in group_members:
            member_loan = []
            print(".......")
            print(".......")  
            print(g)
            print(".......")
            print(".......")  
            member_loan = Loan.objects.filter(borrower=g.pk)
            #print(member_loan[0])
            for unit in member_loan:
                member_loan.append(unit[0].pk)    
            print(".......")
            print(".......")  
            #print(unit.member)
            #members_loan.append(unit.member)
        #print(members_loan)
        # members = borrower_group.member
        # print(members)
        serializer = BorrowerGroupSerializer(members_loan, many=True)
        return Response(serializer.data)


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


# @api_view(['GET'])
# def BorrowersFiles(request, pk=None):
#     #id = request.GET.get("id")
#     # get all restaurants
#     if request.method == 'GET':
#         #members_loan = []
#         borrower = Borrower.objects.filter(working_status = status)
#         # for unit in borrower_group:
#         #     print(unit.member)
#         #     members_loan.append(unit.member)
#         #print(members_loan)
#         # members = borrower_group.member
#         # print(members)
#         serializer = BorrowerSerializer(borrower, many=True)
#         return Response(serializer.data)

@api_view(['GET'])
def MembersOfGroupLoans(request, pk=None):
    if request.method == 'GET':
        borrower = Borrower.objects.filter(pk=pk)
        serializer = SavingsAccountSerializer(savings_account, many=True)
        return Response(serializer.data)