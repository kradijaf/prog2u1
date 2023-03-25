# Třída StopSegment
__Popis__<br/>
Třída simuluje mezizastávkový úsek, úsek mezi dvěma po sobě následujícími zastávkami<br/>
__Datové položky:__
>>start - název počáteční stanice<br/>
>>finish - název konečné stanice<br/>
>>counter - počet souvisejících tříd třídy Trip<br/>
>>trips - souvisejících tříd třídy Trip<br/>

__Metody__
>>\__add_trip(trip):<br/>
>>>> přidání objektu třídy Trip do pole trips<br/>


# Ostatní moje funkce v main.py
|Název|merge_sort()|
|:---:|:---|
|Popis|Funkce pomocí algoritmu merge sort seřadí pole objektů StopSegment|
|Argumenty|array - pole objektů třídy StopSegment, které mají být seřazeny|
|Návratová hodnota| seřazené pole objektů třídy StopSegment sestupně|

|Název|busiest()|
|:---:|:---|
|Popis|Funkce seřadí a poté vypíše 5 (popř. méně) nejfrekventovanějších mezizastávkových úseků|
|Argumenty|stopSegments - pole objektů třídy StopSegment|
|Návratová hodnota| None|

## create_StopSegments(stopTimesT)
|Název|create_StopSegments()|
|:---:|:---|
|Popis|Funkce seřadí a poté vypíše 5 (popř. méně) nejfrekventovanějších mezizastávkových úseků|
|Argumenty|stopTimeT - slovník objektů StopSegment podle Tripu, pod každým klíčem (trip_id) je pole souvisejících objektů StopTimů|
|Návratová hodnota|stopSegmets - slovník objektů třídy StopSegment (klíč je text (stop_id počáteční stanice a stop_id konečné stanice ), pod každým klíčem je objekt třídy stopSegment|

# Jak ty funkce fungujou
## merge_sort()
Funkce rekurzivně rozdělí pole na dílčí pole délky 1, nebo 2. Při návratu z rekurze se sousední pole sloučí podle velikosti.
### Slučování
každé dílčí pole má svou proměnnou (aktuální index), na začátku nastaveném na 0. Následně se porovnají objekty na danných pozicích. Větší číslo (větší číslo v položce StopSegment.counter) je zařazeno do již srovnaného pole. Pro pole, z které byl objekt vyjmut, byla proměnná zvětšena o jedničku. Algoritmus toto porovnání provádí dokud není jedno z polí prázdné, poté se zbytek druhého pole zařadí na konec seřazeného pole.

## busiest()
Funkce nejprve vytvoří z argument (slovník) pole s objekty třídy StopSegment, které potom seřadí pomocí funkce merge_sort(). Následně funkce vypíše prvních 5 StopSegmentů (popř. méně, pokud je méně StopSegmentů). U každého StopSegmentu funkce vytvoří pole, do kterého jsou přidány všechny související Tripy (názvy tripů). Následně je pole převedeno na set, která smaže duplicity. Poté set znovu převeden na pole a seřazen (abecedně). Výsledné seřazené pole se vypíše do tabulky.

## create_StopSegments()
Funkce postupně prochází všechny objekty StopTime u příslušnýma klíčema. Z pole objektů StopTime, u každého Trip_id (klíč slovníku) jsou vytvořeny StopSegmenty mezi objekty StopTime na pozicích 'i' a 'i+1'. Jako klíč se použito spojení stop_id počátečního a koncového bodu (start_id + finish_id), pokud StopSegment s takovýmto klíčem existuje, do atributu counter je přičtena jednička. Pokud neexistuje, je vytvořen nový stopSegment.   
