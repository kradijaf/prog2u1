from cast1 import *

def __deleteUnreferenced(stopTimes : dict) -> dict:
    """Deletes StopTime object from input dictionary if it´s not connected to all other classes."""
    for (key, stopTime) in stopTimes.items():
        if (not isinstance(stopTime.refToStop, Stop)) or (not isinstance(stopTime.refToTrip, Trip))\
        or (isinstance(stopTime.refToTrip, Trip) and not isinstance(stopTime.refToTrip.refToRoute, Route)):
            stopTimes.pop(key)

    return stopTimes

def referenceObjects(stops : dict, stopTimesS : dict, stopTimesT : dict, tripsT : dict, tripsR : dict, routes : dict) -> tuple[dict, dict, dict, dict, dict, dict]:
    """Creates two-way references between Stop, StopTime, Trip and Route objects.\n

    Creates direct references between these classes:\n
        Stop - StopTime (via stop_id)\n
        StopTime - Trip (via trip_id)\n
        Trip - Route (via route_id).\n
    
    Deletes each StopTime object which couldn´t be connected to each of remaining 3 classes (Stop, Trip, Route).\n
    Returns dictionary only containing StopTime objects connected to all remaining classes."""
    for (key, stop) in stops.items():       # connection of Stop and StopTime objects
        stopTimes = stopTimesS[key]     # all stopTime objects with stop_id equal to key
        for stopTime in stopTimes:
            stopTime.refToStop = stop       
            stop.refToSTs.append(stopTime)

    for (key, trip) in tripsT.items():      # connection of Trip and StopTime objects
        stopTimes = stopTimesT[key]     # all stopTime objects with trip_id equal to key
        for stopTime in stopTimes:
            stopTime.refToTrip = trip       
            trip.refToSTs.append(stopTime)

    for (key, route) in routes.items():      # connection of Route and Trip objects
        trips = tripsR[key]     # all Trip objects with route_id equal to key
        for trip in trips:
            trip.refToRoute = route       
            route.refToTrips.append(stopTime)

    return __deleteUnreferenced(stopTimesS)

# stačí zavolat referenceObjects()