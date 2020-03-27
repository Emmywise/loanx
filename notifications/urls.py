from .views import *
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/send_sms/', SendSMS.as_view()),
    path('api/send_email/', SendEmail.as_view()),
]


