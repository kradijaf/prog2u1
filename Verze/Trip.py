class Trip():
    
    def __init__(self, trip_id, route_id, trip_headsign):
        self.__trip_id = trip_id
        self.__refToSTs = []
        self.__refToRoute = route_id
        self.__tripHeadsign = trip_headsign
        #self.__calendar = calendar

    def __str__(self):
        return 'trip_id: ' + self.__trip_id + ', refToRoute: ' + self.__refToRoute + ', refToSTs: ' + self.__refToSTs + ', tripHeadSign: ' + str(self.__tripHeadsign)

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