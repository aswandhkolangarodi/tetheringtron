from twilio.rest import Client
import pyotp
from django.conf import settings
import time

ACCOUNT_SID = "ACb9b60800ed9b7c42b7a6effdac22b7d0"
AUTH_TOKEN = "af28c30e9b97df06323be940ba19a740"
class MessageHandler:
    phone_number=None
    otp=None

    def __init__(self,phone_number, otp) -> None:
        self.phone_number=phone_number
        self.otp=otp

    def send_otp(self):
        
        
        client = Client(ACCOUNT_SID, AUTH_TOKEN) 

        message = client.messages.create(  
                               
                                body=f'Your otp for verification is {self.otp}',   
                                from_='+12184007822',  
                                to=self.phone_number
                            ) 

        print(message.sid)



# if __name__ == '_main_':
#     send_otp()

# def generateOTP() :
#     totp = pyotp.TOTP('base32secret3232')
#     otp=totp.now() 
#     return otp

