from django.contrib import admin

from member.models import *

# Register your models here.

admin.site.register(Kyc)
admin.site.register(Deposit)
admin.site.register(RewardEarnings)
admin.site.register(Withdraw)
admin.site.register(Transactions)
admin.site.register(WeeklyMemberEarnings)
admin.site.register(MemberTotalEarnings)
admin.site.register(ReffferalEarnings)
admin.site.register(BankDetails)