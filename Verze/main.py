from os.path import exists, isdir       # import pouze potřebného
from requests import get
from zipfile import ZipFile
import csv
from Route import Route
from Trip import Trip
from StopTime import StopTime
from StopSegment import StopSegment
from Stop import Stop
from math import floor
from prettytable import PrettyTable

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
        stopTimesTrip_id = {}
        for idx, stLine in enumerate(reader_st):
            if idx == 0:
                continue
            temporaryObjectST = StopTime(stLine[0],stLine[1],stLine[2],stLine[3])
            # if the key exists, append new object to the list in values
            if stLine[3] in stopTimesStop_id:
                stopTimesStop_id[(stLine[3])].append(temporaryObjectST)
            # else add a new key with an object inside a list 
            else:
                stopTimesStop_id[(stLine[3])] = [temporaryObjectST]
            # same for stopTimesTrip_id
            if stLine[0] in stopTimesTrip_id:
                stopTimesTrip_id[(stLine[0])].append(temporaryObjectST)
            else:
                stopTimesTrip_id[(stLine[0])] = [temporaryObjectST]
        
        tripsRoute_id = {}
        tripsTrip_id = {}
        for idx, trLine in enumerate(reader_tr):
            if idx == 0:
                continue
            temporaryObjectTR = Trip(trLine[0],trLine[2],trLine[3])
            if trLine[0] in tripsRoute_id:
                tripsRoute_id[(trLine[0])].append(temporaryObjectTR)
            else:
                tripsRoute_id[(trLine[0])] = [temporaryObjectTR]
            # tripsTrip_id
            tripsTrip_id[(trLine[2])] = temporaryObjectTR

        routes = {}
        for idx, rtLine in enumerate(reader_rt):
            if idx == 0:
                continue
            routes[(rtLine[0])] = Route(rtLine[0],rtLine[2],rtLine[3])

        # function returns 6 dictionaries
        return stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes

def __deleteUnreferenced(stopTimesDict : dict) -> dict:
    """Deletes all StopTime objects unconnected to all other classes. If list 
    containing StopTime objects is empty, deletes its key from input dictionary.\n
    
    Returns input dictionary only containing StopTime objects connected to all other classes in each record."""
    toPop = []      # invalid records in input dictionary
    for (key, stopTimes) in stopTimesDict.items():      # iterates through each list of StopTime objects
        validObjects = []       # list to replace the old one
        for stopTime in stopTimes:      
            if (isinstance(stopTime.refToStop, Stop)) and (isinstance(stopTime.refToTrip, Trip)\
            and isinstance(stopTime.refToTrip.refToRoute, Route)):        # if it´s connected to all other classes    
                validObjects.append(stopTime)

        if validObjects == []:      # record contains 0 StopTime objects connected to all other classes
            toPop.append(key)
        else:       # replacement of invalid StopTime objects with valid ones
            stopTimesDict[key] = validObjects  

    for key in toPop:       # deleting of invalid records in input dictionary
        stopTimesDict.pop(key)
    return stopTimesDict

def referenceObjects(stops : dict, stopTimesS : dict, stopTimesT : dict, tripsR : dict, tripsT : dict, routes : dict) -> tuple[dict, dict, dict, dict, dict, dict]:
    """Creates two-way references between Stop, StopTime, Trip and Route objects.\n
    Creates direct references between these classes:\n
        Stop - StopTime (via stop_id)\n
        StopTime - Trip (via trip_id)\n
        Trip - Route (via route_id).\n
    
    Deletes each StopTime object which couldn´t be connected to each of remaining 3 classes (Stop, Trip, Route).\n
    Returns dictionary only containing StopTime objects connected to all remaining classes."""
    for (key, stop) in stops.items():       # connection of Stop and StopTime objects
        try:
            stopTimes = stopTimesS[key]     # all stopTime objects with stop_id equal to key
        except KeyError:        # if StopTime objects with stop_id equal to key don´t exist:
            continue
        else:       # if Stop objects to reference to exist:
            for stopTime in stopTimes:
                stopTime.refToStop = stop       
                stop.refToSTs.append(stopTime)

    for (key, trip) in tripsT.items():      # connection of Trip and StopTime objects
        try:
            stopTimes = stopTimesT[key]     # all stopTime objects with trip_id equal to key
        except KeyError:        # if StopTime objects with trip_id equal to key don´t exist:
            continue
        else:       # if StopTime objects to reference to exist:
            for stopTime in stopTimes:
                stopTime.refToTrip = trip       
                trip.refToSTs.append(stopTime)

    for (key, route) in routes.items():      # connection of Route and Trip objects
        try:
            trips = tripsR[key]     # all Trip objects with route_id equal to key
        except KeyError:        # if Trip objects with route_id equal to key don´t exist:
            continue
        else:       # if Trip objects to reference to exist:
            for trip in trips:
                trip.refToRoute = route       
                route.refToTrips.append(trip)

    return __deleteUnreferenced(stopTimesT)

