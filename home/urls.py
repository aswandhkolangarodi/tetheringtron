from django.urls import path
from . import views

app_name= 'home'

urlpatterns = [
    path("",views.main_view,name='index'),


    path("about",views.about,name='about'),
    path("contactus",views.contactus,name='contactus'),
    path("member/login",views.login_attempt,name='login'),
    path('member/login/otp', views.send_otp, name='send-otp'),
    path('logout' , views.logout, name='logout'),
    path("signup",views.signup,name='signup'),
    path("FAQ",views.faq,name='FAQ'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('sent-mail', views.sent_mail, name='sent_mail'),
    path('error' , views.error_page , name="error"),
    path('<str:ref_code>/',views.main_view,name='main-view')

]