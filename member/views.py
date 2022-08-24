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
    context ={
        'user':user,
        'alert':alert,
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
     if request.POST.get('action') == 'kyc_main':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Kyc.objects.create(
            title=title,
            description=description,
            image=image
        )
    
  
     return render(request, 'member/kyc_main.html')