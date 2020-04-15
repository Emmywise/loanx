from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(SavingsAccount)
admin.site.register(CashSafeManagement)
admin.site.register(CashSource)
admin.site.register(TransferCash)
admin.site.register(Teller)
admin.site.register(SavingsProduct)