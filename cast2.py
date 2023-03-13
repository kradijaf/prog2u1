tripsC = trips[ : ]     # fyzická kopie
for i in range(len(routes)):        # vzájemné propojení objektů Route a Trip:
    indices = []
    for j in range(len(tripsC)):
        if tripsC[j].refToRoute == routes[i].refToTrips:        # nalezen první Trip objekt se shodným route_id
            indices.append(j)
            index = j + 1
            break       

    while (index < len(tripsC)) and (tripsC[index].refToRoute == routes[i].refToTrips):
        indices.append(index)      # přídávání indexů řádků se stejným route_id do seznamu
        index += 1

    if len(indices) > 0:
        routes[i].refToTrips = []       # smazání route_id
        for j in indices:
            routes[i].refToTrips.append(tripsC[j])       # napojení trips na routes
            tripsC[j].refToRoute = routes[i]     # napojení routes na trips
        tripsC = tripsC[ : indices[0]] + tripsC[indices[-1] + 1 : ]     # smazání objektů Route, které již jsou obousměrně propojené

stopTimesC = stopTimes[ : ]
for i in range(len(trips)):        # vzájemné propojení objektů Trip a StopTime:
    indices = []
    for j in range(len(stopTimesC)):
        if stopTimesC[j].refToTrip == trips[i].refToSTs:        # nalezen první StopTime objekt se shodným trip_id
            indices.append(j)
            index = j + 1  
            break       

    while (index < len(stopTimesC)) and (stopTimesC[index].refToTrip == trips[i].refToSTs):
        indices.append(index)      # přídávání indexů řádků se stejným trip_id do seznamu
        index += 1

    if len(indices) > 0:
        trips[i].refToSTs = []       # smazání trip_id
        for j in indices:
            trips[i].refToSTs.append(stopTimesC[j])       # napojení stopTimes na trips
            stopTimesC[j].refToTrip = trips[i]     # napojení trips na stopTimes
        stopTimesC = stopTimesC[ : indices[0]] + stopTimesC[indices[-1] + 1 : ]     # smazání objektů stopTime, které již jsou obousměrně propojené

stopTimesC = stopTimes[ : ]
for i in range(len(stops)):     # vzájemné propojení objektů Stop a StopTime:
    indices = []
    for j in range(len(stopTimesC)):        # prohledávání všech nepropojených objektů StopTime
        if stopTimesC[j].refToStop == stops[i].id:      # hledání objektů se stejným stop_id
            indices.append(j)

    stops[i].refToSTs = []      # tvorba atributu pro propojení s objekty StopTime kvůli zachování atributu stop_id pro další práci

    if len(indices) > 0:
        for j in range(-1, -len(indices) - 1, -1):      # procházení zpětně, aby šlo mazat ze stopTimesC
            stops[i].refToSTs.append(stopTimesC[indices[j]])     # napojení stopTimes na stops
            stopTimesC[indices[j]].refToStop = stops[i]      # napojení stops na stopTimes
            del stopTimesC[indices[j]]       # objekt na nic dalšího nelze napojovat