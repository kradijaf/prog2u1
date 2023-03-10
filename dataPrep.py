from os.path import exists, isdir       # import pouze potřebného
from requests import get
from zipfile import ZipFile

if (not exists('gtfs')) or (not isdir('gtfs')):     # ve složce není nic s názvem 'PID_GTFS' nebo to není složka
    r = get('http://data.pid.cz/PID_GTFS.zip')      # získání dat
    
    with open('PID_GTFS.zip', 'wb') as saveTo:      # uložení dat
        saveTo.write(r.content)

    with ZipFile('PID_GTFS.zip', 'r') as myZip:     # přístup k ZIP souboru
        files = ('stops', 'stop_times', 'trips', 'routes', 'calendar', 'calendar_dates')
        for file in files:
            myZip.extract(f'{file}.txt', 'gtfs')        # extrakce dat do /gtfs