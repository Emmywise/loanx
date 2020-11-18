from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Profile)
admin.site.register(Branch)
admin.site.register(BranchAdmin)
admin.site.register(BranchHoliday)
admin.site.register(Country)
admin.site.register(SuspendedAccount)