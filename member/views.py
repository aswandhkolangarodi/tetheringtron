from email import message
from multiprocessing import context
from django import views
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *

from .models import Kyc
# from .forms import Kyc


from .forms import KycForm

# Create your views here.

@login_required(login_url="/member/login")
def index(request):
    user_id=request.session['userid']
    user=User.objects.get(id=user_id)
    alert = Announcement.objects.filter().order_by('-id')
    # kyc_obj=Kyc.objects.get(user=user)
    # if kyc_obj is None:
    #     message.success('Complete KYC to live on Tethering Tron')
    #     return redirect('/member/kyc')
    profile=Profile.objects.get(user=request.user)
    my_recs=profile.get_recommended_profiles()
    recs_count= len(my_recs)

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
    user_id=request.session['userid']
    user=User.objects.get(id=user_id)
    reward=Profile.objects.get(user=request.user)
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
    user_id=request.session['userid']
    #  if request.POST.get('action') == 'kyc_main':
    if request.method == 'POST' and request.FILES:
        country=request.POST['country']
        city =request.POST['city']
        idproof_name=request.POST['idproof_name']
        address=request.POST['address']
        pin=request.POST['pin']
        idproof_document=request.FILES['idproof_document']
        selfi=request.FILES['selfi']
        user=User.objects.get(id=user_id)
        kyc_obj=Kyc(user=user, country=country, address=address, city=city, pin=pin, id_proof=idproof_name, id_proof_file=idproof_document, live_photo=selfi)
        kyc_obj.save()
        return redirect('/member/dashboard')
    return render(request, 'member/kycnew.html')

def kyc(request):

    form = KycForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()   
    context= {
        "form":form,
    }
    return render(request, 'member/kycnew.html')

