# Prvá časť, načítanie dát, vytvorenie tried, vytvorenie objektov
# First part - loading data, definition of classes, initialization of objects, creation of dictionaries

import csv

class Stop():
    
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

class StopTime():

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

class Trip():
    
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

class Route():

    # initialization variables
    def __init__(self, route_id, route_short_name, route_long_name):
        self.__route_id = route_id
        self.__refToTrips = []
        self.__name = route_short_name
        self.__routeLongName = route_long_name

    def __str__(self):
        return 'route_id: ' + self.__route_id + ', refToTrips: ' + self.__refToTrips + ', name: ' + self.__name + ', routeLongName: ' + str(self.__routeLongName)
    
    # necessary getters and setters
    @property
    def route_id(self):
        return self.__route_id

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
def createObjects(): #(stopsFile,stopTimesFile,tripsFile,routesFile) -> tuple[dict, dict, dict, dict, dict, dict]: # docstringy a open upraviť
    """Creates 6 dictionaries: 1. stops, 2. stopTimesStop_id, 3. stopTimesTrip_id, 4. tripsRoute_id, 5. tripsTrip_id, 6. routes:
    
    1. key: stop_id; value: class Stops object with atributes: id, name, stopLat, stopLon, refToSTs \n 
    2. key: stop_id; values: class StopTime objects with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    3. key: trip_id; values: class StopTime objects with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    4. key: route_id; values: class Trip objects with atributes: refToSTs, refToRoute, tripHeadsign \n 
    5. key: trip_id; value: class Trip object with atributes: refToSTs, refToRoute, tripHeadsign \n 
    6. key: route_id; value: class Route object with atributes: refToTrips, name, routeLongName \n 
    
    Object atributes named "ref..." are supposed to be modified, they do NOT represent correct references to other objects at the time of their initialization"""
    
    #with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
    #    open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
    #    open(tripsFile, encoding = "utf-8", newline = "") as tr, \
    #    open(routesFile, encoding = "utf-8", newline = "") as rt:

    # ak sú súbory v inej zložke, do uvodzoviek dajte adresu

    # check if the input files are valid
    try:
        with open(r"C:\Users\andre\Desktop\Prog_python\stops.txt", encoding = "utf-8", newline = "") as sp, \
            open(r"C:\Users\andre\Desktop\Prog_python\stop_times.txt", encoding = "utf-8", newline = "") as st, \
            open(r"C:\Users\andre\Desktop\Prog_python\trips.txt", encoding = "utf-8", newline = "") as tr, \
            open(r"C:\Users\andre\Desktop\Prog_python\routes.txt", encoding = "utf-8", newline = "") as rt:
            pass
    except FileNotFoundError as err:
        print('File not found: ' + str(err))
        quit()
    except PermissionError as err:
        print('Reading from the file is not permitted: ' + str(err))
        quit()
    except NotImplementedError as err:
        print(str(err))
        quit()
    except Exception as err:
        print('Unexpected error: ' + str(err))
        quit()

    # open the files a store the data as readers
    with open(r"C:\Users\andre\Desktop\Prog_python\stops.txt", encoding = "utf-8", newline = "") as sp, \
        open(r"C:\Users\andre\Desktop\Prog_python\stop_times.txt", encoding = "utf-8", newline = "") as st, \
        open(r"C:\Users\andre\Desktop\Prog_python\trips.txt", encoding = "utf-8", newline = "") as tr, \
        open(r"C:\Users\andre\Desktop\Prog_python\routes.txt", encoding = "utf-8", newline = "") as rt:
        reader_sp = csv.reader(sp, delimiter=",")
        reader_st = csv.reader(st, delimiter=",")
        reader_tr = csv.reader(tr, delimiter=",")
        reader_rt = csv.reader(rt, delimiter=",")
        
        # skip the first line - names of the collumns
        next(reader_sp)
        next(reader_st)
        next(reader_tr)
        next(reader_rt)
        
        # create an object for every line in stops.txt => every stop is an object
        stops = {}
        for spLine in reader_sp:
            stops[(spLine[0])] = Stop(spLine[0],spLine[1],spLine[2],spLine[3])

        # create an object for every line in stoptimes.txt => every stoptime is an object
        # objects are stored in two different dictionaries, sorted by stop_id in stopTimesStop_id and sorted by trip_id in stopTimesTrip_id
        stopTimesStop_id = {}
        stopTimesTrip_id = {}
        for stLine in reader_st:
            # create new object from the data on the current line in stoptimes.txt
            temporaryObjectST = StopTime(stLine[0],stLine[1],stLine[2],stLine[3])
            # if the key already exists, append the object to the list in values
            if stLine[3] in stopTimesStop_id:
                stopTimesStop_id[(stLine[3])].append(temporaryObjectST)
            # else add a new key with an object inside a list 
            else:
                stopTimesStop_id[(stLine[3])] = [temporaryObjectST]
            # the same for stopTimesTrip_id
            if stLine[0] in stopTimesTrip_id:
                stopTimesTrip_id[(stLine[0])].append(temporaryObjectST)
            else:
                stopTimesTrip_id[(stLine[0])] = [temporaryObjectST]
        
        # create an object for every line in trips.txt => every trip is an object
        # objects are stored in two different dictionaries, sorted by route_id in tripsRoute_id and sorted by trip_id in tripsTrip_id
        tripsRoute_id = {}
        tripsTrip_id = {}
        for trLine in reader_tr:
            # create new object from the data on the current line in trips.txt
            temporaryObjectTR = Trip(trLine[0],trLine[2],trLine[3])
            # if the key already exists, append the object to the list in values
            if trLine[0] in tripsRoute_id:
                tripsRoute_id[(trLine[0])].append(temporaryObjectTR)
            # else add a new key with an object inside a list 
            else:
                tripsRoute_id[(trLine[0])] = [temporaryObjectTR]
            # trip_id is unique for every line in trips.txt, value of every key is only one object
            tripsTrip_id[(trLine[2])] = temporaryObjectTR

        # create an object for every line in routes.txt => every route is an object
        routes = {}
        for rtLine in reader_rt:
            routes[(rtLine[0])] = Route(rtLine[0],rtLine[2],rtLine[3])

        # function returns 6 dictionaries
        return stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes

# funkcia potrebuje ako argumenty názvy súborov, alebo ich napíšte priamo do "with" časti
stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes = createObjects()
# príklad, ako získať objekt
print((stopTimesStop_id['U953Z102P'][0]))
