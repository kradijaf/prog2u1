# Prvá časť, načítanie dát, vytvorenie tried, vytvorenie objektov

# To Do:
# private metódy
# pridať try except 
# komentáre
# všetko čo čítame z readeru je automaticky string?
# nedá sa obísť if idx == 0: continue ?

import csv

class Stop():
    
    def __init__(self, stop_id, stop_name, stop_lat, stop_lon):
        self.__id = stop_id
        self.__name = stop_name
        self.__stopLat = stop_lat
        self.__stopLon = stop_lon
        self.__refToSTs = []

    def __str__(self):
        return 'id: ' + str(self.__id) + ', name: ' + str(self.__name) + ', stopLat: ' + str(self.__stopLat) \
                + ', stopLon: ' + str(self.__stopLon) + ', refToSTs: ' + str(self.__refToSTs)
    
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

class StopTime():

    def __init__(self, trip_id, arrival_time, departure_time, stop_id):
        self.__refToStop = stop_id
        self.__refToTrip = trip_id
        self.__arrivalTime = arrival_time
        self.__departureTime = departure_time

    def __str__(self):
        return 'refToStop: ' + self.__refToStop + ', refToTrip: ' + self.__refToTrip + ', arrivalTime: ' \
                + str(self.__arrivalTime) + ', departureTime: ' + str(self.__departureTime)
    
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

class Trip():
    
    def __init__(self, trip_id, route_id, trip_headsign):
        self.__refToSTs = []
        self.__refToRoute = route_id
        self.__tripHeadsign = trip_headsign

    def __str__(self):
        return 'refToRoute: ' + self.__refToRoute + ', refToSTs: ' + self.__refToSTs + ', tripHeadSign: ' + str(self.__tripHeadsign)

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

class Route():

    def __init__(self, route_id, route_short_name, route_long_name):
        self.__refToTrips = []
        self.__name = route_short_name
        self.__routeLongName = route_long_name

    def __str__(self):
        return 'refToTrips: ' + self.__refToTrips + ', name: ' + self.__name + ', routeLongName: ' + str(self.__routeLongName)
    
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

# open files, create dictionaries of objects
def createObjects(stopsFile,stopTimesFile,tripsFile,routesFile) -> tuple[dict, dict, dict, dict, dict, dict]: # docstringy a open upraviť
    """Creates 4 dictionaries: 1. stops, 2. stopTimesStop_id, 3. stopTimesTrip_id, 4. tripsRoute_id, 5. tripsTrip_id, 6. routes:
    
    1. key: stop_id; value: class Stops object with atributes: id, name, stopLat, stopLon, refToSTs \n 
    2. key: stop_id; value: class StopTime object with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    3. key: trip_id; value: class StopTime object with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    4. key: route_id; value: class Trip object with atributes: refToSTs, refToRoute, tripHeadsign \n 
    5. key: trip_id; value: class Trip object with atributes: refToSTs, refToRoute, tripHeadsign \n 
    6. key: route_id; value: class Route object with atributes: refToTrips, name, routeLongName \n 
    
    Object atributes named "ref..." are supposed to be modified, they do NOT represent correct references to other objects at the time of their initialization"""
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
        
        stops = {}
        for idx, spLine in enumerate(reader_sp):
            if idx == 0:
                continue
            stops[(spLine[0])] = Stop(spLine[0],spLine[1],spLine[2],spLine[3])

        stopTimesStop_id = {}
        for idx, stLine in enumerate(reader_st):
            if idx == 0:
                continue
            # if the key exists, append new object to the list in values
            if stLine[3] in stopTimesStop_id:
                stopTimesStop_id[(stLine[3])].append(StopTime(stLine[0],stLine[1],stLine[2],stLine[3]))
            # else add a new key with an object inside a list 
            else:
                stopTimesStop_id[(stLine[3])] = [StopTime(stLine[0],stLine[1],stLine[2],stLine[3])]

        stopTimesTrip_id = {}
        # seek(0) sa vráti na prvý riadok st, inak sa nenačítajú dáta, po predošlej smyčke sme na poslednom riadku
        st.seek(0)
        for idx, stLine in enumerate(reader_st):
            if idx == 0:
                continue
            if stLine[0] in stopTimesTrip_id:
                stopTimesTrip_id[(stLine[3])].append(StopTime(stLine[0],stLine[1],stLine[2],stLine[3]))
            else:
                stopTimesTrip_id[(stLine[3])] = [StopTime(stLine[0],stLine[1],stLine[2],stLine[3])]
        
        tripsRoute_id = {}
        for idx, trLine in enumerate(reader_tr):
            if idx == 0:
                continue
            if trLine[0] in tripsRoute_id:
                tripsRoute_id[(stLine[3])].append(Trip(trLine[0],trLine[2],trLine[3]))
            else:
                tripsRoute_id[(stLine[3])] = [Trip(trLine[0],trLine[2],trLine[3])]

        tripsTrip_id = {}
        # seek(0) sa vráti na prvý riadok tr
        tr.seek(0)
        for idx, trLine in enumerate(reader_tr):
            if idx == 0:
                continue
            tripsTrip_id[(trLine[2])] = Trip(trLine[0],trLine[2],trLine[3])

        routes = {}
        for idx, rtLine in enumerate(reader_rt):
            if idx == 0:
                continue
            routes[(rtLine[0])] = Route(rtLine[0],rtLine[2],rtLine[3])

        # function returns 6 dictionaries
        return stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes

# funkcia potrebuje ako argumenty názvy súborov, alebo ich napíšte priamo do "with" časti
stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes = createObjects()
# príklad, ako získať objekt
print((stopTimesStop_id['U953Z102P'][1]))