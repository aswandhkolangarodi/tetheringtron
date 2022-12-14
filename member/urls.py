from django.urls import path
from . import views
app_name= 'member'

urlpatterns = [
   
   path("dashboard/", views.index, name='index'),
   path('profile/', views.profile, name='profile'),
   path('transactions/', views.transactions, name='transactions'),
   path('rewards/', views.rewards, name='rewards'),
   path('kyc/', views.kyc_home, name='kyc'),
   path('coin-details/', views.coin_details, name='coin-details'),
   path('kyc_main/', views.kyc_main, name='kyc_main'),
   path('selfie/', views.selfie, name='selfie'),
   path('selfie/', views.selfie, name='selfie'),
   path('announcement_is_seen/<str:id>', views.announcement_is_seen, name='announcement_is_seen'),
   path('bankdetails', views.bankdetails, name='bankdetails'),




# Stripe
   path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session2"),
   path('success/<str:test_id>', views.paymentSuccess, name="success"),
   path('cancel/<str:test_id>', views.paymentCancel, name="cancel"),
   # withdraw
   path('withdraw', views.withdraw, name="withdraw")
]

