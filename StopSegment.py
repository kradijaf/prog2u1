from math import floor
from prettytable import PrettyTable

class StopSegment:
    '''
    Class respesenting section between 2 adjacent stops
    ...
    
    Atributes:
    ---------
    start:
        name of the staring stop
    finnish :
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
    def __init__(self, start, finnish) -> None:
        self.__start = start
        self.__finnish = finnish
        self.__counter = 1
        self.__trips = []
    
    @property
    def start(self):
        return self.__start

    @property
    def finnish(self):
        return self.__finnish
    
    @property
    def counter(self):
        return self.__counter
    
    @counter.setter
    def counter(self, value) -> None:
        self.__counter = value

    @property
    def trips(self):
        return self.__trips
    
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

# Chtělo by to nějakou třídu pro listy a metody create_segments()) a busiest()
# stopsSegmets - pole objektů třídy StopSegment
stopSegments = {}       
'''
Dictionary  key:    stopSegment_id (joined stop_id of start and stop_id of finnish)
            value:  object of StopSegment
'''

def __merge_sort(self, array : list) -> list:
    '''
        sorting array of objects of stopSegments using merge sort
        
        Parameters:
        ----------
        array :
            array of object (class StopSegment) to sort
        
        Return value:
        -------------
        None
    '''
    if len(array) > 1:
        sorted_1 = self.__merge_sort(array[:floor(len(array)/2)])
        sorted_2 = self.__merge_sort(array[floor(len(array)/2):])
        idx_1 = 0
        idx_2 = 0
        sorted_array = []
        while idx_1 < len(sorted_1) and idx_2 < len(sorted_2):
            if sorted_1[idx_1].counter < sorted_2[idx_2].counter:
                sorted_array.append(sorted_2[idx_2])
                idx_2 += 1
            else:
                sorted_array.append(sorted_1[idx_1])
                idx_1 += 1
        while idx_1 < len(sorted_1):
            sorted_array.append(sorted_1[idx_1])
            idx_1 += 1
        while idx_2 < len(sorted_2):
            sorted_array.append(sorted_2[idx_2])
            idx_2 += 1
        return sorted_array
    return array 

def __sort_Segments(self) -> None:
    '''
        method for calling method merge soft
        
        Parameters:
        -----------
        None

        Return value:
        -------------
        None
        '''
    self.__merge_sort(self.stopSegments)
    
def busiest(self) -> None:
    '''
        calculating and printing five busiest stopSegments
        
        Parameters:
        ----------
        None

        Return value:
        -------------
        None
    '''
    self.__sort_Segments()
    table = PrettyTable(['Start', 'Finnish', 'Number of trips', 'Routes'])
    for item in stopSegments[:5]:
        table.add_row([item.start, item.to, item.count, ''])
        routes=[]
        for trip in item.trips:
            routes.append(trip.reftoRoute.name)
        set_routes = set(routes)
        routes = list(set_routes)
        routes = sorted(routes)
        for route in routes:
            table.add_row(['', '', '', route])
    print(table)
    
def create_StopSegments(self) -> None:
    '''
        method for creating objects of class StopSegment
        
        Parameters:
        ----------
        None
        
        Return value:
        -------------
        None
    '''
    current_trip_id = None
    start = None
    finish = None
    start_id = None
    finish_id = None
    for (key, stopTime) in stopTimesT:
        if current_trip_id != key:
            current_trip_id = key
            start = stopTime.refToStop.name
            start_id = stopTime.refToStop.id
        else:
            finish = stopTime.refToStop.name
            finish_id = stopTime.refToStop.id
            Segment = stopSegments.get(start_id + finish_id)
            if not Segment:
                stopSegments[start_id + finish_id] = StopSegment(start, finish)
                stopSegments[start_id + finish_id].trips.append(stopTime.refToTrip)
            else:
                Segment.counter += 1
                Segment.trips.append(stopTime.refToTrip)
            start = stopTime.refToStop.name
            start_id = stopTime.refToStop.id
        current_trip_id = key

# Sekvence volání metod: 
#self.Create_stopSegments()
#self.busiest()