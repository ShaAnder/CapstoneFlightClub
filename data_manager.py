### --- IMPORTS --- ###

#we want pprint to read the data better
from pprint import pprint
#import requests to read the destination data
import requests
#we want to import os and loadenv to load our env variables
import os
from dotenv import load_dotenv

### --- ENV VARS --- ###

#let's load our envs
load_dotenv()

#sheety endpoint for interacting with google sheet
sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
sheety_bearer_token = os.getenv("SHEETY_TOKEN")

sheety_user_endpoint = os.getenv("SHEETY_USERS")

print(sheety_bearer_token)
print(sheety_endpoint)

### --- HEADER --- ###

sheety_header = {
    "Authorization": f"Bearer {sheety_bearer_token}"
}

### --- CLASS --- ###

class DataManager:
    """Class Focused on interacting with the sheet
    """
    def __init__(self) -> None:
        #we want to get the destination data here for passing back to main
        self.destination_data = {}


    def get_destination_data(self):
        """Gets the destination data from the sheet
        """
        #first we want to make our request. We want the prices to feed to main.py and to 
        #compare for deals later on
        response = requests.get(sheety_endpoint)
        #raise for status to flag any errors
        response.raise_for_status()
        #get the response json as data
        data = response.json()
        #we get all the data under the prices list(of dictionaries) for use
        self.destination_data = data["prices"]
        #now we return that for use later
        print(self.destination_data)
        return self.destination_data

    def update_IATA_codes(self):
        """Takes the response from destination data and uses it to get the IATA code from the kiwi api
        """
        #now we loop through each city in the destination data
        for city in self.get_destination_data:
            #we then edit the data
            new_data = {
                #we want to input the iatacode we get into that sheet row
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            #then we put the new data into the sheet
            response = requests.put(
                url=f"{sheety_endpoint}/{city['id']}",
                json=new_data
            )
            print(response.text)

    #Day40 turning it from flight deal finder into a flight club
    def get_customer_emails(self):
        """Gets the customer emails for sending out flight deals

        Returns:
            _type_: _description_
        """
        customers_endpoint = sheety_user_endpoint
        response = requests.get(customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data