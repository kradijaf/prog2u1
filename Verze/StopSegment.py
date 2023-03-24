class StopSegment:
    '''
    Class respesenting section between 2 adjacent stops
    ...
    
    Atributes:
    ---------
    start:
        name of the staring stop
    finish :
        name of the ending stop 
    counter :
        number of related trips
    trips :
        array of objects of related trips

    Methods
    ------
    __add_trip(trip):
        adding object od related trip to the array self.__trips
    '''
    def __init__(self, start, finish) -> None:
        self.__start = start
        self.__finish = finish
        self.__counter = 1
        self.__trips = []
    
    @property
    def start(self):
        return self.__start

    @property
    def finish(self):
        return self.__finish
    
    @property
    def counter(self):
        return self.__counter
    
    @counter.setter
    def counter(self, value) -> None:
        self.__counter = value

    @property
    def trips(self):
        return self.__trips
    
    def __str__(self) -> str:
        return str(self.counter)
    
    def __add_trip(self, trip) -> None:
        '''
        adding related trip to array of trips
        
        Parameters:
        ----------
        trip :
            object of class Trip, trip which service this segment
        
        Return value:
        -------------
        None
        '''
        self.__trips.append(trip)
        self.counter = self.counter + 1