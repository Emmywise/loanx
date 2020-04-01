from django.contrib import admin
from .models import CalendarEvent, CalendarEventEmail, CalendarLog
# Register your models here.


admin.site.register(CalendarEventEmail)
admin.site.register(CalendarEvent)
admin.site.register(CalendarLog)
