from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from member.models import Kyc,RewardEarnings,ReffferalEarnings, Transactions, Withdrow,Deposit,WeeklyMemberEarnings,MemberTotalEarnings
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
    refferals = Profile.objects.exclude(recommended_by__isnull=True).filter(is_verified = True)
    if request.method == "POST":
        youtube = request.POST['youtubereffer']
        reffer = request.POST['reffer']
        reffer_obj = AddReward(refer_reward=reffer,youtube_reward=youtube)
        reffer_obj.save()

    context = {
        "youtube":youtube,
        'refferals':refferals
    }
    return render(request, 'trxadmin/reward.html',context)

def refferal_reward_given(request, id):
    recommented_user_profile = Profile.objects.get(id=id)
    recommentedby_user = recommented_user_profile.recommended_by
    print("recommentedby_user",recommentedby_user)
    reward_price_obj = AddReward.objects.all().last()
    print(reward_price_obj.refer_reward)
    Profile.objects.filter(id = id).update(recommended_by_status = True)
    ReffferalEarnings.objects.create(user = recommentedby_user, earnings = reward_price_obj.refer_reward)
    total_earnings_exist = MemberTotalEarnings.objects.filter(user = recommentedby_user).exists()
    if total_earnings_exist:
        total_earnings_obj = MemberTotalEarnings.objects.get(user = recommentedby_user)
        total_earnings_obj.earnings += reward_price_obj.refer_reward
        total_earnings_obj.save()
    else:
        MemberTotalEarnings.objects.create(user = recommentedby_user, earnings = reward_price_obj.refer_reward)
    return redirect('/trxadmin/reward')

def reward_given(request, id):
    user = Reward.objects.get(id = id)
    reward_price_obj = AddReward.objects.all().last()
    RewardEarnings.objects.create(user = user.user, earnings = reward_price_obj.youtube_reward)
    Reward.objects.filter(id=id).update(status="given")
    total_earnings_exist = MemberTotalEarnings.objects.filter(user = user.user).exists()
    if total_earnings_exist:
        total_earnings_obj = MemberTotalEarnings.objects.get(user = user.user)
        total_earnings_obj.earnings += reward_price_obj.youtube_reward
        total_earnings_obj.save()
    else:
        MemberTotalEarnings.objects.create(user = user.user, earnings = reward_price_obj.youtube_reward)
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
    total_deposit = 0
    total_deposit_qs = Deposit.objects.filter(payment_status = "success")
    for deposit in total_deposit_qs:
        total_deposit += deposit.amount
    if request.method == "POST":
        earnings_amount = float(request.POST['earnings_amount'])
        WeeklyEarnings.objects.create(earnings_amount = earnings_amount)
        for percentage in total_deposit_qs:
            member_deposits = Deposit.objects.filter(user = percentage.user)
            for member_deposit_percentage in member_deposits:
                percentage = (member_deposit_percentage.amount*100) / total_deposit
                print(member_deposit_percentage.amount," ", percentage, " ", round(earnings_amount * percentage/100, 3))
                WeeklyMemberEarnings.objects.create(user = member_deposit_percentage.user , amount = round(earnings_amount * percentage/100, 3))
                total_earnings_exist = MemberTotalEarnings.objects.filter(user = member_deposit_percentage.user).exists()
                if total_earnings_exist:
                    total_earnings_obj = MemberTotalEarnings.objects.get(user = member_deposit_percentage.user)
                    total_earnings_obj.earnings += round(earnings_amount * percentage/100, 3)
                    total_earnings_obj.save()
                else:
                    MemberTotalEarnings.objects.create(user = member_deposit_percentage.user, earnings = round(earnings_amount * percentage/100, 3))
    context={
        "is_earning":True,
    }
    return render(request,"trxadmin/earning.html",context)