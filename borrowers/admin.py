from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Borrower)
admin.site.register(BorrowerGroup)
admin.site.register(Membership)
admin.site.register(InviteBorrower)
