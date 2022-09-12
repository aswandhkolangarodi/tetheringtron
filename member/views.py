from email import message
from multiprocessing import context
from unittest import result
from django import views
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *
from .models import Kyc, Transaction
from .forms import KycForm
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
# create transaction imports

from .pyCoinPayments import CoinPayments


@login_required(login_url="/member/login")
def index(request):
    user=User.objects.get(email=request.user)
    alert = Announcement.objects.filter().order_by('-id')
    profile=Profile.objects.get(user=user)
    my_recs=profile.get_recommended_profiles()
    recs_count= len(my_recs)
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    kyc_status = Kyc.objects.filter(user=request.user).last()
# create transaction
    # if request.method == "POST":
    #     test_id=uuid.uuid4()
    #     amount = request.POST['amount']
    #     currency2 = request.POST['currency1']
    #     crypto_client = CoinPayments(settings.COINPAYMENT_PUBLICKEY,settings.COINPAYMENT_PRIVATEKEY)
    #     create_transaction_params = {
    #     'amount' : amount,
    #     'currency1' : currency2,
    #     'currency2' : 'TRX',
    #     'buyer_email': request.user,
    #     'success_url': 'http://127.0.0.1:8000/member/success/{test_id}',
    #     'cancel_url': 'http://127.0.0.1:8000/member/cancel/{test_id}'

        
    #     }
    #     transaction= crypto_client.create_transaction(create_transaction_params)
    #     transaction_log=Transaction(user=request.user,amount=transaction['result']['amount'],address=transaction['result']['address'],txn_id=transaction['result']['txn_id'],test_id=test_id)
    #     transaction_log.save()
    #     return redirect(f"{transaction['result']['checkout_url']}")

    context ={
        'recs_count':recs_count,
        'user':user,
        'alert':alert,
        'my_recs':my_recs,
        'kyc_check':kyc_check,
        'kyc_status':kyc_status,
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

def transactions(request):
    context ={
        'is_transactions':True
    }
    return render(request, 'member/transactions.html',context)

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
    return render(request, 'member/kyc-home.html')

def coin_details(request):
    context ={
        'is_coin_details':True
    }
    return render(request, 'member/coin-details.html',context)

def kyc_main(request):
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
    user=request.user
    
    if request.method == 'POST':
        image_data = request.POST['imgurl']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name="Username" + '.' + ext)
        
        image_data = Kyc.objects.filter(user=user).last()
        image_data.live_photo = data
        image_data.save()
        return redirect('/member/dashboard')
    return render(request, 'member/selfie.html')



def payment_success(request,test_id):
    transactions_log=Transaction.objects.filter(test_id=test_id).update(payment_status="success")
    return redirect('/member/dashboard')


def payment_cancel(request,test_id):
    transactions_log=Transaction.objects.filter(test_id=test_id).update(payment_status="cancel")
    return redirect('/member/dashboard')


 