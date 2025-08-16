class Profile:
    def __init__(self, name:str, money:float, assets:dict,  historical: dict):
        self.name = name    
        self.money = money
        self.assets = assets
        self.historical = historical

class Stock:
    def __init__(self, symbol:str, openprice:float, high:float,low:float,price:float, volume:int,date:str, yesterdaycloseprice:float, performance:float ):
        self.symbol = symbol
        self.open = openprice
        self.high = high
        self.low = low
        self.price = price
        self.volume = volume
        self.date = date
        self.closeprice = yesterdaycloseprice
        self.performance = performance        