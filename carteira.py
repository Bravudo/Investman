from data.handler import load, save, file_name

class Profile:
    def __init__(self, name:str, money:float, assets:dict,  historical: dict):
        self.name = name    
        self.money = money
        self.assets = assets
        self.historical = historical

    def for_dict(self) -> dict:
        return {
            "name": self.name,
            "money": self.money,
            "assets": self.assets,
            "historical": self.historical
        }
    
    def save(self, filename: str = file_name):
        save(self.for_dict(), filename)

    @classmethod
    def load(cls, filename: str = file_name):
        data = load(filename)
        return cls(
            name=data["name"], 
            money=data["money"],
            assets=data["assets"],
            historical=data["historical"]
        )
    


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