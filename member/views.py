from multiprocessing.sharedctypes import Value
from statistics import mode
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *
from .models import Kyc, MemberTotalEarnings, RewardEarnings, Deposit, WeeklyMemberEarnings,Withdrow,Transactions
import base64
from django.contrib.auth import logout as django_logout
from django.core.files.base import ContentFile
from django.conf import settings
import stripe
from django.contrib import messages
from datetime import  datetime
from django.utils import timezone
import random
from django.db.models import Q
import requests
from .helpers import send_deposit_mail_to_admin

@login_required(login_url="/member/login")
def index(request):
    user=User.objects.get(email=request.user)
    if user.member_status == False:
        django_logout(request)
        return redirect('/')

    reward=Profile.objects.get(user=user)
    alert = Announcement.objects.filter(user = request.user,is_seen =False).last()
    profile=Profile.objects.get(user=user)
    my_recs=profile.get_recommended_profiles()
    recs_count= len(my_recs)
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    kyc_status = Kyc.objects.filter(user=request.user).last()
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    today_transactions = Transactions.objects.filter(Q(deposit_status = "success") | Q(withdrowal_status = "requested"),user=request.user, date__range=(today_min, today_max)).order_by('-date')
    all_transactions = Transactions.objects.filter(Q(deposit_status = "success") | Q(withdrowal_status = "requested") ,user=request.user).order_by('-date')
    # total earnings 
    total_earnings = MemberTotalEarnings.objects.filter(user = request.user).last()
    # total deposit of a member
    total_deposit = 0
    total_deposit_qs = Deposit.objects.filter(user=request.user,payment_status = "success")
    for deposit in total_deposit_qs:
        total_deposit += deposit.amount
    
    trans = Transactions.objects.filter(mode = "deposit").last()
    context ={
        'recs_count':recs_count,
        'user':user,
        'reward' : reward,
        'alert':alert,
        'my_recs':my_recs,
        'kyc_check':kyc_check,
        'kyc_status':kyc_status,
        'transactions':today_transactions,
        'all_transactions':all_transactions,
        'total_deposit':total_deposit,
        'total_earnings':total_earnings,
        'is_index':True
    }
    return render(request, 'member/index.html', context)
    

def profile(request):
    if request.method == 'POST':
        img = request.FILES['user_img']
        print(img)
        profile = User.objects.get(email = request.user)
        profile.user_img = img
        profile.save()
        return redirect('/member/profile/')
    return render(request, 'member/profile.html')


def rewards(request):
    user=User.objects.get(email=request.user)
    reward=Profile.objects.get(user=user)
    add_reward = AddReward.objects.all().last()
    if request.method == 'POST':
        youtube = request.POST['youtube']
        print(youtube)
        youtube_obj = Reward(youtube=youtube,user=request.user)
        youtube_obj.save()
        
    context ={
        'is_rewards':True,
        'reward' : reward,
        'add_reward':add_reward
    }
    return render(request, 'member/rewards.html',context)

def kyc_home(request):
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    if kyc_check is None:
        kyc_check_last = Kyc.objects.filter(user = request.user).last()
        if kyc_check_last.status == "approved":
            return redirect('/member/dashboard/')
    return render(request, 'member/kyc-home.html')

def coin_details(request):
    context ={
        'is_coin_details':True
    }
    return render(request, 'member/coin-details.html',context)

def kyc_main(request):
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    if kyc_check:
        kyc_check_last = Kyc.objects.filter(user = request.user).last()
        if kyc_check_last.status == "approved":
            messages.warning(request ,"KYC already approved")
            return redirect('/member/dashboard/')
    user_id=request.user.id
    print(user_id)
    if request.method == 'POST' and request.FILES:
        country=request.POST['country']
        city =request.POST['city']
        idproof_name=request.POST['idproof_name']
        address=request.POST['address']
        pin=request.POST['pin']
        idproof_document=request.FILES['idproof_document']
        member_image=request.FILES['member_image']
        user=User.objects.get(id=user_id)
        kyc_obj=Kyc(user=user, country=country, address=address, city=city, pin=pin, id_proof=idproof_name, id_proof_file=idproof_document, member_image=member_image, status="Waiting for approvel")
        kyc_obj.save()
        return redirect(f'/member/selfie/')
        
    return render(request, 'member/kycnew.html')

def selfie(request):
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    if kyc_check:
        kyc_check_last = Kyc.objects.filter(user = request.user).last()
        if kyc_check_last.status == "approved":
            messages.warning(request ,"KYC already approved")
            return redirect('/member/dashboard/')
    user=request.user
    if request.method == 'POST':
        image_data = request.POST['imgurl']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name="Username" + '.' + ext)
        image_data = Kyc.objects.filter(user=user).last()
        image_data.live_photo = data
        image_data.save()
        messages.success(request, "KYC Request Send Successfully.Verification take 24 houres")
        return redirect('/member/dashboard')
    return render(request, 'member/selfie.html')

def transactions(request):
    all_transactions = Transactions.objects.filter(Q(deposit_status = "success") | Q(withdrowal_status = "requested") ,user=request.user).order_by('-date')
    context ={
        'is_transactions':True,
        "transactions" : all_transactions
    }
    return render(request, 'member/transactions.html',context)


