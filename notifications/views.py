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
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from celery import shared_task


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
            return {"message": "Success", "status": status.HTTP_200_OK}
        except:
            return {"message": "Failed", "status": status.HTTP_400_BAD_REQUEST}

class SendEmail(APIView):
    def send_mail(self, purpose, sender, recepient):
        try:
            subject, from_email, to = purpose, \
                                    sender, recepient
            text_content = 'Hey please reset password'
            html_content = '<p>Hey please reset password .' \
                        '</p>' 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return {"message": "Success", "status":status.HTTP_200_OK}
        except:
            return {"message": "Failed", "status":status.HTTP_400_BAD_REQUEST}

    def post(self, request):
        recepient = request.data.get("recepient")
        sender = request.data.get("sender")
        purpose = request.data.get("purpose")
        #msg_status = SendSMSAPI(recepient, sender) 
        #self.send_mail
        #return Response({"message": "Success"}, status=status.HTTP_200_OK)
        return Response(self.send_mail(purpose, sender, recepient), status=status.HTTP_201_CREATED)
        # try:
        #     if msg_status == True:
        #         message = SMS.objects.create(status="sent", message_purpose=purpose)
        #         message.save()
        #     return Response({"message": "Success"}, status=status.HTTP_200_OK)
        # except:
        #     return Response({"message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
        


