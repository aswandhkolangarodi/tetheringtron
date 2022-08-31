from twilio.rest import Client
import pyotp
from django.conf import settings
import time

ACCOUNT_SID = "ACb9b60800ed9b7c42b7a6effdac22b7d0"
AUTH_TOKEN = "142ea5eb34008a9f42fa8f7c32b25fa1"
class MessageHandler:
    phone_number=None
    otp=None

    def __init__(self,phone_number, otp) -> None:
        self.phone_number=phone_number
        self.otp=otp

    def send_otp(self):
        print('.........',self.phone_number)
        print(',,,,,,,,,',self.otp)
        account_sid = 'ACb9b60800ed9b7c42b7a6effdac22b7d0' 
        auth_token = AUTH_TOKEN
        client = Client(account_sid, auth_token) 

        message = client.messages.create(  
                                messaging_service_sid='MG50cd2dc652121ee9fa33b4dad45a7d13',  
                                body=f'Your otp for verification is {self.otp}',     
                                to=self.phone_number
                            ) 

        print(message.sid)



# if __name__ == '_main_':
#     send_otp()

# def generateOTP() :
#     totp = pyotp.TOTP('base32secret3232')
#     otp=totp.now() 
#     return otp


