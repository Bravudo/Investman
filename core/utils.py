import traceback
import os
from datetime import date

#===============
#Generic systems
#===============

#Texto de input padrão para receber o nome do ativo selecionado
def defaultinput():
    return input('Código do ativo >> ').upper()

#Texto de saída de input
def leaveinput():
    input('\n>$> Digite qualquer coisa para sair >$> ')

#Texto de Erro da busca por ativos
def errorfoundstock(e):
    try:
        print(f'Erro: {e}')
    except Exception:
        print('[!] Ação não encontrada!')

def debugtracebackprint(e):
    print(f'ERRO: {type(e).__name__}: {e}')
    print('__Traceback__')
    traceback.print_exc()
    input('>> ')

#Limpar o Chat do Terminal
def clearTerminal():
    try:
        os.system('cls')
    except:
        os.system('clear')

#Salvar dados da sua ação no histórico
def saveHistorical(profile, stock, qtd, totalprice, action):
    #iso.format faz a data ficar em string pra verificação do action
    try:
        today = date.today().isoformat()

        if today not in profile.historical:
            profile.historical[today] = []

        if action == "buy":
            profile.historical[today].append({
                "action": 'buy',
                "symbol": stock.symbol,
                "amount": qtd,
                "price": stock.price,
                "total": totalprice
                })
        if action == "sell":
            profile.historical[today].append({
                "action": 'sell',
                "symbol": stock.symbol,
                "amount": qtd,
                "price": stock.price,
                "total": totalprice
                })
        profile.save()

    except Exception as e:
        debugtracebackprint(e)
