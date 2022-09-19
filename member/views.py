from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *
from .models import Kyc, Transaction
import base64
from django.core.files.base import ContentFile
from django.conf import settings
import stripe


@login_required(login_url="/member/login")
def index(request):
    user=User.objects.get(email=request.user)
    alert = Announcement.objects.filter().order_by('-id')
    profile=Profile.objects.get(user=user)
    my_recs=profile.get_recommended_profiles()
    recs_count= len(my_recs)
    kyc_check = Kyc.objects.filter(user=request.user).exists()
    kyc_status = Kyc.objects.filter(user=request.user).last()   
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

def transactions(request):
    context ={
        'is_transactions':True
    }
    return render(request, 'member/transactions.html',context)


# #  stripe payment

def create_checkout_session(request):
    test_id = uuid.uuid4()
    if request.method == 'POST':
        amount = int(request.POST['amount'])*100
        selected_currency = request.POST['currency']

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
           success_url = 'http://127.0.0.1:8000/member/dashboard/success/',
           cancel_url = 'http://127.0.0.1:8000/member/dashboard/cancel/',
        #    success_url = 'http://127.0.0.1:8000/member/dashboard/success/{test_id}',
        #    cancel_url = 'http://127.0.0.1:8000/member/dashboard/cancel/{test_id}',
        )
        print(session)
        # if session:
        #     transaction = Transaction(user = request.user, test_id = test_id, amount=amount/100)
        #     transaction.save()
    return redirect(session.url, code = 303)

# def paymentSuccess(request,test_id):
#     Transaction.objects.filter(test_id = test_id).update(payment_status = "success")
#     return redirect('/member/dashboard/')

# def paymentCancel(request,testid):
#     context = {
#         "payment_status" : "cancel"
#     }
#     return render(request,"member/index.html",context)
