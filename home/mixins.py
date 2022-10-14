from twilio.rest import Client
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
                                messaging_service_sid='MG50cd2dc652121ee9fa33b4dad45a7d13', 
                                body=f'Your otp for verification is {self.otp}',   
                                  
                                to=self.phone_number
                            ) 

        print(message.sid)





