from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from member.models import Kyc
from home.models import Profile, User
from member.views import profile
from .models import *
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

# from tetheringtron.member.models import Kycform

# Create your views here.


def Trxadmin(request):
    members=Profile.objects.all().count()
    
    context={
        "members":members,
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
    members= Profile.objects.all()
    context={
        "is_member":True,
        "members":members
    }
    return render(request,'trxadmin/member.html',context)
    # return render(request,'trxadmin/member.html',context)

def coindetails(request):
    context={
        "is_coin":True,
    }
    return render(request,'trxadmin/coindetails.html',context)

def announcement(request):
    if request.method == 'POST':
        alert = request.POST['announcement']
        aler_obj = Announcement(Alert=alert)
        aler_obj.save()
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


def kyclist(request):
    kyc_list=Kyc.objects.all()
    context={
        'kyc_list':kyc_list
    }
    return render(request, 'trxadmin/kyclist.html',context)


def kycdetail(request,user_id):
    user_id=User.objects.get(id=user_id)
    user = Kyc.objects.get(user=user_id)
    profile=Profile.objects.get(user=user_id)
    context={
        'kyc_details':user,
        'profile':profile
    }
    return render(request, 'trxadmin/kycdetail.html',context)


def block(request,user_id):
    members= Profile.objects.all()
    block_obj=User.objects.filter(id=user_id).update(member_status=False)
    context={
        "is_member":True,
        "members":members
    }
    
    return render(request,'trxadmin/member.html',context)
    
def unblock(request,user_id):
    members= Profile.objects.all()
    unblock_obj=User.objects.filter(id=user_id).update(member_status=True)
    context={
        "is_member":True,
        "members":members
    }
    
    return render(request,'trxadmin/member.html',context)

@login_required(login_url="/member/login")
def logout_admin(request):
    django_logout(request)
    return redirect('/member/login')