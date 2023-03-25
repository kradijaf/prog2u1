# Uživatelská dokumentace
Program na začátku načtene soubory 'stops.txt', 'trips.txt', 'routes.txt' a 'stop_times.txt'<br/>
ze složky "gtfs", která se nachází v pracovním adresáři.<br/>
Pokud není složka gtfs dostupná, program soubory stáhne z adresy "http://data.pid.cz/PID_GTFS.zip"<br/>

## Vstupní soubory
### stops.txt
V prvním řádku se nachází jména sloupců.<br/>
>> "stop_id,stop_name,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,wheelchair_boarding,level_id,platform_code,asw_node_id,asw_stop_id"<br/>
Názvy sloupců musí odpovídat vzoru, jelikož jsou použity při dalším zpracování dat.<br/>
Každý řádek poté popisuje jednu zastávku. Např. Nemocnice Motol<br/> 
Při dalších výpočtech jsou použité tyto sloupce:
>> stop_id - jedineční identifikátor zastávky
>> stop_name - jměno zastávky
Př. "U1Z1P,"Boletická",50.132732,14.513702,"P",,0,,0,,A,1,1"<br/>

### routes.txt
V prvním řádku se nachází jména sloupců.<br/>
>> "route_id,agency_id,route_short_name,route_long_name,route_type,route_url,route_color,route_text_color,is_night,is_regional,is_substitute_transport"<br/>
Názvy sloupců musí odpovídat vzoru, jelikož jsou použity při dalším zpracování dat.<br/>
Každý řádek poté popisuje jednu linku tramvaje/autobusu. Např. Linka A<br/> 
Při dalších výpočtech jsou použité tyto sloupce:
>> route_id - jedinečný identifikátor linky
>> route_short_name - Zkrácený název linky
>> route_long_name - celý název linky
Př. "L991,1111100-1,991_4357_230213,"Nemocnice Motol",,0,,L991V1,1,1,0,1"<br/>

### trips.txt
V prvním řádku se nachází jména sloupců.<br/>
>> "route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id,wheelchair_accessible,bikes_allowed,exceptional,sub_agency_id"<br/>
Názvy sloupců musí odpovídat vzoru, jelikož jsou použity při dalším zpracování dat.<br/>
Každý řádek poté popisuje jednu realizaci linky, jednu jízdu tramvaje/autobusu. Např. Jízda určité soupravy metra<br/> 
Při dalších výpočtech jsou použité tyto sloupce:
>> route_id - jedinečný identifikátor linky, ke které patří
>> trip_id - jedinečný identifikátor každé jízdy
>> trip_headsign - název konečné zastávky linky
>> trip_short_name - název počáteční stanice jízdy
>> stop_name - jměno zastávky
Př. "L991,1111100-1,991_4357_230213,"Nemocnice Motol",,0,,L991V1,1,1,0,1"<br/>

### stop_times.txt
V prvním řádku se nachází jména sloupců.<br/>
>> "trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled,trip_operation_type,bikes_allowed"<br/>
Názvy sloupců musí odpovídat vzoru, jelikož jsou použity při dalším zpracování dat.<br/>
Každý řádek poté popisuje jedno zastavení jedné tramvaje/autobusu v jedné stanici. Např. přítonost metra ve stanici Nemocnice Motol v 12:54<br/> 
Při dalších výpočtech jsou použité tyto sloupce:
>> trip_id - jedinečný identifikátor jízdy, ke které patří
>> arrival_time - čas příjezdu jízdy ve formátu "00:00:00"
>> departure_time - čas odjezdu jízdy ve formátu "00:00:00"
>> stop_id - jedinečný identifikátor zastávky
Př. "991_4357_230213,7:25:00,7:25:30,U713Z102P,2,,0,0,1.389436,1,1"<br/>

## Výstup
Program poté vypíše do terminálu 5 nejfrekventovanějších mezizastávkových úseků, počet souvisejících jízd autobusus/tramvaje a počet souvisejících linek<br/>
![Vzor](https://user-images.githubusercontent.com/116712623/227737937-48ec2089-bddc-4c39-aa19-fd0690116ba5.png)
