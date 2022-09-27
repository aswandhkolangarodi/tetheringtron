from django.urls import path
from . import views

app_name= 'trxadmin'

urlpatterns = [
    path("dashboard",views.Trxadmin,name='Trxadmin'),
    path("trade-status-update/<str:id>", views.trade_status_update, name="trade_status_update"),
    path('withdrow-request-status/<str:id>', views.withdrow_request_status , name="withdrow_request_status"),
    path("kyc",views.kyc,name='kyc'),
    path("coindetails",views.coindetails,name='coindetails'),
    path("announcement",views.announcement,name='announcement'),
    path("notifications",views.notifications,name='notifications'),
    path("singlenotification",views.singlenotification,name='singlenotification'),
    path("members",views.members,name='members'),
    path("kycdetail/<str:user_id>",views.kycdetail,name='kycdetail'),
    path('block/<str:user_id>', views.block, name="block"),
    path('unblock/<str:user_id>', views.unblock, name="unblock"),
    path('kyc-approve/<str:user_id>', views.kyc_approove, name="kyc_approve"),
    path('kyc-reject/<str:user_id>', views.kyc_reject, name="kyc_reject"),
    path('logout', views.logout_admin , name='logout_admin'),
    path('reward', views.reward, name='reward'),
    path('contact', views.contact, name='contact'),
    path('reward-given/<str:id>', views.reward_given, name='reward_given'),
    path('refferal-reward-given/<str:id>',views.refferal_reward_given, name="refferal_reward_given"),
    path('reward-reject/<str:id>', views.reward_reject, name='reward_reject'),
    path('earning', views.earning, name='earning'),
    
]
