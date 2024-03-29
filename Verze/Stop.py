class Stop():
    '''
    Class respesenting Stops
    
    Object Attributes:
    ---------
    id :
        id of the stop
    name :
        name of the stop 
    stopLat :
        lattitude of the stop
    stopLon :
        longitude of the stop
    refToSTs :
        reference to stop times (empty list, will be modified later)
    '''
    
    # initialization variables
    def __init__(self, stop_id, stop_name, stop_lat, stop_lon):
        self.__id = stop_id
        self.__name = stop_name
        self.__stopLat = stop_lat
        self.__stopLon = stop_lon
        self.__refToSTs = []

    def __str__(self):
        return 'id: ' + str(self.__id) + ', name: ' + str(self.__name) + ', stopLat: ' + str(self.__stopLat) \
                + ', stopLon: ' + str(self.__stopLon) + ', refToSTs: ' + str(self.__refToSTs)
    
    # necessary getters and setters
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def refToSTs(self):
        return self.__refToSTs
    
    @property
    def stopLat(self):
        return self.__stopLat

    @property
    def stopLon(self):
        return self.__stopLon

    @refToSTs.setter
    def refToSTs(self, refToSTs):
        self.__refToSTs = refToSTs