def merge_sort(array : list) -> list:
    '''
        sorting array of objects of stopSegments using merge sort
        
        Parameters:
        ----------
        array :
            array of object (class StopSegment) to sort
        
        Return value:
        -------------
        array:
            sorted array
    '''
    if len(array) > 1:
        sorted_1 = merge_sort(array[:floor(len(array)/2)])
        sorted_2 = merge_sort(array[floor(len(array)/2):])
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
    
def busiest(stopSegments) -> None:
    '''
        calculating and printing five busiest stopSegments
        
        Parameters:
        ----------
        stopSegments:
            dictionary  key:    stop_id of starting station + stop_id of terminating station
                        value:  object of class StopSegment
        date:
            object of class datetime.date

        Return value:
        -------------
        None
    '''
    array = []
    for item in stopSegments.values():
        array.append(item)
    merge_sort(array)
    table = PrettyTable(['Start', 'Finish', 'Number of trips', 'Routes'])
    for item in array[:min(5, len(array))]:
        table.add_row([item.start, item.finish, item.counter, ''])
        routes=[]
        for trip in item.trips:
            routes.append(trip.refToRoute.name)
        set_routes = set(routes)
        routes = list(set_routes)
        routes = sorted(routes)
        for route in routes:
            table.add_row(['', '', '', route])
    print(table)
    
def create_StopSegments(stopTimesT) -> None:
    '''
        method for creating objects of class StopSegment
        
        Parameters:
        ----------
        stopTimes:
            dictionary  key:    stop_id of related trip
                        value:  array of object class StopTime

        Return value:
        -------------
        stopSegments:
            dictionary  key:    stop_id of starting station + stop_id of terminating station
                        value:  object of class StopSegment
    '''
    stopSegments = {}
    start = None
    finish = None
    start_id = None
    finish_id = None
    for stopTime in stopTimesT.values():

        start = stopTime[0].refToStop.name
        start_id = stopTime[0].refToStop.id
        for item in stopTime[1:]:
            finish = item.refToStop.name
            finish_id = item.refToStop.id

            Segment = stopSegments.get(start_id + finish_id)
            if not Segment:
                stopSegments[start_id + finish_id] = StopSegment(start, finish)
                stopSegments[start_id + finish_id].trips.append(item.refToTrip)
            else:
                Segment.counter += 1
                Segment.trips.append(item.refToTrip)
            start = finish
            start_id = finish_id
    return stopSegments

if (not exists('gtfs')) or (not isdir('gtfs')):     # ve složce není nic s názvem 'PID_GTFS' nebo to není složka
    r = get('http://data.pid.cz/PID_GTFS.zip')      # získání dat
    
    with open('PID_GTFS.zip', 'wb') as saveTo:      # uložení dat
        saveTo.write(r.content)

    with ZipFile('PID_GTFS.zip', 'r') as myZip:     # přístup k ZIP souboru
        files = ('stops', 'stop_times', 'trips', 'routes', 'calendar', 'calendar_dates')
        for file in files:
            myZip.extract(f'{file}.txt', 'gtfs')        # extrakce dat do /gtfs

# funkcia potrebuje ako argumenty názvy súborov, alebo ich napíšte priamo do "with" 
stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes = createObjects("gtfs\\stops.txt", "gtfs\\stop_times.txt",
                                                                                                "gtfs\\trips.txt", "gtfs\\routes.txt")
stopTimes = referenceObjects(stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes)
stopSegments = create_StopSegments(stopTimes)
busiest(stopSegments)