class Trip():
    '''
    Class respesenting Trips
    
    Object Attributes:
    ---------
    trip_id :
        trip id of the trip
    refToRoute :
        route id of the trip
    tripHeadsign :
        headsign of the trip 
    refToSTs :
        reference to stop times (empty list, will be modified later)
    '''
    
    # initialization variables
    def __init__(self, trip_id, route_id, trip_headsign):
        self.__trip_id = trip_id
        self.__refToSTs = []
        self.__refToRoute = route_id
        self.__tripHeadsign = trip_headsign

    def __str__(self):
        return 'trip_id: ' + self.__trip_id + ', refToRoute: ' + self.__refToRoute + ', refToSTs: ' + self.__refToSTs + ', tripHeadSign: ' + str(self.__tripHeadsign)

    # necessary getters and setters
    @property
    def trip_id(self):
        return self.__trip_id

    @property
    def refToSTs(self):
        return self.__refToSTs
    
    @property
    def refToRoute(self):
        return self.__refToRoute
    
    @property
    def tripHeadsign(self):
        return self.__tripHeadsign
    
    @refToSTs.setter
    def refToSTs(self, refToSTs):
        self.__refToSTs = refToSTs

    @refToRoute.setter
    def refToRoute(self, refToRoute):
        self.__refToRoute = refToRoute
