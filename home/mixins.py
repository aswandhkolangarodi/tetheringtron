from twilio.rest import Client
import pyotp
from django.conf import settings
import time


class MessageHandler:
    phone_number=None
    otp=None

    def __init__(self,phone_number, otp) -> None:
        self.phone_number=phone_number
        self.otp=otp

    def send_otp(self):
        
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) 

        message = client.messages.create(  
                               
                                body=f'Your otp for verification is {self.otp}',   
                                from_='+9718000320738',  
                                to=self.phone_number
                            ) 

        print(message.sid)



# if __name__ == '_main_':
#     send_otp()

# def generateOTP() :
#     totp = pyotp.TOTP('base32secret3232')
#     otp=totp.now() 
#     return otp


