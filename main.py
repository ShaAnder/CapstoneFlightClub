### --- IMPORTS --- ### 

#we want to import all our classes here
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

#we want date time for searching flights over the next 6 months
from datetime import datetime, timedelta

### --- OBJECTS --- ###

#let's initialize our objects
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

### --- MAIN --- ###

#we want to get our sheet data from the get destination data method
sheet_data = data_manager.get_destination_data()
#we have the origin city IATA to check flights from said city
ORIGIN_IATA = "DUB"
 
#if our sheet data for iata code is empty
if sheet_data[0]["iataCode"] == "":
    #in each row of the sheet (iata codes)
    for row in sheet_data:
        #take what get_destination_code provides and update it using the update method
        row["iataCode"] = flight_search.get_IATA_code(row["city"])
 
    #update destination_data with the sheet data
    data_manager.get_destination_data = sheet_data
    #update the codes on the sheet
    data_manager.update_IATA_codes()

#we want to get the date time for tomorrow - 180 days from now
tomorrow = datetime.now() + timedelta(days=1)
#this can then be used to search for flights over 6 months
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

#we now loop through the sheet data destinations
for destination in sheet_data:
    #and feed them into the check flights method, which is saved as the flight variable
    flight = flight_search.check_flights(
        #the method also takes, origin IATA, and from - to
        ORIGIN_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    #we want to add this here to catch any empty flights from the try / catch
    if flight is None:
        continue

    #D40: as this is now a flight club we're changing it to send emails
    if flight.price < destination["lowestPrice"]:
        #we want to get the variables for the users, their email and their fname
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        #we then create a message with the deal
        message = f"Low price alert! Only €{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            #if the stopovers is greater than 0 we notify them about the stop over
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        #finally we link them to a google link to book flight
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        #then send emails
        notification_manager.send_emails(emails, message, link)
    #else no cheaper flight found
    else:
        print("No cheaper price found")