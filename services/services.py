from models import Stock
from dotenv import load_dotenv
import requests
import os

#Alpha Vantage API
load_dotenv()
alphaapikey = os.getenv("alpha_vantage_api_key")

def searchStock(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={alphaapikey}"  
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                return Stock(
                    symbol = ticker,
                    openprice = float(quote.get('02. open', 0)),
                    high = float(quote.get("03. high", 0)),
                    low = float(quote.get("04. low", 0)),
                    price = float(quote.get("05. price", 0)),
                    volume = int(quote.get("06. volume", 0)),
                    date = str(quote.get("07. latest trading day", "")),
                    yesterdaycloseprice = float(quote.get('08. previous close', 0)),
                    performance = float(quote.get("10. change percent", "0%").replace('%',''))
                )

        print(f'[!] Não foi possível obter dados para {ticker}')
        return None  

    except requests.RequestException as e:
        print(f'API -  Falha na conexão: {e}')
        return None
    except KeyError as e:
        print(f'ERRO - Campo {e} não encontrado na resposta da API.')
        return None
    except Exception as e:
        print(f'ERRO: {e}')
        return None
        