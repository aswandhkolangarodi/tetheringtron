from multiprocessing.sharedctypes import Value
from statistics import mode
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.helpers import reffer_reward_email_to_member
from trxadmin.models import *
from .models import *
import base64
from django.contrib.auth import logout as django_logout
from django.core.files.base import ContentFile
from django.conf import settings
import stripe
from django.contrib import messages
from datetime import  datetime,date
from django.utils import timezone
import random
from django.db.models import Q
import requests
from .helpers import send_deposit_mail_to_admin,send_withdraw_mail_to_admin
from dateutil.relativedelta import relativedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    today = date.today()
    first_deposit_date = profile.first_deposit_date
    five_year_date = '00/00/0000'
    if first_deposit_date is not None:
        five_year_date = first_deposit_date + relativedelta(days=+1)
        print('five_year_date',five_year_date)
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    kyc_status = Kyc.objects.filter(user=request.user).last()
    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)
    today_transactions = Transactions.objects.filter(Q(deposit_status = "success") | Q(withdrawal_status = "requested"),user=request.user, date__range=(today_min, today_max)).order_by('-date')
    # all_transactions = Transactions.objects.filter(Q(deposit_status = "success") | Q(withdrawal_status = "requested") ,user=request.user).order_by('-date')
    # total earnings 
    total_earnings = MemberTotalEarnings.objects.filter(user = request.user).last()
    # total deposit of a member
    member_refferal_earnings = 0
    reffferal = ReffferalEarnings.objects.filter(user = request.user)
    for refferal_earnings in reffferal:
        member_refferal_earnings += refferal_earnings.earnings

    total_deposit = Deposit.objects.filter(user = user ,payment_status ='success').last()
    
    
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
        # 'all_transactions':all_transactions,
        'total_deposit':total_deposit,
        'total_earnings':total_earnings,
        'member_refferal_earnings':member_refferal_earnings,
        'five_year_date':five_year_date,
        'today':today,
        'is_index':True
    }
    return render(request, 'member/index.html', context)
    

def profile(request):
    if request.method == 'POST':
        img = request.FILES['user_img']
        profile = User.objects.get(email = request.user)
        profile.user_img = img
        profile.save()
        return redirect('/member/profile/')
    return render(request, 'member/profile.html')


