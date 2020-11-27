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
# from .send_sms import SendSMSAPI
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from celery import shared_task

from .tasks import send_sms, send_mail_task


# Create your views here.
class SendSMS(APIView):
	def post(self, request):
		#url = 'https://comms.tcore.online/api/v1/sms/send'
		recepient = request.data.get('recepient')
		sender = request.data.get('sender')
		purpose = request.data.get('purpose')
		body = request.data.get('body')
		datum = {
			"to": recepient,
			"message": body,
		}
		headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
		datum = json.dumps(datum)
		res = requests.post(url, data=datum, headers=headers)
		# print(res.json())
		# msg_status = SendSMSAPI(recepient, sender, body)
		if purpose == None:
			purpose = 'to_all_borrowers'
		data = {
			'message_purpose': purpose,
			'status': 'sent'
		}
		serializer = SendSMSSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(res.json(), status=status.HTTP_200_OK)
		else:
			return Response({'error': 'Try again.'}, status=status.HTTP_400_BAD_REQUEST)
		# if res.status_code == 200:
		#     message = SMS.objects.create(status="sent", message_purpose=purpose)
		#     message.save()
		#     return Response({"message": "Success", "status": status.HTTP_200_OK})
		# else:
		#     return Response({"message": "Failed", "status": status.HTTP_400_BAD_REQUEST})

		# print(res.status)


class SendEmail(APIView):
	def post(self, request):
		url = 'https://comms.tcore.online/api/v1/generic/sendmail/mail'
		recepient = request.data.get('recepient')
		sender = request.data.get('sender')
		subject = request.data.get('subject')
		body = request.data.get('body')
		sender = request.data.get('sender')
		name = request.data.get('name')
		email = request.data.get('emal')
		datum = {
			"subject" : subject,
			"html_content" : body,
			"to" : recepient,
			"from" : {
				'name': 'loanx',
				'email': 'adefia.emmywise@gmail.com',
			},
		}

		headers = {
			'Content-Type' : 'application/json',
			'Accept' : 'application/json'
		}
		datum = json.dumps(datum)
		res = requests.post(url, data=datum, headers=headers)
		data = {
			'subject': subject,
			'status': 'sent'
		}

		serializer = SendEmailSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(res.json(), status=status.HTTP_200_OK)
		else:
			return Response({'error': 'Try again.'}, status=status.HTTP_400_BAD_REQUEST)

	# def send_mail(self, purpose, sender, recepient):
	# 	try:
	# 		pass
	# 	except:
	# 		pass
	# #        subject, from_email, to = purpose, \
	#                                 sender, recepient
	#         text_content = 'Hey please reset password'
	#         html_content = '<p>Hey please reset password .' \
	#                     '</p>'
	#         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	#         msg.attach_alternative(html_content, "text/html")
	#         msg.send()
	#         return {"message": "Success", "status":status.HTTP_200_OK}
	#     except:
	#         return {"message": "Failed", "status":status.HTTP_400_BAD_REQUEST}

	# def post(self, request):
	#     recepient = request.data.get("recepient")
	#     sender = request.data.get("sender")
	#     purpose = request.data.get("purpose")
	#     return Response(self.send_mail(purpose, sender, recepient), status=status.HTTP_201_CREATED)