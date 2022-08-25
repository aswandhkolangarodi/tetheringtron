from multiprocessing import context
from django import views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *
from .models import Kyc
# from .forms import Kyc

# Create your views here.

@login_required(login_url="/member/login")
def index(request):
    user_id=request.session['userid']
    user=User.objects.get(id=user_id)

    alert = Announcement.objects.all()

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
    context ={
        'is_rewards':True
    }
    return render(request, 'member/rewards.html',context)

# def kyc_home(request):
#     return render(request, 'member/kyc-home.html')

def coin_details(request):
    context ={
        'is_coin_details':True
    }
    return render(request, 'member/coin-details.html',context)

def kyc_main(request):
    #  if request.POST.get('action') == 'kyc_main':
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        print(address)
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        id_proof = request.POST.get('id_proof')
       
        id_proof_file = request.FILES.get('id_proof_file')
        

        new = Kyc(
            full_name=full_name,
            country=country,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            pin=pin,
            id_proof=id_proof,
            id_proof_file=id_proof_file,
        )
        new.save()
    
  
    return render(request, 'member/kyc_main.html')

def kyc(request):
    return render(request, 'member/kycnew.html')



