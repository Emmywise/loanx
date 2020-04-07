from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(LoanType)
admin.site.register(Loan)
admin.site.register(LoanRepayment)
admin.site.register(LoanDisbursement)
admin.site.register(LoanComment)
admin.site.register(LoanGroup)
admin.site.register(LoanOfficer)
admin.site.register(LoanRemainder)
admin.site.register(LoanFee)
admin.site.register(LoanAttachment)
admin.site.register(LoanCollateral)
admin.site.register(LoanScheduler)
admin.site.register(LoanGuarantor)
admin.site.register(GuarantorFile)
