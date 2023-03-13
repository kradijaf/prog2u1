# Prvá časť, načítanie dát, vytvorenie tried, vytvorenie objektov


import csv


class Stop():
    
    def __init__(self,stop_id,stopName):
        self.id = stop_id
        self.name = stopName

    def __str__(self):
        return 'id: ' + str(self.id) + ', name: ' + str(self.name)

class StopTime():

    def __init__(self,stop_id,trip_id):
        self.refToStop = stop_id
        self.refToTrip = trip_id

    def __str__(self):
        return 'refToStop: ' + self.refToStop + ', refToTrip: ' + self.refToTrip

class Trip():
    
    def __init__(self,trip_id,route_id):
        self.refToSTs = trip_id
        self.refToRoute = route_id

    def __str__(self):
        return 'refToRoute: ' + self.refToRoute + ', refToSTs: ' + self.refToSTs

class Route():

    def __init__(self,route_id,routeShortName):
        self.refToTrips = route_id
        self.name = routeShortName

    def __str__(self):
        return 'refToTrips: ' + self.refToTrips + ', name: ' + self.name

def createObjects(stopsFile,stopTimesFile,tripsFile,routesFile): # docstringy a open upraviť
    with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
        open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
        open(tripsFile, encoding = "utf-8", newline = "") as tr, \
        open(routesFile, encoding = "utf-8", newline = "") as rt:

    # ak sú súbory v inej zložke, do uvodzoviek dajte adresu
    #with open(r"C:\Users\andre\Desktop\Prog_python\stops.txt", encoding = "utf-8", newline = "") as sp, \
    #    open(r"C:\Users\andre\Desktop\Prog_python\stop_times.txt", encoding = "utf-8", newline = "") as st, \
    #    open(r"C:\Users\andre\Desktop\Prog_python\trips.txt", encoding = "utf-8", newline = "") as tr, \
    #    open(r"C:\Users\andre\Desktop\Prog_python\routes.txt", encoding = "utf-8", newline = "") as rt:
        
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