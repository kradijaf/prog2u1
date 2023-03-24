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
