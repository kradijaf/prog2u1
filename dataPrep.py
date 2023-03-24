try:
    from os.path import exists, isdir       # importing only the necesarry stuff
    from requests import get
    from zipfile import ZipFile

    if (not exists('gtfs')) or (not isdir('gtfs')):     # nothing in own folder is named 'gtfs' or it´s not a folder
        r = get('http://data.pid.cz/PID_GTFS.zip')      # accessing the data
        
        with open('PID_GTFS.zip', 'wb') as saveTo:      # saving the data
            saveTo.write(r.content)

        with ZipFile('PID_GTFS.zip', 'r') as myZip:     # access to ZIP file
            files = ('stops', 'stop_times', 'trips', 'routes', 'calendar', 'calendar_dates')
            for file in files:
                myZip.extract(f'{file}.txt', 'gtfs')        # extraction of the data into /gtfs
                
except ImportError as e:
    raise SystemExit(f'Couldn´t import module: {e.name}. Check if it´s installed.')
except PermissionError:
    raise SystemExit(r'Can´t write into this folder or into \gtfs.')
except OSError as e:
    raise SystemExit(f'OS Error: {e}.')
