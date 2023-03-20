class Calendar_date:
    '''
    Class respesenting irregularity in schedule of trip
    ...
    
    Atributes:
    ---------
    calendar_id :
        reference to object of class Calendar on which irregularity refers
    date :
        object of clast Datetime.date when irregularity occurs 
    exception_type :
        1 - if trip goes
        2 - if trip does not go
    '''
    def __init__(self, calendar_id, date, exception) -> None:
        self.__calendar_id = calendar_id      # reference na objekt třídy Calendar
        self.__date = date                    # objekt třídy Datetime.date
        self.__exception_type = exception     # 1/2   jede/nejede
    
    @property
    def calendar_id(self) -> object:
        return self.__calendar_id
    
    @property
    def date(self) -> object:
        return self.__date
    
    @property
    def exception_type(self) -> int:
        return self.__exception_type