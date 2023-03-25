try:
    from os.path import exists, isdir       # importing only the necesarry stuff
    from requests import get
    from zipfile import ZipFile
    from csv import DictReader
    from os import stat
    from Route import Route
    from Trip import Trip
    from StopTime import StopTime
    from StopSegment import StopSegment
    from Stop import Stop
    from math import floor
    from prettytable import PrettyTable
except ImportError as e:
    raise SystemExit(f'Couldn´t import module: {e.name}. Check if it´s installed.')

def dataPrep():
    if (not exists('gtfs')) or (not isdir('gtfs')):     # nothing in own folder is named 'gtfs' or it´s not a folder
        r = get('http://data.pid.cz/PID_GTFS.zip')      # accessing the data
        
        with open('PID_GTFS.zip', 'wb') as saveTo:      # saving the data
            saveTo.write(r.content)

        with ZipFile('PID_GTFS.zip', 'r') as myZip:     # access to ZIP file
            files = ('stops', 'stop_times', 'trips', 'routes', 'calendar', 'calendar_dates')
            for file in files:
                myZip.extract(f'{file}.txt', 'gtfs')        # extraction of the data into /gtfs

def createObjects(stopsFile : str, stopTimesFile : str, tripsFile : str, routesFile : str) -> tuple[dict, dict, dict, dict, dict, dict]:
    """Creates 6 dictionaries: 1. stops, 2. stopTimesStop_id, 3. stopTimesTrip_id, 4. tripsRoute_id, 5. tripsTrip_id, 6. routes:
    
    1. key: stop_id; value: class Stops object with atributes: id, name, stopLat, stopLon, refToSTs \n 
    2. key: stop_id; values: class StopTime objects with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    3. key: trip_id; values: class StopTime objects with atributes: refToStop, refToTrip, arrivalTime, departureTime \n 
    4. key: route_id; values: class Trip objects with atributes: refToSTs, refToRoute, tripHeadsign \n 
    5. key: trip_id; value: class Trip object with atributes: refToSTs, refToRoute, tripHeadsign \n 
    6. key: route_id; value: class Route object with atributes: refToTrips, name, routeLongName \n 
    
    Object atributes named "ref..." are supposed to be modified, they do NOT represent correct references to other objects at the time of their initialization"""
    
    # check if the input files are valid
    try:
        with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
            open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
            open(tripsFile, encoding = "utf-8", newline = "") as tr, \
            open(routesFile, encoding = "utf-8", newline = "") as rt:
                
                # if the file/s are empty, notify the user
                endProg = False # if changed to True at any point, the script will be terminated later
                if stat(stopsFile).st_size == 0:
                    print('File', stopsFile, 'is empty.')
                    endProg = True
                if stat(stopTimesFile).st_size == 0:
                    print('File', stopTimesFile, 'is empty.')
                    endProg = True
                if stat(tripsFile).st_size == 0:
                    print('File', tripsFile, 'is empty.')
                    endProg = True
                if stat(routesFile).st_size == 0:
                    print('File', routesFile, 'is empty.')
                    endProg = True

                # check the first line of the textfile for required attributes, otherwise set endProg to True
                sp_firstLine = sp.readline().strip('\n').split(sep=',')
                st_firstLine = st.readline().strip('\n').split(sep=',')
                tr_firstLine = tr.readline().strip('\n').split(sep=',')
                rt_firstLine = rt.readline().strip('\n').split(sep=',')
                if all(x in sp_firstLine for x in ['stop_id','stop_name','stop_lat','stop_lon']) == False:
                    print('File', stopsFile, 'is not valid.')
                    endProg = True
                if all(x in st_firstLine for x in ['trip_id', 'arrival_time', 'departure_time', 'stop_id']) == False:
                    print('File', stopTimesFile, 'is not valid.')
                    endProg = True
                if all(x in tr_firstLine for x in ['trip_id', 'route_id', 'trip_headsign']) == False:
                    print('File', tripsFile, 'is not valid.')
                    endProg = True
                if all(x in rt_firstLine for x in ['route_id', 'route_short_name', 'route_long_name']) == False:
                    print('File', routesFile, 'is not valid.')
                    endProg = True

                # terminate if one of the previous checks failed
                if endProg == True:
                    quit()

    except FileNotFoundError as err:
        print('File not found: ' + str(err))
        quit()
    except PermissionError as err:
        print('Reading from the file is not permitted: ' + str(err))
        quit()

  
    # open the files a store the data as readers
    with open(stopsFile, encoding = "utf-8", newline = "") as sp, \
        open(stopTimesFile, encoding = "utf-8", newline = "") as st, \
        open(tripsFile, encoding = "utf-8", newline = "") as tr, \
        open(routesFile, encoding = "utf-8", newline = "") as rt:

        reader_sp = DictReader(sp, delimiter=",")
        reader_st = DictReader(st, delimiter=",")
        reader_tr = DictReader(tr, delimiter=",")
        reader_rt = DictReader(rt, delimiter=",")

        # create an object for every line in stops.txt => every stop is an object
        stops = {}
        for spLine in reader_sp:
            stops[(spLine['stop_id'])] = Stop(spLine['stop_id'],spLine['stop_name'],spLine['stop_lat'],spLine['stop_lon'])

        # create an object for every line in stoptimes.txt => every stoptime is an object
        # objects are stored in two different dictionaries, sorted by stop_id in stopTimesStop_id and sorted by trip_id in stopTimesTrip_id
        stopTimesStop_id = {}
        stopTimesTrip_id = {}
        for stLine in reader_st:
            # create new object from the data on the current line in stoptimes.txt
            temporaryObjectST = StopTime(stLine['trip_id'],stLine['arrival_time'],stLine['departure_time'],stLine['stop_id'])
            # if the key already exists, append the object to the list in values
            if stLine['stop_id'] in stopTimesStop_id:
                stopTimesStop_id[(stLine['stop_id'])].append(temporaryObjectST)
            # else add a new key with an object inside a list 
            else:
                stopTimesStop_id[(stLine['stop_id'])] = [temporaryObjectST]
            # the same for stopTimesTrip_id
            if stLine['trip_id'] in stopTimesTrip_id:
                stopTimesTrip_id[(stLine['trip_id'])].append(temporaryObjectST)
            else:
                stopTimesTrip_id[(stLine['trip_id'])] = [temporaryObjectST]
        
        # create an object for every line in trips.txt => every trip is an object
        # objects are stored in two different dictionaries, sorted by route_id in tripsRoute_id and sorted by trip_id in tripsTrip_id
        tripsRoute_id = {}
        tripsTrip_id = {}
        for trLine in reader_tr:
            # create new object from the data on the current line in trips.txt
            temporaryObjectTR = Trip(trLine['trip_id'],trLine['route_id'],trLine['trip_headsign'])
            # the same procedure as before
            if trLine['route_id'] in tripsRoute_id:
                tripsRoute_id[(trLine['route_id'])].append(temporaryObjectTR) 
            else:
                tripsRoute_id[(trLine['route_id'])] = [temporaryObjectTR]
            # trip_id is unique for every line in trips.txt, value of every key is only one object
            tripsTrip_id[(trLine['trip_id'])] = temporaryObjectTR

        # create an object for every line in routes.txt => every route is an object
        routes = {}
        for rtLine in reader_rt:
            routes[(rtLine['route_id'])] = Route(rtLine['route_id'],rtLine['route_short_name'],rtLine['route_long_name'])

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
            if (isinstance(stopTime.refToStop, Stop)) and (isinstance(stopTime.refToTrip, Trip))\
            and isinstance(stopTime.refToTrip.refToRoute, Route):        # if it´s connected to all other classes    
                validObjects.append(stopTime)

        if validObjects == []:      # record contains 0 StopTime objects connected to all other classes
            toPop.append(key)
        else:       # replacement of invalid StopTime objects with valid ones
            stopTimesDict[key] = validObjects  

    for key in toPop:       # deleting of invalid records in input dictionary
        stopTimesDict.pop(key)
    if not stopTimesDict:
        raise SystemExit('StopTime objects from which Stop, Trip and Route can be accesed don´t exist. Further calculations can´t be done.')
    
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
    if len(array) < 5:
        print(f"Cannot be listed 5 the busiest sections. Only {len(array)} sections were found.")
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
    if not stopTimesT:
        print("Cannot be created any sections.")
        quit()
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
try:
    # preparation of the data if they don´t exist
    dataPrep()
    # funkcia potrebuje ako argumenty názvy súborov, alebo ich napíšte priamo do "with" 
    stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes = createObjects("gtfs\\stops.txt", "gtfs\\stop_times.txt",
                                                                                                    "gtfs\\trips.txt", "gtfs\\routes.txt")
    stopTimes = referenceObjects(stops, stopTimesStop_id, stopTimesTrip_id, tripsRoute_id, tripsTrip_id, routes)
    # príklad, ako získať objekt
    stopSegments = create_StopSegments(stopTimes)
    busiest(stopSegments)
except PermissionError:
    raise SystemExit('Can´t write into this folder.')
except OSError as e:
    raise SystemExit(f'OS Error: {e}.')
except Exception as e:
    raise SystemExit(f'Unexpected error: {e}.')
