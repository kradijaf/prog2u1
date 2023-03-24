from os.path import exists, isdir       # import pouze potřebného
from requests import get
from zipfile import ZipFile
from csv import reader
from Route import Route
from Trip import Trip
from StopTime import StopTime
from StopSegment import StopSegment
from Stop import Stop
from math import floor
from prettytable import PrettyTable
from datetime import date

# open files, create dictionaries of objects
def createObjects(stopsFile : str, stopTimesFile : str, tripsFile : str, routesFile : str) -> tuple[dict, dict, dict, dict, dict, dict]:
    """Creates 6 dictionaries: 1. stops, 2. stopTimesStop_id, 3. stopTimesTrip_id, 4. tripsRoute_id, 5. tripsTrip_id, 6. routes:
    
    1. key: stop_id; value: class Stops object with atributes: id, name, stopLat, stopLon, refToSTs \n 
    2. key: stop_id; values: class StopTime objects with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    3. key: trip_id; values: class StopTime objects with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    4. key: route_id; values: class Trip objects with atributes: refToSTs, refToRoute, tripHeadsign \n 
    5. key: trip_id; value: class Trip object with atributes: refToSTs, refToRoute, tripHeadsign \n 
    6. key: route_id; value: class Route object with atributes: refToTrips, name, routeLongName \n 
    
    Object atributes named "ref..." are supposed to be modified, they do NOT represent correct references to other objects at the time of their initialization"""
    
    try:
        with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
            open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
            open(tripsFile, encoding = "utf-8", newline = "") as tr, \
            open(routesFile, encoding = "utf-8", newline = "") as rt:
            pass
    except FileNotFoundError as err:
        print('File not found: ' + str(err))
        quit()
    except PermissionError as err:
        print('Reading from the file is not permitted: ' + str(err))
        quit()
    except Exception as err:
        print('Unexpected error: ' + str(err))
        quit()
  
    # open the files a store the data as readers
    with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
        open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
        open(tripsFile, encoding = "utf-8", newline = "") as tr, \
        open(routesFile, encoding = "utf-8", newline = "") as rt:
        reader_sp = reader(sp, delimiter=",")
        reader_st = reader(st, delimiter=",")
        reader_tr = reader(tr, delimiter=",")
        reader_rt = reader(rt, delimiter=",")
    
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
            # the same procedure as before
            if trLine[0] in tripsRoute_id:
                tripsRoute_id[(trLine[0])].append(temporaryObjectTR)
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

def sort_Segments(stopSegments) -> None:
    '''
        method for calling method merge soft
        
        Parameters:
        -----------
        stopSegments:
            array of object (class StopSegment) to sort

        Return value:
        -------------
        sorted array
        '''
    return merge_sort(stopSegments)
    
def busiest(stopSegments, date) -> None:
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
    sort_Segments(array)
    table = PrettyTable(['Start', 'Finish', 'Number of trips', 'Routes'])
    for item in array[:5]:
        table.add_row([item.start, item.finnish, item.counter, ''])
        routes=[]
        for trip in item.trips:
            """
            in arguments must be date, object of class Calendar 
            if trip.is_available(date):
                routes.append(trip.reftoRoute.name)
            """
            routes.append(trip.refToRoute.name)
        set_routes = set(routes)
        routes = list(set_routes)
        routes = sorted(routes)
        for route in routes:
            table.add_row(['', '', '', route])
    print(table)
    
def create_StopSegments(stopTimesS) -> None:
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
    print(len(stopTimesS.values()))
    counter = 0
    for stopTime in stopTimesS.values():
        counter += len(stopTime)
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
    print(counter)
    return stopSegments

"""
if (not exists('gtfs')) or (not isdir('gtfs')):     # ve složce není nic s názvem 'PID_GTFS' nebo to není složka
    r = get('http://data.pid.cz/PID_GTFS.zip')      # získání dat
    
    with open('PID_GTFS.zip', 'wb') as saveTo:      # uložení dat
        saveTo.write(r.content)

    with ZipFile('PID_GTFS.zip', 'r') as myZip:     # přístup k ZIP souboru
        files = ('stops', 'stop_times', 'trips', 'routes', 'calendar', 'calendar_dates')
        for file in files:
            myZip.extract(f'{file}.txt', 'gtfs')        # extrakce dat do /gtfs
"""
# funkcia potrebuje ako argumenty názvy súborov, alebo ich napíšte priamo do "with" 
stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes = createObjects("Test\\stops.txt", "Test\\stop_times.txt",
                                                                                                "Test\\trips.txt", "Test\\routes.txt")
stopTimes = referenceObjects(stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes)
# príklad, ako získať objekt
stopSegments = create_StopSegments(stopTimes)
datum = date(2023,3,22)
busiest(stopSegments, datum)