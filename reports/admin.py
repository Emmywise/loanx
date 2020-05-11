from django.contrib import admin
from .models import CalendarEvent, CalendarEventEmail, CalendarLog, LoanReport
# Register your models here.


admin.site.register(CalendarEventEmail)
admin.site.register(CalendarEvent)
admin.site.register(CalendarLog)
admin.site.register(LoanReport)