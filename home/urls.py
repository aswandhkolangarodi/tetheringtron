from django.urls import path
from . import views

app_name= 'home'

urlpatterns = [
    path("",views.main_view,name='index'),


    path("about",views.about,name='about'),
    path("contactus",views.contactus,name='contactus'),
    path("member/login",views.login_attempt,name='login'),
    # path('member/login/otp', views.send_otp, name='send-otp'),
    path('logout' , views.logout, name='logout'),
    path("signup",views.signup,name='signup'),
    path('terms-conditions', views.terms_conditions, name="terms_conditions"),
    path("FAQ",views.faq,name='FAQ'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('sent-mail', views.sent_mail, name='sent_mail'),
    path('error' , views.error_page , name="error"),
    path('<str:ref_code>/',views.main_view,name='main-view'),
    path('member/change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('member/forgetpassword', views.forgetpassword, name='forgetpassword'),
    path('member/signup-otp/<token>', views.signup_otp, name="signup_otp"),
    path('member/otp/<uid>',views.otp, name='otp')
    # path('send_otp',views.send_otp)

]