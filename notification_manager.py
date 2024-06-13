### --- IMPORTS --- ###

#we want pprint to read the data better
from pprint import pprint
#we want to import twilio to send messages
from twilio.rest import Client
#we want to import os and loadenv to load our env variables
import os
from dotenv import load_dotenv
#we import smtplib for email sending
import smtplib

### --- ENV VARS --- ###

#let's load our envs
load_dotenv()

twilio_sid_number = os.getenv("TWILIO_SID")
twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
sending_number = os.getenv("NUMBER_SENDING")
receiving_number = os.getenv("NUMBER_RECEIVING")


sending_email = os.getenv("SEND_EMAIL")
sending_pass = os.getenv("SEND_PASS")

### --- CLASS --- ###

class NotificationManager:

    def __init__(self):
        #we're initializing the twilio client as an attribute here
        self.client = Client(twilio_sid_number, twilio_auth)

    def send_sms(self, message):
        """Method to send twilio message

        Args:
            message (_type_): The message is created in main.py and passed to this as an arg.
        """
        #creates and sends the message
        message = self.client.messages.create(
            body=message,
            from_=sending_number,
            to=receiving_number,
        )
        # Prints if successfully sent.
        print(message.sid)
    
    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(sending_email, sending_pass)
            for email in emails:
                connection.sendmail(
                    from_addr=sending_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )