from django.urls import path
from . import views

app_name= 'member'

urlpatterns = [
   
   path("", views.index, name='index'),
   path('profile/', views.profile, name='profile'),
   path('transactions/', views.transactions, name='transactions'),
   path('rewards/', views.rewards, name='rewards'),
   # path('kyc/', views.kyc_home, name='kyc'),
   path('coin-details/', views.coin_details, name='coin-details'),
   path('kyc_main/', views.kyc_main, name='kyc_main')

]
