from multiprocessing import context
from django import views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import *
from trxadmin.models import *
from .forms import KycForm
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

def kyc(request):
    form = KycForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()   
    context= {
        "form":form,
    }
    return render(request, 'member/kycnew.html')