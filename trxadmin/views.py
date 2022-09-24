from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from member.models import Kyc,TotalEarnings, Transactions, Withdrow,Deposit
from home.models import Contact, Profile, Reward, User
from member.views import profile, transactions
from .models import *
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import  datetime

def Trxadmin(request):
    members=Profile.objects.all().count()
    withdrow_req = Withdrow.objects.all()
    deposit_list = Transactions.objects.filter(deposit_status = "success", mode = "deposit")
    total_deposit = 0
    total_deposit_qs = Deposit.objects.filter(payment_status = "success")
    for deposits in total_deposit_qs:
        total_deposit += deposits.amount
    context={
        "members":members,
        "total_deposit":total_deposit,
        "deposit_list":deposit_list,
        "withdrow_req":withdrow_req,
        "is_index":True,
    }

        
    return render(request,'trxadmin/index.html',context)


def trade_status_update(request, id):
    transaction_obj = Transactions.objects.filter(id = id).last()
    transaction_obj.deposit.trade_status = True
    transaction_obj.deposit.save()
    return redirect('/trxadmin/dashboard')


def withdrow_request_status(request, id):
    Withdrow.objects.filter(id=id).update(status = "given")
    return redirect('/trxadmin/dashboard')

def kyc(request):
    members= Kyc.objects.all()
    context={
        "is_kyc":True,
        "members":members
    }
    return render(request,'trxadmin/kyc.html',context)

def coindetails(request):
    context={
        "is_coin":True,
    }
    return render(request,'trxadmin/coindetails.html',context)

def announcement(request):
    announcement = Announcement.objects.filter().order_by('-id')
    users = Profile.objects.all()
    if request.method == 'POST':
        Announcement.objects.all().delete()
        alert = request.POST['announcement']
        for user in users:
            aler_obj = Announcement(Alert=alert, user = user.user)
            aler_obj.save()
    context={
        "is_announcement":True,
        "announcement":announcement
    }
    return render(request, 'trxadmin/announcement.html',context)

def notifications(request):
    return render(request, 'trxadmin/notifications.html')

def singlenotification(request):
    return render(request, 'trxadmin/singlenotification.html')

def reward(request):
    youtube = Reward.objects.all()
    if request.method == "POST":
        youtube = request.POST['youtubereffer']
        reffer = request.POST['reffer']
        reffer_obj = AddReward(refer_reward=reffer,youtube_reward=youtube)
        reffer_obj.save()

    context = {
        "youtube":youtube
    }
    return render(request, 'trxadmin/reward.html',context)

def reward_given(request, id):
    user = Reward.objects.get(id = id)
    total_earnings_obj = TotalEarnings.objects.filter(user = user.user).last()
    if total_earnings_obj is None:
        TotalEarnings.objects.create(user = user.user, earnings = 0)
    total_earnings= TotalEarnings.objects.filter(user = user.user).last()
    reward_price_obj = AddReward.objects.all().last()
    total_earnings.earnings += float(reward_price_obj.youtube_reward)
    total_earnings.save()
    Reward.objects.filter(id=id).update(status="given")
    return redirect('/trxadmin/reward')

def reward_reject(request, id):
    Reward.objects.filter(id=id).update(status="rejected")
    return redirect('/trxadmin/reward')

def members(request):
    members=Profile.objects.all()
    context={
        'members':members
    }
    return render(request, 'trxadmin/members.html',context)


def kycdetail(request,user_id):
    user_kyc=User.objects.get(id=user_id)
    # print('user',user)
    kyc = Kyc.objects.filter(user=user_kyc).last()
    profile=Profile.objects.get(user=user_kyc)
    context={
        'kyc_details':kyc,
        'profile':profile,
        
    }
    return render(request, 'trxadmin/kycdetail.html',context)


def block(request,user_id):
    block_obj=User.objects.filter(id=user_id).update(member_status=False)
    return redirect('/trxadmin/members')
    
def unblock(request,user_id):
    unblock_obj=User.objects.filter(id=user_id).update(member_status=True)
    return redirect('/trxadmin/members')
    

def kyc_approove(request, user_id):
    user=Kyc.objects.filter(id=user_id).update(status="approved")
    return redirect('/trxadmin/kyc')

def kyc_reject(request, user_id):
    if request.method == "POST":
        reson = request.POST['reson']
        user=Kyc.objects.filter(id=user_id).update(status="rejected", reson=reson)
    return redirect('/trxadmin/kyc')

@login_required(login_url="/member/login")
def logout_admin(request):
    django_logout(request)
    return redirect('/member/login')


def contact(request):
    contact = Contact.objects.all()
    context = {
        "is_contact":True,
        "contact" : contact
    }
    return render(request,'trxadmin/enquiry.html',context)

def handler404(request, exception):
    return render(request, "member/404.html", status=404)

def earning(request):
    context={
        "is_earning":True,
    }
    return render(request,"trxadmin/earning.html",context)