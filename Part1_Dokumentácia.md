## Dokumentácia part1.py

## Triedy Stop, StopTime, Trip, Route

Z každého riadku každého vstupného súboru (`stops.txt`, `stop_times.txt`, `trips.txt`, `routes.txt`) bude vytvorený objekt odpovedajúcej triedy. Každý atribút má definovaný getter, atribúty s definovaným setterom sú označené (s). Každá trieda má definovanú metódu `__str__`, ktorá vypíše do konzoly všetky atribúty daného objektu.

### Atribúty:

class Stop:

>>id: id of the stop<br/>
>>name: name of the stop<br/>
>>stopLat: lattitude of the stop<br/>
>>stopLon: longitude of the stop<br/>
>>refToSTs (s): reference to stop times (empty list, will be modified later)<br/>

class StopTime:

>>refToTrip (s): trip id of the stop time<br/>
>>arrivalTime: arrival time of the stop time<br/>
>>departureTime: departure time of the stop time<br/>
>>refToStop (s): stop id of the stop time<br/>

class Trip:

>>trip_id: trip id of the trip<br/>
>>refToRoute (s): route id of the trip<br/>
>>tripHeadsign: headsign of the trip<br/>
>>refToSTs (s): reference to stop times (empty list, will be modified later)<br/>


class Route:
>>route_id: id of the route<br/>
>>name: short name of the route<br/>
>>routeLongName: long name of the route<br/>
>>refToTrips (s): reference to trips (empty list, will be modified later)<br/>

##### V čase vzniku v atribútoch `refTo...` NIE SÚ správne referencie na ostatné objekty. Tieto atribúty sú modifikované v priebehu programu.

### Funkcia createObjects(stopsFile, stopTimesFile, tripsFile, routesFile):

|Názov|createObjects()|
|:---:|:---|
|Popis|Funkcia vyžaduje 4 argumenty, názvy vstupných súborov, typ string<br/> Funkcia načíta vstupné súbory, skontroluje ich validitu, vytvorí 6 slovníkov a vytvorí a uloží do nich objekty|
|Argumenty|`stopsFile` - názov textového súboru obsahujúceho informácie o zastávkach (`stops.txt`) <br/> `stopTimesFile` - názov textového súboru obsahujúceho informácie o zastaveniach na zastávkach (`stop_times.txt`)<br/> `tripsFile` - názov textového súboru obsahujúceho informácie o jazdách liniek (`trips.txt`)<br/> `routesFile` - názov textového súboru obsahujúceho informácie o linkách (`routes.txt`)|
|Návratová hodnota|tuple 6 slovníkov|

Funkcia v `try` bloku kontroluje, či vstupné súbory nie sú prázdne - atribút `st_size` funkcie `stat` z modulu `os` obsahujúci počet riadkov je v takom prípade rovný nule; či obsahujú všetky atribúty (stĺpce), ktoré sú potrebné na chod programu - smyčkou cez prvý riadok textových súborov, ktorý obsahuje názvy parametrov, sa kontroluje prítomnosť jednotlivých atribútov. Ak je niektorý zo súborov prázdny alebo niektorý z atribútov chýba, program sa ukončí.

Funkcia prechádza cez textové súbory a vytvára a vráti 6 slovníkov: 

1. `stops`: key: stop_id, value: objekt triedy Stop
2. `stopTimesStop_id`: key: stop_id, value: list objektov triedy StopTime
3. `stopTimesTrip_id`: key: trip_id, value: list objektov triedy StopTime
4. `tripsRoute_id`: key: stop_id, value: list objektov triedy Trip
5. `tripsTrip_id`: key: stop_id, value: objekt triedy Trip
6. `routes`: key: stop_id, value: objekt triedy Route

Čítanie súboru a indexovanie slovníkov a vstupných parametrov pri inicializácii objektov je riešené použitím `DictReader` z modulu `csv`.

Pre objekty tried, ktoré obsahujú dva typy id, `StopTime` - stop_id a trip_id, a `Trip` - trip_id a route_id, je výhodné vytvoriť dva druhy slovníkov, v jednom sú zoradené podľa jedného id, v druhom podľa druhého id, viď slovníky 2., 3., 4., 5. Value slovníkov v takom prípade obsahuje zoznam, kde sa objekt pripojí v prípade, že kľúč s daným id sa už v slovníku nachádza.
