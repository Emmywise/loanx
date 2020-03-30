from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


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
