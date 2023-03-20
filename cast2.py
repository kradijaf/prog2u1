def referenceObjects(stops : dict, stopTimesS : dict, stopTimesT : dict, tripsT : dict, tripsR : dict, routes : dict) -> tuple[dict, dict, dict, dict, dict, dict]:
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