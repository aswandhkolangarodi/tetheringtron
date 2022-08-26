from django.urls import path
from . import views

app_name= 'trxadmin'

urlpatterns = [
    path("dashboard",views.Trxadmin,name='Trxadmin'),
    path("Adminprofile",views.Adminprofile,name='Adminprofile'),
    path("share",views.share,name='share'),
    path("member",views.member,name='member'),
    path("coindetails",views.coindetails,name='coindetails'),
    path("announcement",views.announcement,name='announcement'),
    path("shareprofile",views.shareprofile,name='shareprofile'),
    path("profile",views.memberprofile,name='profile'),
    path("notifications",views.notifications,name='notifications'),
    path("singlenotification",views.singlenotification,name='singlenotification'),
    path("kyclist",views.kyclist,name='kyclist'),
    path("kycdetail/<str:user_id>",views.kycdetail,name='kycdetail'),
    path('block/<str:user_id>', views.block, name="block"),
    path('unblock/<str:user_id>', views.unblock, name="unblock")
]
