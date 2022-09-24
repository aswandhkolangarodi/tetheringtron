from django.contrib import admin

from member.models import *

# Register your models here.

admin.site.register(Kyc)
admin.site.register(Deposit)
admin.site.register(TotalEarnings)
admin.site.register(Withdrow)
admin.site.register(Transactions)