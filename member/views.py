from email import message
from multiprocessing import context
from django import views
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *
from .models import Kyc
from .forms import KycForm
import base64
from django.core.files.base import ContentFile
from django.conf import settings


# create transaction imports

from .pyCoinPayments import CoinPayments


@login_required(login_url="/member/login")
def index(request):

    user=User.objects.get(email=request.user)
    
    alert = Announcement.objects.filter().order_by('-id')
    # kyc_obj=Kyc.objects.get(user=user)
    # if kyc_obj is None:
    #     message.success('Complete KYC to live on Tethering Tron')
    #     return redirect('/member/kyc')
    profile=Profile.objects.get(user=user)
    my_recs=profile.get_recommended_profiles()
    recs_count= len(my_recs)
# create transaction
    if request.method == "POST":
        amount = request.POST['amount']
        currency1 = request.POST['currency1']
   
        crypto_client = CoinPayments(settings.COINPAYMENT_PUBLICKEY,settings.COINPAYMENT_PRIVATEKEY)
        create_transaction_params = {
        'amount' : amount,
        'currency1' : currency1,
        'currency2' : 'TRX',
        'buyer_email': request.user
        }
        transaction= crypto_client.create_transaction(create_transaction_params)
        print(transaction)
        return render(f"/{transaction.result.checkout_url}")

    context ={
        'recs_count':recs_count,
        'user':user,
        'alert':alert,
        'my_recs':my_recs,
        'is_index':True
    }
    return render(request, 'member/index.html', context)
    

def profile(request):
    return render(request, 'member/profile.html')

def transactions(request):
    context ={
        'is_transactions':True
    }
    return render(request, 'member/transactions.html',context)

def rewards(request):
    user=User.objects.get(email=request.user)
    reward=Profile.objects.get(user=user)
    if request.method == 'POST':
        youtube = request.POST['youtube']
        print(youtube)
        youtube_obj = Reward(youtube=youtube,user=request.user)
        youtube_obj.save()
        
    context ={
        'is_rewards':True,
        'reward' : reward,
        
        
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
        kyc_obj=Kyc(user=user, country=country, address=address, city=city, pin=pin, id_proof=idproof_name, id_proof_file=idproof_document, member_image=member_image)
        kyc_obj.save()
        return redirect(f'/member/selfie/{user_id}')
    return render(request, 'member/kycnew.html')




def selfie(request,user):
    user_id=User.objects.get(id=user)
    print('user_id:',user_id)
    if request.method == 'POST':
        image_data = request.POST['imgurl']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name="Username" + '.' + ext)
     
        image_data = Kyc.objects.filter(user=user_id).update(live_photo=data)
        
        return redirect('/member/dashboard')
    return render(request, 'member/selfie.html')




 