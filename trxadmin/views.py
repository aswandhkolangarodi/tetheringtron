from multiprocessing import context
from django.shortcuts import render
from member.models import Kyc
# from tetheringtron.member.models import Kycform

# Create your views here.


def Trxadmin(request):
    
    context={
        "is_index":True,
    }

        
    return render(request,'trxadmin/index.html',context)

def base(request):
    return render(request,'trxadmin/base.html')


def Adminprofile(request):
    return render(request,'trxadmin/profile.html')

def share(request):
    context={
        "is_share":True,
    }
    return render(request,'trxadmin/share.html',context)

def member(request):
    posts = Kyc.objects.all().order_by('-id')
    context={
        "is_member":True,
    }
    return render(request,'trxadmin/member.html',context,{'posts':posts})

def coindetails(request):
    context={
        "is_coin":True,
    }
    return render(request,'trxadmin/coindetails.html',context)

def announcement(request):
    context={
        "is_announcement":True,
    }
    return render(request, 'trxadmin/announcement.html',context)

def shareprofile(request):
    
    return render(request, 'trxadmin/shareprofile.html')

def memberprofile(request):
    return render(request, 'trxadmin/member profile.html')

def notifications(request):
    return render(request, 'trxadmin/notifications.html')

def singlenotification(request):
    return render(request, 'trxadmin/singlenotification.html')