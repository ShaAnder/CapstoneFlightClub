class FlightData:

    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date, stop_overs=0, via_city=""):
        """
        Method for holding all the information for flights, the sole purpose of this is to get our flight data and store it for 
        any and all usages later on (checking prices, multiple stop overs ect. And sending the info via text / email)   
        """
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

        #we want to add these parameters D.40 (find flights with stopovers)

        self.stop_overs = stop_overs
        self.via_city = via_city