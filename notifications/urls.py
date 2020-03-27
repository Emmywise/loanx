from .views import *
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/send_sms/', SendSMS.as_view()),
]


