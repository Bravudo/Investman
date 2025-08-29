import traceback
import os
from datetime import date
from datetime import datetime

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

        if action == "compra":
            profile.historical[today].append({
                "action": 'Compra',
                "symbol": stock.symbol,
                "amount": qtd,
                "price": stock.price,
                "total": totalprice
                })
        if action == "venda":
            profile.historical[today].append({
                "action": 'Venda',
                "symbol": stock.symbol,
                "amount": qtd,
                "price": stock.price,
                "total": totalprice
                })
        profile.save()

    except Exception as e:
        debugtracebackprint(e)

#Transformar data em formato brasileiro
def brazilian_data_format(data_str):
    try:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")
    except ValueError:
        return data_str 


#Botão de seleção
def selectNumber():
    try:
        while True:
            select = input('>> ')
            if select.isdigit():
                select = int(select)
                return select
            else:
                print('ERRO: Digite apenas números para seleção no menu.')
    except Exception as e:
        print(f'Erro Inesperado: {e}')
