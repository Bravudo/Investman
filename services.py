import requests
from dotenv import load_dotenv
import os
from carteira import Stock


#Alpha Vantage API
load_dotenv()
alphaapikey = os.getenv("")

def searchActive(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={alphaapikey}"  
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "Global Quote" in data and data["Global Quote"]:

                quote = data["Global Quote"]
                stock = Stock(
                    symbol = ticker,
                    openprice = quote['02. open'],
                    high = quote["03. high"],
                    low = quote["04. low"],
                    price = quote["05. price"],
                    volume = quote["06. volume"],
                    date = quote["07. latest trading day"],
                    yesterdaycloseprice = quote['08. previous close'],
                    performance = quote["10. change percent"]
                 )
                return stock

        else:
            print('Erro na busca pela ação')
    except requests.RequestException as e:
        print(f'API -  Falha na conexão: {e}')
    except KeyError as e:
        print(f'ERRO - Ativo {e} não encontrado.')
    except Exception as e:
        print(f'ERRO: {e}')
        