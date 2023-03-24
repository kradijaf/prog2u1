class Route():

    # initialization variables
    def __init__(self, route_id, route_short_name, route_long_name):
        self.__route_id = route_id
        self.__refToTrips = []
        self.__name = route_short_name
        self.__routeLongName = route_long_name

    def __str__(self):
        return 'route_id: ' + self.__route_id + ', refToTrips: ' + self.__refToTrips + ', name: ' + self.__name + ', routeLongName: ' + str(self.__routeLongName)
    
    # necessary getters and setters
    @property
    def route_id(self):
        return self.__route_id

    @property
    def refToTrips(self):
        return self.__refToTrips
    
    @property
    def name(self):
        return self.__name
    
    @property
    def routeLongName(self):
        return self.__routeLongName
    
    @refToTrips.setter
    def refToTrips(self, refToTrips):
        self.__refToTrips = refToTrips