# #  stripe payment

def create_checkout_session(request):
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    if kyc_check :
        kyc_check_last = Kyc.objects.filter(user = request.user).last()        
        if kyc_check_last.status == "approved":
            if request.method == 'POST':
                amount = int(request.POST['amount'])*100
                selected_currency = request.POST['currency']
                live_tron = requests.get(url = f"https://min-api.cryptocompare.com/data/price?fsym=TRX&tsyms={selected_currency}").json()
                tron_value = live_tron.get(selected_currency)
                print('tron_value',amount/tron_value)
                if amount/(tron_value*100) >= 1000:
                    test_id = uuid.uuid4()
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = [{
                        'price_data':{
                            'currency': selected_currency,
                            'product_data':{
                                'name':'TRON'
                            },
                            'unit_amount': amount,

                        },
                        'quantity':1,
                    }],
                    mode = 'payment',
                    success_url = f'http://127.0.0.1:8000/member/success/{test_id}',
                    cancel_url = f'http://127.0.0.1:8000/member/cancel/{test_id}',
                    )
                    if session:
                        id_generator=str(random.randint(100000000000000,999999999999999))
                        txn_id = "TETH-D"+id_generator
                        last_deposit = Deposit.objects.filter(user = request.user, payment_status = "success").last()
                        if last_deposit is None:
                            deposit = Deposit(user = request.user ,test_id = test_id, amount = round(amount/(100*tron_value), 3)  ,txn_id = txn_id,total_deposit = round(amount/(100*tron_value), 3))
                            deposit.save()
                        else:
                            deposit = Deposit(user = request.user ,test_id = test_id, amount = round(amount/(100*tron_value), 3)  ,txn_id = txn_id)
                            deposit.save()
                            Deposit.objects.filter(txn_id = txn_id).update(total_deposit = last_deposit.total_deposit + round(amount/(100*tron_value), 3))
                            Transactions(user = request.user ,deposit = deposit,test_id = test_id, mode = "deposit").save()
                else:
                    messages.warning(request , "You try to deposit " + str(round(amount/(tron_value*100),3))  + " TRX. Minimum deposit amount is 1000 TRX")
                    return redirect('/member/dashboard/')
        elif kyc_check_last.status == "waiting for approval":
            messages.warning(request , "Your KYC under Verification please wait")
            return redirect('/member/dashboard/')
        else:
            messages.warning(request, "Your KYC verification is rejected")
            return redirect('/member/dashboard/')
    else:
        messages.warning(request, "Complte KYC To Activate Your Wallet")
        return redirect('/member/dashboard/')
    return redirect(session.url, code = 303)

def paymentSuccess(request,test_id):
    deposit = Deposit.objects.filter(test_id = test_id).last()
    deposit.payment_status = "success"
    deposit.save()
    amount = str(deposit.amount)
    Transactions.objects.filter(test_id = test_id).update(deposit_status = "success")
    messages.success(request, "Payment of " + amount + "TRX successfull")
    send_deposit_mail_to_admin(test_id)
    return redirect('/member/dashboard/')

def paymentCancel(request,test_id):
    Deposit.objects.filter(test_id = test_id).update(payment_status = "cancel")
    Transactions.objects.filter(test_id = test_id).update(deposit_status = "cancel")
    return redirect('/member/dashboard/')

def withdraw(request):
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    if kyc_check :
        kyc_check_last = Kyc.objects.filter(user = request.user).last()       
        if kyc_check_last.status == "approved":
            # total earnings 
            total_earnings = MemberTotalEarnings.objects.filter(user = request.user).last()

            if request.method == "POST":
                amount = float(request.POST['withdraw_amount'])
                trx_address = request.POST['trx_address']
                if amount > total_earnings.earnings:
                    messages.warning(request, "Your account has insufficient funds.Retry after checking your balance")
                    return redirect('/member/dashboard/')
                else:
                    id_generator=str(random.randint(10000000000,99999999999999999999))
                    txn_id = "TETH-W"+id_generator
                    withdrow = Withdrow(user = request.user , amount = amount, trx_address = trx_address, txn_id=txn_id)
                    withdrow.save()
                    total_earnings.earnings -= round(amount, 3)
                    total_earnings.save()
                    Transactions(user = request.user ,withdrow = withdrow , mode = "withdrow",withdrowal_status ="requested" ).save()
                    messages.success(request , "Withdrow request is send successfully.The amount will be credited with in 24 houre ")
                    return redirect('/member/dashboard/')
        elif kyc_check_last.status == "Waiting for approvel":
            messages.warning(request , "Your KYC under Verification please wait")
        else:
            messages.warning(request , "Your KYC Request is rejected")
    else:
        messages.warning(request, "Complte KYC")
    return redirect('/member/dashboard')

def handler404(request, exception):
    return render(request, "member/404.html", status=404)

def announcement_is_seen(request,id):
    Announcement.objects.filter(id=id).update(is_seen = True)
    return redirect('/member/dashboard')