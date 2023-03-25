class StopTime():
    '''
    Class respesenting Stop Times
    
    Object Attributes:
    ---------
    refToTrip :
        trip id of the stop time
    arrivalTime :
        arrival time of the stop time
    departureTime :
        departure time of the stop time
    refToStop :
        stop id of the stop time
    '''

    # initialization variables
    def __init__(self, trip_id, arrival_time, departure_time, stop_id):
        self.__refToStop = stop_id
        self.__refToTrip = trip_id
        self.__arrivalTime = arrival_time
        self.__departureTime = departure_time

    def __str__(self):
        return 'refToStop: ' + self.__refToStop + ', refToTrip: ' + self.__refToTrip + ', arrivalTime: ' \
                + str(self.__arrivalTime) + ', departureTime: ' + str(self.__departureTime)
    
    # necessary getters and setters
    @property
    def refToStop(self):
        return self.__refToStop
    
    @property
    def refToTrip(self):
        return self.__refToTrip
    
    @property
    def arrivalTime(self):
        return self.__arrivalTime
    
    @property
    def departureTime(self):
        return self.__departureTime

    @refToStop.setter
    def refToStop(self, refToStop):
        self.__refToStop = refToStop

    @refToTrip.setter
    def refToTrip(self, refToTrip):
        self.__refToTrip = refToTrip
