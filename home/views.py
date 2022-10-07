from .models import Profile
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .helpers import send_forget_password_mail
from .mixins import MessageHandler
# from .forms import UserPhone

# html email required stuff

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# OTP
import pyotp


def signup(request):
    profile_id= request.session.get("ref_profile")
    if request.method == 'POST':
        first_name = request.POST.get('username')
        email = request.POST.get('email')
        country = str(request.POST.get('countryCode'))
        phone = str(request.POST.get('phone'))
        phone_number_with_country_code = country + phone
        password = request.POST.get('password')
        check=request.POST.get('ckeck')

        if check is None:
            messages.success(request,'You must check Terms and conditions')
            return redirect('/signup')

        try:
            user =User.objects.filter(email = email).first()
            if user:
                verification_check = Profile.objects.filter(user = user,is_verified = True).last()
                if verification_check:
                    print(verification_check)
                    messages.success(request, 'Username is taken.')
                    return redirect('/signup')
                else:
                    User.objects.filter(email = email).delete()

            if User.objects.filter(phone = phone_number_with_country_code).first():
                messages.success(request, 'Number is taken.')
                return redirect('/signup')
            
            user_obj = User(first_name = first_name , email = email,phone=phone_number_with_country_code)
            print(user_obj)
            user_obj.set_password(password)
            user_obj.save()
            user_secret_key = pyotp.random_base32()
            print('user_secret_key',user_secret_key)
            profile_obj = Profile.objects.create(user = user_obj , auth_token = user_secret_key)

            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                print(recommended_by_profile)
                profile_obj.save()
                instance=User.objects.get(email= email)
                print(instance.id)
                registered_user = User.objects.get(id=instance.id)
                print('registered_user id',registered_user)
                registered_profile = Profile.objects.get(user=registered_user)
                print(recommended_by_profile)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
                messages.success(request, "We have send an OTP to your phone")
                return redirect(f'/member/signup-otp/{profile_obj.auth_token}')
            else:
                messages.success(request, "We have send an OTP to your phone")
                return redirect(f'/member/signup-otp/{profile_obj.auth_token}')

        except Exception as e:
            print(e)


    return render(request,'home/signup.html')

def signup_otp(request, token):
    member_profile=Profile.objects.get(auth_token = token)
    otp = pyotp.TOTP(token, interval=300)
    print('asdfghjk',otp)
    recent_otp = otp.now()
    if request.method == 'POST':
        enter_otp=request.POST['otp']
        verification = otp.verify(enter_otp)
        if verification == True:
            send_mail_after_registration(member_profile , token)
            return redirect('/sent-mail')
        elif verification == False:
            messages.success(request,'OTP Expired')
            return redirect(f'/member/signup-otp/{member_profile.auth_token}')
        else:
            messages.success(request,'Wrong OTP')
            return redirect(f'/member/signup-otp/{member_profile.auth_token}')
    else:
        message_handler=MessageHandler(member_profile.user.phone, recent_otp).send_otp()
    return render(request, 'home/otp.html',{'token':token})

# Referral
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

# email verification
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

def sent_mail(request):
    return render(request, 'home/token_sent.html')

def send_mail_after_registration(email , token):
    html_content = render_to_string("home/email_template.html",{'title':'send mail','content':token})
    text_content = strip_tags(html_content)
    subject = 'Your accounts need to be verified'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_obj = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()
    
def error_page(request):
    return  render(request , 'home/error.html')


# login
def login_attempt(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(email = email).first()
        print(user_obj)
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/member/login')
        
        if user_obj.is_superuser:
            user = authenticate(email = email , password = password)
            login(request , user)
            return redirect('/trxadmin/dashboard')
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/member/login')

        user = authenticate(email = email , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/member/login')
        if user.member_status == False:
            messages.success(request,'you are temporary blocked')
            return redirect('/member/login')
        else:
            login_user=User.objects.get(email=email)
            member_profile=Profile.objects.get(user=user)
            messages.success(request,"OTP is send to registered Phone number")
            return redirect(f'/member/otp/{member_profile.auth_token}')
            # login(request , user)
            # return redirect('/member/dashboard')
    return render(request , 'home/login.html')


# login otp
def otp(request, token):
    print('hi')
    member_profile=Profile.objects.get(auth_token = token)
    otp = pyotp.TOTP(token, interval=300)
    recent_otp = otp.now()
    if request.method == 'POST':
        enter_otp=request.POST['otp']
        verification = otp.verify(enter_otp)
        if verification == True:
            login(request , member_profile.user)
            return redirect('/member/dashboard')
        elif verification == False:
            messages.success(request,'OTP Expired')
            return redirect(f'/member/otp/{token}')
        else:
            messages.success(request,'Wrong OTP')
            return redirect(f'/member/otp/{token}')
    else:
        message_handler=MessageHandler(member_profile.user.phone, recent_otp).send_otp()
    return render(request,'home/otp.html',{'token':token})


# re send otp 

def resend_otp(request , token):
    user = Profile.objects.filter(auth_token = token).last()
    user_secret_key = pyotp.random_base32()
    print("user_secret_key",user_secret_key)
    user.auth_token = user_secret_key
    user.save()
    return redirect(f'/member/otp/{user_secret_key}')


# forget password
def forgetpassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            
            if not User.objects.filter(email=email).first():
                messages.success(request, 'Not user found with this email.')
                return redirect('/forgetpassword')
            
            user_obj = User.objects.get(email = email)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/member/forgetpassword')
    except Exception as e:
        print(e)
    return render(request , 'home/forget-password.html')

def ChangePassword(request , token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user_id = request.POST.get('user_id')
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/member/change-password/{token}/')
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password Reset Successfully.')
            return redirect('/member/login')
    except Exception as e:
        print(e)
    return render(request , 'home/change-password.html' , context)


def terms_conditions(request):
    return render(request, 'home/terms_conditions.html')

def error_page(request):
    return  render(request , 'error.html')


def faq(request):
    return render(request,'home/faq.html')


def about(request):
     return render(request,'home/about.html')


def contactus(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact(name=name,email=email,message=message)
        contact.save()
    context={
            "is_contactus":True,

        }
    return render(request,'home/contactus.html',context)

# logout
@login_required(login_url="/member/login")
def logout(request):
    django_logout(request)
    return redirect('/member/login')


def handler404(request, exception):
    return render(request, "member/404.html", status=404)