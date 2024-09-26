import datetime

class Brokerage:
    
    OPERATION_BUY = "buy"
    OPERATION_SELL = "sell"
    OPERATIONS = [
        OPERATION_BUY,
        OPERATION_SELL
    ]
    
    def __init__(
            self, 
            date: datetime.date|str|None = None, 
            stock_symbol: str|None = None, 
            quantity: int|None = None, 
            price: float|None = None,
            operation: str|None = None,
            fee: float|None = None, 
            ir: float|None = None, 
            broker: str|None = None,
            note_id: str|None = None
        ) -> None:
        if date:
            self.__setattr__("date", date)
        self._stock_symbol = stock_symbol or None
        self._quantity = quantity or None
        self._price = price or None
        self._operation = operation or None
        self._fee = fee or None
        self._ir = ir or None
        self._broker = broker or None
        self._note_id = note_id or None
        
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
    def stock_symbol(self) -> str|None:
        return self._stock_symbol
    
    @stock_symbol.setter
    def stock_symbol(self, stock_symbol) -> None:
        if not isinstance(stock_symbol, str):
            raise TypeError("Stock code must be a string")
        
        self._stock_symbol = stock_symbol
    
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
    def operation(self) -> str|None:
        return self._operation
    
    @operation.setter
    def operation(self, operation) -> None:
        if not operation in self.OPERATIONS:
            raise ValueError(f"Operation must be one of {self.OPERATIONS}")
        
        self._operation = operation
        
    @property
    def fee(self) -> float|None:
        return self._fee
    
    @fee.setter
    def fee(self, fee) -> None:
        if not isinstance(fee, float):
            raise TypeError("fee must be a float")
        
        self._fee = fee
        
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
        
    @property
    def note_id(self) -> str|None:
        return self._note_id
    
    @note_id.setter
    def note_id(self, note_id) -> None:
        if not isinstance(note_id, str):
            raise TypeError("Note ID must be a string")
        
        self._note_id = note_id
        
    def __json__(self):
        return {
            "date": self.date.isoformat() if self.date else None,
            "stock_symbol": self.stock_symbol,
            "quantity": self.quantity,
            "price": self.price,
            "operation": self.operation,
            "fee": self.fee,
            "ir": self.ir,
            "broker": self.broker,
            "note_id": self.note_id
        }
        
    def __str__(self) -> str:
        return f"Brokerage(date={self.date}, stock_symbol={self.stock_symbol}, quantity={self.quantity}, price={self.price}, operation={self.operation}, fee={self.fee}, ir={self.ir}, broker={self.broker}), note_id={self.note_id}"