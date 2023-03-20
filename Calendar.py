class Calendar:
    '''
    Class respesenting schedule of trip
    ...
    Atributes:
    ---------
    service_id :
        reference to object of class Trip on which schedule refers
    days :
        7-elements array, each item for every day
        0 - trip does not on these day
        1 - trip goes on these day
    start_date :
        reference to object of class datetime.date on which schedule starts
    end_date :
        reference to object of class datetime.date on which schedule ends
    exceptions :
        array of references to objects of class Calendar_date which stores irregularities of schedule
    '''
    def ___init__(self, service_id, array, start_date, end_date, exceptions) -> None:
        self.__service_id = service_id        # reference na trip
        self.__days = array                   # 7prvkové pole, pro každý den 1/0 jede/nejede
        self.__start_date = start_date        # objekt třídy datetime.date
        self.__end_date = end_date            # objekt třídy datetime.date
        self.__exceptions = exceptions        # pole objektů typu Calendar_date

    @property
    def service_id(self) -> object:
        return self.__service_id
        
    @property
    def days(self) -> object:
        return self.__days

    @property
    def start_date(self) -> object:
        return self.__start_date
    
    @property
    def end_date(self) -> object:
        return self.__end_date
    
    @property
    def exceptions(self) -> object:
        return self.__exceptions