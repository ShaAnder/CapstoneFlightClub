### --- IMPORTS --- ###

#we want pprint to read the data better
from pprint import pprint
#import requests to read the destination data
import requests
#we want to import os and loadenv to load our env variables
import os
from dotenv import load_dotenv

#we want to import FlightData, this stores our variables to be called when we need them
from flight_data import FlightData


### --- ENV VARS --- ###

#let's load our envs
load_dotenv()

#we want these to interact with tequila
tequila_url = os.getenv("TEQUILA_ENDPOINT")
tequila_api_key = os.getenv("TEQUILA_FLIGHT_API")

#usually id put the endpoint / params at the top for easy editing but it requires us to feed in arguments from main.py
#as a result the endpoints and queries are inside the class / methods for this project


### --- CLASS --- ###

class FlightSearch:
    """Class designed to search for flights and IATA codes
    """
    def get_IATA_code(self, city_name):
        """Gets the IATA destination code
        Args:
            city_name (str): Arg fed in from main.py the city name is the name of the city from the sheet 
        Returns:
            str: IATA code for sheet and finding flights later, for testing purposes code will be set to TESTING
        """

        #we want to get the params and headers, we do this inside class to pass in the city_name arg
        tequila_endpoint = f"{tequila_url}/locations/query"
        tequila_header = {"apikey": tequila_api_key}
        tequila_params = {"term": city_name, "location_types": "city"}

        #now we make our request
        response = requests.get(url=tequila_endpoint, headers=tequila_header, params=tequila_params)
        response.raise_for_status()
        #we dive into the locations section
        data = response.json()["locations"]
        #then we get the code
        code = data[0]["code"]
        #now we return it
        return code     

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """Method to check for flights with data provided

        Args:
            origin_city_code (_type_): Origin City IATA code, this is fed in from main.py
            destination_city_code (_type_): Destination IATA, this comes from the sheety variable in main.py
            from_time (_type_): This comes from main.py the datatime for tomorrow
            to_time (_type_): ^ same as above but for 6 months from now

        Returns:
            _type_: _description_
        """
        
        #we get our headers and query, this time were providing all the details for a flight to a place
        search_header = {"apikey": tequila_api_key}
        search_params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR"
        }

        #now we get our response
        response = requests.get(
            url=f"{tequila_url}/v2/search",
            headers=search_header,
            params=search_params,
        )

        #we now want to add a try / except to ensure that if no city / route is found it won't crash out
        try:
            data = response.json()["data"][0]
            print(data)
        except IndexError:
            #very likely there won't be certain flights due to distance, so we want to change the request
            #to include more stop overs in this event. If it flags the error it will then proceed to search the route with 2 max stop overs
            #then if it can't find it will return none.
            search_params["max_stopovers"] = 2
            response = requests.get(
                url=f"{tequila_url}/v2/search",
                headers=search_header,
                params=search_params,
            )

            #on the off chance that even with stop overs there is no flight we must add another try / except to ensure no flight is caught
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data

        #we add this here to keep the code going instead of bricking it when it returns none
        else:
            #finally we create the flight data object for returning, and take all the information we acquired from hte 
            #search and feed it into flight data for storage
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            #print the city and the price
            print(f"{flight_data.destination_city}: €{flight_data.price}")
            #now return it
            return flight_data