def rewards(request):
    user=User.objects.get(email=request.user)
    reward=Profile.objects.get(user=user)
    add_reward = AddReward.objects.all().last()
    member_youtube_reward_exist = Reward.objects.filter(Q(status = "waiting for approval") | Q(status = "given") ,user = user).last()
    if request.method == 'POST':
        youtube = request.POST['youtube']
        if member_youtube_reward_exist:
            return redirect('/member/rewards/')
            
        youtube_obj = Reward(youtube=youtube,user=request.user)
        youtube_obj.save()
        messages.success(request, "Your reward request send successfully")
        return redirect('/member/rewards/')
    context ={
        'is_rewards':True,
        'reward' : reward,
        'add_reward':add_reward,
        'member_youtube_reward_exist':member_youtube_reward_exist
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
        elif kyc_check_last.status == "Waiting for approvel":
            messages.warning(request ,"Your KYC under verification")
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
    all_transactions = Transactions.objects.filter(Q(deposit_status = "success") | Q(withdrawal_status = "requested") ,user=request.user).order_by('-date')
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
                try:
                    amount = int(request.POST['amount'])*100
                    selected_currency = request.POST['currency']
                    live_tron_price_in_usd = requests.get(url = "https://min-api.cryptocompare.com/data/price?fsym=TRX&tsyms=USD").json()
                    tron_value = live_tron_price_in_usd.get('USD')
                    usd_price = requests.get(url = f"https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms={selected_currency}").json()
                    usd_value = usd_price.get(selected_currency)
                    member_deposit_amount_in_usd = round((amount/usd_value)/100 , 3)
                    print('usd_value_in',selected_currency ,' ',usd_value)
                    print('member_deposit_amount_in_usd', member_deposit_amount_in_usd, 'usd')
                    
                    print('tron_value_in_usd', tron_value)
                    member_deposit_amount_in_trx = round(member_deposit_amount_in_usd/tron_value , 3)
                    print('member_deposit_amount_in_trx', member_deposit_amount_in_trx , 'TRX')
                    if member_deposit_amount_in_trx >= 1000:
                        test_id = uuid.uuid4()

                        
                        session = stripe.checkout.Session.create(
                        payment_method_types = ['card'],
                        line_items = [{
                            'price_data':{
                                'currency': selected_currency,
                                'product_data':{
                                    'name':'TRON',
                                    'description':str(member_deposit_amount_in_trx)+" TRX , " +str(member_deposit_amount_in_usd)+ " USD",
                                    
                                },
                                'unit_amount': amount,

                            },
                            'quantity':1,
                        }],
                        mode = 'payment',
                        success_url = f'https://tetheringtron.geany.website/member/success/{test_id}',
                        cancel_url = f'https://tetheringtron.geany.website/member/cancel/{test_id}',
                        )
                        if session:
                            id_generator=str(random.randint(100000000000000,999999999999999))
                            txn_id = "TETHD"+id_generator
                            last_deposit = Deposit.objects.filter(user = request.user, payment_status = "success").last()
                            if last_deposit is None:
                                deposit = Deposit(user = request.user ,test_id = test_id, amount_in_trx= member_deposit_amount_in_trx  ,txn_id = txn_id,amount_in_usd = member_deposit_amount_in_usd ,total_deposit = member_deposit_amount_in_trx)
                                deposit.save()
                                Transactions(user = request.user ,deposit = deposit,test_id = test_id, mode = "deposit").save()
                            else:
                                deposit = Deposit(user = request.user ,test_id = test_id, amount_in_trx= member_deposit_amount_in_trx ,amount_in_usd = member_deposit_amount_in_usd,txn_id = txn_id)
                                deposit.save()
                                Deposit.objects.filter(txn_id = txn_id).update(total_deposit = round(last_deposit.total_deposit + member_deposit_amount_in_trx, 3))
                                Transactions(user = request.user ,deposit = deposit,test_id = test_id, mode = "deposit").save()
                    else:
                        messages.warning(request , "You try to deposit " + str(member_deposit_amount_in_trx)  + " TRX. Minimum deposit amount is 1000 TRX")
                        return redirect('/member/dashboard/')
                except:
                    messages.warning(request, "Something went wrong")
                    return redirect('/member/dashboard/')
        elif kyc_check_last.status == "Waiting for approvel":
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
    amount = str(deposit.amount_in_trx)
    user = Profile.objects.get(user=request.user)
    if user.first_deposit_status == False:
        if user.recommended_by is not None:
            recommented_user = user.recommended_by
            reward_price_obj = AddReward.objects.all().last()
            Profile.objects.filter(user=request.user).update(recommended_by_status = True)
            ReffferalEarnings.objects.create(user = recommented_user, earnings = reward_price_obj.refer_reward)
            reffer_reward_email_to_member(recommented_user, reward_price_obj.refer_reward)
            total_earnings_exist = MemberTotalEarnings.objects.filter(user = recommented_user).exists()
            if total_earnings_exist:
                total_earnings_obj = MemberTotalEarnings.objects.get(user = recommented_user)
                total_earnings_obj.earnings += reward_price_obj.refer_reward
                total_earnings_obj.save()
            else:
                MemberTotalEarnings.objects.create(user = recommented_user, earnings = 
                reward_price_obj.refer_reward)
        Profile.objects.filter(user=request.user).update(first_deposit_status = True, first_deposit_date = date.today())
    Transactions.objects.filter(test_id = test_id).update(deposit_status = "success")
    messages.success(request, "Payment of " + amount + "TRX successfull")
    send_deposit_mail_to_admin(test_id)
    return redirect('/member/dashboard/')

def paymentCancel(request,test_id):
    Deposit.objects.filter(test_id = test_id).update(payment_status = "cancel")
    Transactions.objects.filter(test_id = test_id).update(deposit_status = "cancel")
    return redirect('/member/dashboard/')

def withdraw(request):
    user = request.user
    kyc_check = Kyc.objects.filter(user=user).exists()
    if kyc_check :
        kyc_check_last = Kyc.objects.filter(user = user).last()       
        if kyc_check_last.status == "approved":
            # total earnings
            first_deposit_check = Profile.objects.filter(user = user, first_deposit_status = True)
            if first_deposit_check:
                total_earnings = MemberTotalEarnings.objects.filter(user = user).last()
                bank_details = BankDetails.objects.filter(user = user).last()
                if bank_details:
                    if request.method == "POST":
                        req_amount = float(request.POST['withdraw_amount'])
                        
                        amount_from = request.POST['from']
                        id_generator=str(random.randint(100000000000000,999999999999999))
                        txn_id = "TETH-W"+id_generator
                        if amount_from == 'earnings':
                            if req_amount > total_earnings.earnings:
                                messages.warning(request, "Your account has insufficient funds.Retry after checking your balance")
                                return redirect('/member/dashboard/')
                            else:
                                withdraw = Withdraw(user = user , amount = req_amount, txn_id=txn_id)
                                withdraw.save()
                                total_earnings.earnings -= round(req_amount, 3)
                                total_earnings.save()
                                Transactions(user = user ,withdraw = withdraw , mode = "withdraw",withdrawal_status ="requested" ).save()
                                messages.success(request , "withdraw request is send successfully.The amount will be credited with in 24 houre ")
                                send_withdraw_mail_to_admin(txn_id)
                                return redirect('/member/dashboard/')
                        else:
                            last_deposit = Deposit.objects.filter(user=user, payment_status='success').last()
                            print(last_deposit)
                            if req_amount > last_deposit.total_deposit:
                                messages.warning(request, "Your account has insufficient funds.Retry after checking your balance")
                                return redirect('/member/dashboard/')
                            else:
                                withdraw = Withdraw(user = user , amount = req_amount, txn_id=txn_id)
                                withdraw.save()
                                last_deposit.total_deposit = round(last_deposit.total_deposit - req_amount, 3)
                                last_deposit.save()
                                Transactions(user = user ,withdraw = withdraw , mode = "withdraw",withdrawal_status ="requested" ).save()
                                messages.success(request , "withdraw request is send successfully.The amount will be credited with in 24 houre ")
                                return redirect('/member/dashboard/')
                else:
                    messages.warning(request, "Add your bank details")
                    return redirect('/member/bankdetails')
            else:
                messages.warning(request, "Complte Your first deposit to withdraw your earnings")
        elif kyc_check_last.status == "Waiting for approvel":
            messages.warning(request , "Your KYC under Verification please wait")
        else:
            messages.warning(request , "Your KYC Request is rejected")
    else:
        messages.warning(request, "Complte KYC")
    return redirect('/member/dashboard')

def handler404(request, exception):
    return render(request, "member/404.html", status=404)

def bankdetails(request):
    user = request.user
    bank_details = BankDetails.objects.filter(user=user).last()
    if request.method == "POST":
        bank_name = request.POST['bank_name']
        branch = request.POST['branch']
        account_number = request.POST['account_number']
        swift_code = request.POST['swift_code']
        
        bank_exist = BankDetails.objects.filter(user=user).exists()
        if bank_exist:
            BankDetails.objects.filter(user=user).update(
                bank_name = bank_name,
                branch=branch,
                swift_code =swift_code,
                account_number = account_number,
                )
            messages.success(request, "Bank details updated successfully")
        else:
            BankDetails.objects.create(
                user=user,
                bank_name = bank_name,
                branch=branch,
                swift_code =swift_code,
                account_number = account_number,
            )
            messages.success(request, "Bank details added successfully")
        return redirect('/member/bankdetails')
    context = {
        "is_bankdetails" : True,
        "bank_details":bank_details
    }
    return render(request, "member/bank-details.html",context)

def announcement_is_seen(request,id):
    Announcement.objects.filter(id=id).update(is_seen = True)
    return redirect('/member/dashboard')