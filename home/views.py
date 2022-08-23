from .models import Profile
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.shortcuts import render



 



        


def signup(request):
    profile_id= request.session.get("ref_profile")
    print('profile_id',profile_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(password)
    

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/signup')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/signup')
            
            user_obj = User(username = username , email = email, phone=phone)
            print(user_obj)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                print(recommended_by_profile)
                profile_obj.save()
                instance=User.objects.get(phone= phone)
                print(instance.id)
                registered_user = User.objects.get(id=instance.id)
                print('registered_user id',registered_user)
                registered_profile = Profile.objects.get(user=registered_user)
                print('....................')
                print(recommended_by_profile)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
                send_mail_after_registration(email , auth_token)
            else:
                profile_obj.save()
                send_mail_after_registration(email , auth_token)

            
            return redirect('/sent-mail')

        except Exception as e:
            print(e)


    return render(request,'home/signup.html')

def main_view(request,*args,**kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code = code)
        request.session['ref_profile']=profile.id
        
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    context={
            "is_index":True,

        }
    return render(request,'home/index.html',context)

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/member/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/member/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')


def faq(request):
    context={
            "is_faq":True,

        }
  
    return render(request,'home/faq.html',context)

def sent_mail(request):
    return render(request, 'home/token_sent.html')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def error_page(request):
    return  render(request , 'home/error.html')


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        print(user_obj)
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/member/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/member/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/member/login')
        request.session['userid']=user.id
        login(request , user)
        return redirect('/member/dashboard')
    return render(request , 'home/login.html')


def logout(request):
    del request.session['userid']
    return redirect('/member/login')

 



def about(request):

     context={
            "is_about":True,

        }
        
     return render(request,'home/about.html',context)

def contactus(request):
     context={
            "is_contactus":True,

        }
  
     return render(request,'home/contactus.html',context)
        
# def login(request):
#      return render(request, 'home/login.html')





