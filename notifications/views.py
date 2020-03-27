from django.shortcuts import render
import json
import requests
import hashlib
import datetime
from random import randint
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from .models import SMS
from .send_sms import SendSMSAPI

# Create your views here.
class SendSMS(APIView):
    def post(self, request):
        serializer_class = SendSMSSerializer
        recepient = request.data.get("recepient")
        sender = request.data.get("sender")
        purpose = request.data.get("purpose")
        msg_status = SendSMSAPI(recepient, sender) 
        try:
            if msg_status == True:
                message = SMS.objects.create(status="sent", message_purpose=purpose)
                message.save()
            return Response({"message": "Success"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


        
