from math import floor
from prettytable import PrettyTable

class StopSegment:

    def __init__(self, start, finnish) -> None:
        self.__start = start
        self.__finnish = finnish
        self.__counter = 0
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
    
    def add_trip(self, trip) -> None:
        self.__trips.append(trip)
        self.counter = self.counter + 1

# Chtělo by to nějakou třídu pro listy a metody create_segments()) a busiest()
# stopsSegmets - pole objektů třídy StopSegment
stopSegments = []       # pole s objekty stopSegment

def __ss_exist(self, start, finnish) -> StopSegment|bool:
    for ss in stopSegments:
        if  ss.start == start and ss.finnish == finnish:      
            return ss
    return False

def __merge_sort(self, array : list) -> list:
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

    self.__merge_sort(self.stopSegments)
    
def busiest(self, date : date) -> None:
    self.__sort_Segments()
    table = PrettyTable(['Start', 'Finnish', 'Number of trips', 'Routes'])
    for item in stopSegments[:5]:
        table.add_row([item.start, item.to, item.count, ''])
        routes=[]
        for trip in item.trips.values():
            routes.append(trip.reftoRoute.name)
        set_routes = set(routes)
        routes = list(set_routes)
        routes = sorted(routes)
        for route in routes:
            table.add_row(['', '', '', route])
    print(table)
    
def create_StopSegments(self) -> None:
    for item in trips.values():              # pole objektů třídy Trip
        for idx in range(len(item.reftoSTs) - 1):
            result = __ss_exist(item.reftoSTs[idx].reftoStop.name, item.reftoSTs[idx + 1].reftoStop.name)
            if not result:
                segment = StopSegment(item.reftoSTs[idx].reftoStop.name, item.reftoSTs[idx + 1].reftoStop.name)
                segment.trips.append(item)
                stopSegments.append(segment)
            else:
                result.trips.append(item)

# Sekvence volání metod: 
#self.Create_stopSegments()
#self.busiest()