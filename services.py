from carteira import Stock
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
   
                stock = Stock(
                    symbol = ticker,
                    openprice = float(quote['02. open']),
                    high = float(quote["03. high"]),
                    low = float(quote["04. low"]),
                    price = float(quote["05. price"]),
                    volume = int(quote["06. volume"]),
                    date = str(quote["07. latest trading day"]),
                    yesterdaycloseprice = float(quote['08. previous close']),
                    performance = float(quote["10. change percent"].replace('%',''))
                 )
                return stock

        else:
            print('[!] Erro na busca pela ação!')

    except requests.RequestException as e:
        print(f'API -  Falha na conexão: {e}')
    except KeyError as e:
        print(f'ERRO - Ativo {e} não encontrado.')
    except Exception as e:
        print(f'ERRO: {e}')
        