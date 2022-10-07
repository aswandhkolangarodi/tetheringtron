from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from member.models import *
from home.models import Contact, Profile, Reward, User
from member.views import profile, transactions
from .models import *
from django.contrib.auth import logout as django_logout
from django.utils import timezone
from datetime import  datetime
from django.contrib.auth.decorators import user_passes_test
from .helpers import reffer_reward_email_to_member, weekly_reward_email_to_member, youtube_reward_email_to_member,youtube_reward_reject_email_to_member
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def Trxadmin(request):
    members=Profile.objects.all().count()
    withdraw_req = Withdraw.objects.all()
    deposit_list = Transactions.objects.filter(deposit_status = "success", mode = "deposit")
    total_deposit = 0
    total_deposit_qs = Deposit.objects.filter(payment_status = "success")
    for deposits in total_deposit_qs:
        total_deposit += deposits.amount_in_trx
    total_earnings = 0
    total_earnings_obj = WeeklyEarnings.objects.all()
    for earnings in total_earnings_obj:
        total_earnings += earnings.earnings_amount
    print(total_earnings)
    context={
        "members":members,
        "total_deposit":total_deposit,
        'total_earnings':total_earnings,
        "deposit_list":deposit_list,
        "withdraw_req":withdraw_req,
        "is_index":True,
    }

        
    return render(request,'trxadmin/index.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def member_bank_details(request, id):
    withdraw_req_member_details = Withdraw.objects.get(id=id)
    bank_details = BankDetails.objects.filter(user=withdraw_req_member_details.user).last()
    return render(request, 'trxadmin/single-bank-details.html',{'bank_details':bank_details})

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
@csrf_exempt
def withdraw_req_reject(request):
    id = request.POST['id']
    reson = request.POST['reson']
    withdrow_obj = Withdraw.objects.filter(id=id).update(status="rejected", reject_reson = reson)
    withdraw = Withdraw.objects.get(id=id)
    print('user',withdraw.user,"amount",withdraw.amount )
    total_earnings = MemberTotalEarnings.objects.get(user = withdraw.user)
    print(total_earnings)
    total_earnings.earnings += withdraw.amount
    total_earnings.save()
    return redirect('/trxadmin/dashboard')
    
@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def trade_status_update(request, id):
    transaction_obj = Transactions.objects.filter(id = id).last()
    transaction_obj.deposit.trade_status = True
    transaction_obj.deposit.save()
    return redirect('/trxadmin/dashboard')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def withdraw_request_status(request, id):
    Withdraw.objects.filter(id=id).update(status = "given")
    return redirect('/trxadmin/dashboard')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def kyc(request):
    members= Kyc.objects.all()
    context={
        "is_kyc":True,
        "members":members
    }
    return render(request,'trxadmin/kyc.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def coindetails(request):
    context={
        "is_coin":True,
    }
    return render(request,'trxadmin/coindetails.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
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

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def notifications(request):
    return render(request, 'trxadmin/notifications.html')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def singlenotification(request):
    return render(request, 'trxadmin/singlenotification.html')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def reward(request):
    youtube = Reward.objects.all()
    refferals = Profile.objects.exclude(recommended_by__isnull=True).filter(is_verified = True, first_deposit_status =True)  
    print(refferals)
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

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def refferal_reward_given(request, id):
    recommented_user_profile = Profile.objects.get(id=id)
    recommentedby_user = recommented_user_profile.recommended_by
    print("recommentedby_user",recommentedby_user)
    reward_price_obj = AddReward.objects.all().last()
    print(reward_price_obj.refer_reward)
    Profile.objects.filter(id = id).update(recommended_by_status = True)
    ReffferalEarnings.objects.create(user = recommentedby_user, earnings = reward_price_obj.refer_reward)
    reffer_reward_email_to_member(recommentedby_user, reward_price_obj.refer_reward)
    total_earnings_exist = MemberTotalEarnings.objects.filter(user = recommentedby_user).exists()
    if total_earnings_exist:
        total_earnings_obj = MemberTotalEarnings.objects.get(user = recommentedby_user)
        total_earnings_obj.earnings += reward_price_obj.refer_reward
        total_earnings_obj.save()
    else:
        MemberTotalEarnings.objects.create(user = recommentedby_user, earnings = 
        reward_price_obj.refer_reward)
    return redirect('/trxadmin/reward')


@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def reward_given(request, id):
    user = Reward.objects.get(id = id)
    reward_price_obj = AddReward.objects.all().last()
    RewardEarnings.objects.create(user = user.user, earnings = reward_price_obj.youtube_reward)
    Reward.objects.filter(id=id).update(status="given")
    youtube_reward_email_to_member(user.user, reward_price_obj.youtube_reward)
    total_earnings_exist = MemberTotalEarnings.objects.filter(user = user.user).exists()
    if total_earnings_exist:
        total_earnings_obj = MemberTotalEarnings.objects.get(user = user.user)
        total_earnings_obj.earnings += reward_price_obj.youtube_reward
        total_earnings_obj.save()
    else:
        MemberTotalEarnings.objects.create(user = user.user, earnings = reward_price_obj.youtube_reward)
    return redirect('/trxadmin/reward')


# def reward_given(request):
#     id = request.GET['id']
#     user = Reward.objects.get(id = id)
#     reward_price_obj = AddReward.objects.all().last()
#     RewardEarnings.objects.create(user = user.user, earnings = reward_price_obj.youtube_reward)
#     Reward.objects.filter(id=id).update(status="given")
#     # youtube_reward_email_to_member(user.user, reward_price_obj.youtube_reward)
#     total_earnings_exist = MemberTotalEarnings.objects.filter(user = user.user).exists()
#     if total_earnings_exist:
#         total_earnings_obj = MemberTotalEarnings.objects.get(user = user.user)
#         total_earnings_obj.earnings += reward_price_obj.youtube_reward
#         total_earnings_obj.save()
#     else:
#         MemberTotalEarnings.objects.create(user = user.user, earnings = reward_price_obj.youtube_reward)
#     return JsonResponse({'status':'success'})

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
@csrf_exempt
def reward_reject(request):
    id = request.POST['id']
    reson = request.POST['reson']
    print(id, reson)
    Reward.objects.filter(id=id).update(status="rejected", reject_reson = reson)
    reward_obj = Reward.objects.get(id=id)
    youtube_reward_reject_email_to_member(reward_obj.user, reson , reward_obj.youtube)
    return redirect('/trxadmin/reward')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def members(request):
    members=Profile.objects.all()
    context={
        'members':members
    }
    return render(request, 'trxadmin/members.html',context)


@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
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


@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def block(request,user_id):
    block_obj=User.objects.filter(id=user_id).update(member_status=False)
    return redirect('/trxadmin/members')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")    
def unblock(request,user_id):
    unblock_obj=User.objects.filter(id=user_id).update(member_status=True)
    return redirect('/trxadmin/members')
    

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def kyc_approove(request, user_id):
    user=Kyc.objects.filter(id=user_id).update(status="approved")
    return redirect('/trxadmin/kyc')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def kyc_reject(request, user_id):
    if request.method == "POST":
        reson = request.POST['reson']
        user=Kyc.objects.filter(id=user_id).update(status="rejected", reson=reson)
    return redirect('/trxadmin/kyc')

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def logout_admin(request):
    django_logout(request)
    return redirect('/member/login')


@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def contact(request):
    contact = Contact.objects.all()
    context = {
        "is_contact":True,
        "contact" : contact
    }
    return render(request,'trxadmin/enquiry.html',context)

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def handler404(request, exception):
    return render(request, "member/404.html", status=404)

@user_passes_test(lambda u: u.is_superuser,login_url="/member/login")
def earning(request):
    total_deposit = 0
    weekly_earnings_obj = WeeklyEarnings.objects.all().order_by('-id')
    total_deposit_qs = Deposit.objects.filter(payment_status = "success")
    for deposit in total_deposit_qs:
        total_deposit += deposit.amount_in_trx
    deposit_members = []
    for deposit_member in total_deposit_qs:
        deposit_members.append(deposit_member.user)
    duplicated_deposit_members = [*set(deposit_members)]
    if request.method == "POST":
        earnings_amount_in_usd = float(request.POST['earnings_amount'])
        WeeklyEarnings.objects.create(earnings_amount = earnings_amount_in_usd)
        live_tron_price_in_usd = requests.get(url = "https://min-api.cryptocompare.com/data/price?fsym=TRX&tsyms=USD").json()
        tron_value = live_tron_price_in_usd.get('USD')
        earnings_amount_in_usd_covert_to_trx = earnings_amount_in_usd/tron_value
        print('earnings_amount_in_usd_covert_to_trx', earnings_amount_in_usd_covert_to_trx)
        for member in duplicated_deposit_members:
            member_total_deposit = Deposit.objects.filter(user = member).last()
            member_deposit_percentage = member_total_deposit.total_deposit / total_deposit*100
            print(member,' percentage ',member_deposit_percentage)
            weekly_member_earnings = float(earnings_amount_in_usd_covert_to_trx) * member_deposit_percentage/100
            print('weekly_member_earnings_in 100 percent', weekly_member_earnings)
            weekly_member_earnings_in_five_percent = round(weekly_member_earnings * 5/100, 3)
            print(member,' 5% : ',weekly_member_earnings_in_five_percent)
            WeeklyMemberEarnings.objects.create(user = member , amount = weekly_member_earnings_in_five_percent)
            weekly_reward_email_to_member(member, weekly_member_earnings_in_five_percent)
            total_earnings_exist = MemberTotalEarnings.objects.filter(user = member).exists()
            if total_earnings_exist:
                total_earnings_obj = MemberTotalEarnings.objects.get(user = member)
                total_earnings_obj.earnings += weekly_member_earnings_in_five_percent
                total_earnings_obj.save()
            else:
                MemberTotalEarnings.objects.create(user = member, earnings = weekly_member_earnings_in_five_percent)
    context={
        "is_earning":True,
        "weekly_earnings_obj":weekly_earnings_obj
    }
    return render(request,"trxadmin/earning.html",context)