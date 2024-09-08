import datetime

class Brokerage:
    def __init__(
            self, 
            date: datetime.date|str|None = None, 
            stockCode: str|None = None, 
            quantity: int|None = None, 
            price: float|None = None, 
            fees: float|None = None, 
            ir: float|None = None, 
            broker: str|None = None
        ) -> None:
        if date:
            self.__setattr__("date", date)
        self._stockCode = stockCode or None
        self._quantity = quantity or None
        self._price = price or None
        self._fees = fees or None
        self._ir = ir or None
        self._broker = broker or None
        
    @property
    def date(self) -> datetime.date|None:
        return self._date
    
    @date.setter
    def date(self, date) -> None:
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        
        if not isinstance(date, datetime.date):
            raise TypeError("Date must be a datetime.date object")
        
        self._date = date
        
    @property
    def stockCode(self) -> str|None:
        return self._stockCode
    
    @stockCode.setter
    def stockCode(self, stockCode) -> None:
        if not isinstance(stockCode, str):
            raise TypeError("Stock code must be a string")
        
        self._stockCode = stockCode
    
    @property
    def quantity(self) -> int|None:
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity) -> None:
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")
        
        self._quantity = quantity
        
    @property
    def price(self) -> float|None:
        return self._price
    
    @price.setter
    def price(self, price) -> None:
        if not isinstance(price, float):
            raise TypeError("Price must be a float")
        
        self._price = price
        
    @property
    def fees(self) -> float|None:
        return self._fees
    
    @fees.setter
    def fees(self, fees) -> None:
        if not isinstance(fees, float):
            raise TypeError("Fees must be a float")
        
        self._fees = fees
        
    @property
    def ir(self) -> float|None:
        return self._ir
    
    @ir.setter
    def ir(self, ir) -> None:
        if not isinstance(ir, float):
            raise TypeError("IR must be a float")
        
        self._ir = ir
        
    @property
    def broker(self) -> str|None:
        return self._broker
    
    @broker.setter
    def broker(self, broker) -> None:
        if not isinstance(broker, str):
            raise TypeError("Broker must be a string")
        
        self._broker = broker
        
    def __json__(self):
        return {
            "date": self.date.isoformat() if self.date else None,
            "stockCode": self.stockCode,
            "quantity": self.quantity,
            "price": self.price,
            "fees": self.fees,
            "ir": self.ir,
            "broker": self.broker
        }
        
    def __str__(self) -> str:
        return f"Brokerage(date={self.date}, stockCode={self.stockCode}, quantity={self.quantity}, price={self.price}, fees={self.fees}, ir={self.ir}, broker={self.broker})"