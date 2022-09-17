import json
from urllib import request

import stripe


# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
stripe.api_key = 'sk_test_51Li9phSJkEhbSHouPoTkOm5Oj3VWO4QuiMZd5LAP4xItN7rteTlCZlg5rZoB3NuBGgMBW55EEn3iZ5lJMYlKUJMn00vcYgEjqC'
print(stripe.PaymentIntent.create(
  amount=1099,
  currency='inr',
  payment_method_types=['card'],
))
