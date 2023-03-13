# Prvá časť, načítanie dát, vytvorenie tried, vytvorenie objektov


import csv

class Stop():
    
    def __init__(self,stop_id,stopName):
        self.__id = stop_id
        self.__name = stopName

    def __str__(self):
        return 'id: ' + str(self.__id) + ', name: ' + str(self.__name)
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @id.setter
    def id(self, id):
        self.__id = id

class StopTime():

    def __init__(self,stop_id,trip_id):
        self.__refToStop = stop_id
        self.__refToTrip = trip_id

    def __str__(self):
        return 'refToStop: ' + self.__refToStop + ', refToTrip: ' + self.__refToTrip
    
    @property
    def refToStop(self):
        return self.__refToStop
    
    @property
    def refToTrip(self):
        return self.__refToTrip
    
    @refToStop.setter
    def refToStop(self, refToStop):
        self.__refToStop = refToStop

    @refToTrip.setter
    def refToTrip(self, refToTrip):
        self.__refToTrip = refToTrip

class Trip():
    
    def __init__(self,trip_id,route_id):
        self.__refToSTs = trip_id
        self.__refToRoute = route_id

    def __str__(self):
        return 'refToRoute: ' + self.__refToRoute + ', refToSTs: ' + self.__refToSTs

    @property
    def refToSTs(self):
        return self.__refToSTs
    
    @property
    def refToRoute(self):
        return self.__refToRoute
    
    @refToSTs.setter
    def refToSTs(self, refToSTs):
        self.__refToSTs = refToSTs

    @refToRoute.setter
    def refToRoute(self, refToRoute):
        self.__refToRoute = refToRoute

class Route():

    def __init__(self,route_id,routeShortName):
        self.__refToTrips = route_id
        self.__name = routeShortName

    def __str__(self):
        return 'refToTrips: ' + self.__refToTrips + ', name: ' + self.__name
    
    @property
    def refToTrips(self):
        return self.__refToTrips
    
    @property
    def name(self):
        return self.__name
    
    @refToTrips.setter
    def refToTrips(self, refToTrips):
        self.__refToTrips = refToTrips

def createObjects():#(stopsFile,stopTimesFile,tripsFile,routesFile): # docstringy a open upraviť
    #with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
    #    open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
    #    open(tripsFile, encoding = "utf-8", newline = "") as tr, \
    #    open(routesFile, encoding = "utf-8", newline = "") as rt:

    # ak sú súbory v inej zložke, do uvodzoviek dajte adresu
    with open(r"C:\Users\andre\Desktop\Prog_python\stops.txt", encoding = "utf-8", newline = "") as sp, \
        open(r"C:\Users\andre\Desktop\Prog_python\stop_times.txt", encoding = "utf-8", newline = "") as st, \
        open(r"C:\Users\andre\Desktop\Prog_python\trips.txt", encoding = "utf-8", newline = "") as tr, \
        open(r"C:\Users\andre\Desktop\Prog_python\routes.txt", encoding = "utf-8", newline = "") as rt:
        
        reader_sp = csv.reader(sp, delimiter=",")
        reader_st = csv.reader(st, delimiter=",")
        reader_tr = csv.reader(tr, delimiter=",")
        reader_rt = csv.reader(rt, delimiter=",")

        # list comprehension - vytvorí listy objektov
        stops = []
        stops = [Stop(spLine[0],spLine[1]) for idx, spLine in enumerate(reader_sp) if idx != 0]
        
        stopTimes = []
        stopTimes = [StopTime(stLine[3],stLine[0]) for idx, stLine in enumerate(reader_st) if idx != 0]
        
        trips = []
        trips = [Trip(trLine[2],trLine[0]) for idx, trLine in enumerate(reader_tr) if idx != 0]
        
        routes = []
        routes = [Route(rtLine[0],rtLine[2]) for idx, rtLine in enumerate(reader_rt) if idx != 0]
        
        return stops, stopTimes, trips, routes

# funkcia vráti 4 listy
stops, stopTimes, trips, routes = createObjects() # funkcia potrebuje ako argumenty názvy súborov, alebo ich napíšte priamo do "with" časti

print(trips[7].refToRoute)
trips[7].refToRoute = 'asd'
print(trips[7].refToRoute)
