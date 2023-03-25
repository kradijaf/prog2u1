# Vývojárska dokumentácia

Program main.py načíta cestovné poriadky z formátu [GTFS](https://developers.google.com/transit/gtfs/reference) a určí najfrekventovanejší medzizastávkový úsek.

## Triedy

Pre každý súbor existuje jemu odpovedajúca trieda: __Stop, StopTime, Trip, Route__

Z každého riadku každého vstupného súboru (`stops.txt`, `stop_times.txt`, `trips.txt`, `routes.txt`) je vytvorený objekt odpovedajúcej triedy. Každý atribút má definovaný getter, atribúty s definovaným setterom sú označené (s). Každá trieda má definovanú metódu `__str__`, ktorá vypíše do konzoly všetky atribúty daného objektu.

#### Atribúty:

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

V rámci výpočtu frekvencie dopravy na medzizastávkových úsekoch bola implementovaná trieda __StopSegment:__

Třída __StopSegment__ simuluje mezizastávkový úsek, úsek mezi dvěma po sobě následujícími zastávkami<br/>

__Datové položky:__
>>start - název počáteční stanice<br/>
>>finish - název konečné stanice<br/>
>>counter - počet souvisejících objektů třídy Trip<br/>
>>trips - pole souvisejících objektů třídy Trip<br/>

__Metody:__
>>\__add_trip(trip):<br/>
>>>> přidání objektu třídy Trip do pole trips<br/>

## Funkcie

Skript je členený do nasledujúcich funkcií:

1. `dataPrep()` 

|Název|dataPrep()|
|:---:|:---|
|Popis|Funkce ve své složce kontroluje následující vlastnosti dat:<br/> - zda existuje soubor pojmenovaný `gtfs`<br/> - zda je složkou|
|Argumenty|-|
|Návratová hodnota|None|

Pokud alespoň jedna podmínka není splněna, z webu http://data.pid.cz/PID_GTFS.zip ukládá do své složky data jako `PID_GTFS.zip`. Z tohoto souboru následně extrahuje soubory `stops.txt`, `stop_times.txt`, `trips.txt` a `routes.txt` do složky `\gtfs`, tu vytváří ve své složce.

2. `createObjects()`

|Názov|createObjects()|
|:---:|:---|
|Popis|Funkcia načíta vstupné súbory, skontroluje ich validitu, vytvorí 6 slovníkov a vytvorí a uloží do nich objekty|
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

3. `referenceObjects()` 

|Název|referenceObjects()|
|:---:|:---|
|Popis|Funkce propojuje objekty `Stop`, `StopTime`, `Trip` a `Route`.|
|Argumenty|Slovníky `stops`, `stopTimesStop_id`, `stopTimesTrip_id`, `tripsRoute_id`, `tripsTrip_id`, `routes`|
|Návratová hodnota|`__deleteUnreferenced(stopTimesT)` -> `stopTimesDict`, viď 4.|

Do atributu `refTo<objekt(y)>` vkládá příslušný počet objektů se stejnou hodnotou identifikátoru, skrz který jsou provázat. Veškeré vstupní slovníky jsou indexované podle jednoho identifikátoru. Funkce tedy pro každou kombinaci slovníků `stops–stopTimesStop_id`, `tripsTrip_id–stopTimesTrip_id` a `routes–tripsRoute_id` iteruje skrz první slovník a pro každý objekt v něm hledá v druhém slovníku klíč se stejným identifikátorem, případně všechny objekty daného klíče propojuje s objektem v prvním klíči.

Následně předává podfunkci `__deleteUnreferenced()` slovník seznamů objektů StopTime indexovaný podle trip_id (`stopTimesTrip_id`). Výstup této funkce je výstupem funkce `referenceObjects()`.

4. `__deleteUnreferenced()`

|Název|deleteUnreferenced()|
|:---:|:---|
|Popis|Funkce vrací vstupní slovník obsahující pouze objekty StopTime, ze kterých se lze dostat do ostatních 3 objektů.|
|Argumenty|Slovník `stopTimesT`|
|Návratová hodnota|`stopTimesDict`|

Funkce iterováním skrz veškeré objekty každého klíče v něm kontroluje, zda:
- je v atributu `refToStop` objekt `Stop`
- je v atributu `refToTrip` objekt `Trip`
- je v atributu `refToTrip.refToRoute` objekt `Route`

Každý objekt, který nesplňuje všechny podmínky, je smazán, pokud pro daný klíč neexistuje objekt StopTime se správnými referencemi, po dokončení cyklu je klíč odstaněn z slovníku.

Výstup této funkce je i výstupem funkce `referenceObjects()`.

5. `createStopSegments()`

|Název|create_StopSegments()|
|:---:|:---|
|Popis|Funkce seřadí a poté vypíše 5 (popř. méně) nejfrekventovanějších mezizastávkových úseků|
|Argumenty|`stopTimeT` - slovník objektů StopSegment podle Tripu, pod každým klíčem (`trip_id`) je pole souvisejících objektů StopTimů|
|Návratová hodnota|`stopSegments` - slovník objektů třídy StopSegment, klíč je text (`stop_id` počáteční stanice a `stop_id` konečné stanice). Pod každým klíčem je objekt třídy stopSegment|

Funkce postupně prochází všechny objekty StopTime u příslušnými klíči. Z pole objektů StopTime, u každého `trip_id` (klíč slovníku) jsou vytvořeny StopSegmenty mezi objekty StopTime na pozicích 'i' a 'i+1'. Jako klíč se použito spojení `stop_id` počátečního a koncového bodu (`start_id` + `finish_id`), pokud StopSegment s takovýmto klíčem existuje, do atributu `counter` je přičtena jednička. Pokud neexistuje, je vytvořen nový objekt třídy stopSegment.  

6. `busiest()`

|Název|busiest()|
|:---:|:---|
|Popis|Funkce seřadí a poté vypíše 5 (popř. méně) nejfrekventovanějších mezizastávkových úseků|
|Argumenty|`stopSegments` - pole objektů třídy StopSegment|
|Návratová hodnota| None|

Funkce nejprve vytvoří z argument (slovník) pole s objekty třídy StopSegment, které potom seřadí pomocí funkce `merge_sort()`. Následně funkce vypíše prvních 5 StopSegmentů (popř. méně, pokud je méně StopSegmentů). U každého StopSegmentu funkce vytvoří pole, do kterého jsou přidány všechny související Tripy (názvy tripů). Následně je pole převedeno na set, která smaže duplicity. Poté set znovu převeden na pole a seřazen (abecedně). Výsledné seřazené pole se vypíše do tabulky.

7. `merge_sort()`

|Název|merge_sort()|
|:---:|:---|
|Popis|Funkce pomocí algoritmu merge sort seřadí pole objektů StopSegment|
|Argumenty|array - pole objektů třídy StopSegment, které mají být seřazeny|
|Návratová hodnota| seřazené pole objektů třídy StopSegment sestupně|

Funkce rekurzivně rozdělí pole na dílčí pole délky 1. Při návratu z rekurze se sousední pole sloučí podle velikosti. Každé dílčí pole má svou proměnnou (aktuální index), na začátku nastaveném na 0. Následně se porovnají objekty na danných pozicích. Větší StopSegment (větší číslo v položce StopSegment.counter) je zařazeno do již srovnaného pole. Pro pole, z které byl objekt vyjmut, byla proměnná zvětšena o jedničku. Algoritmus toto porovnání provádí dokud není jedno z polí prázdné, poté se zbytek druhého pole zařadí na konec seřazeného pole.

### Beh programu

Funkcie sú volané v `try` bloku, ktorý odchytáva prípadné chyby pri zápise
