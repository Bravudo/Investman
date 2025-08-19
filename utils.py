from services import searchStock
from data.handler import load
from carteira import Profile, Stock
from datetime import date
import os

data = load('carteira.json')
profile = Profile(name=data['name'], money=data['money'], assets=data['assets'], historical=data['historical'])
profile.save()




#Main system
def system_setup():
    selectmenu()

#Menu
def selectmenu():
    while True:
        clearTerminal()
        print('__I N V E S T M A N__')
        print('1 > Buscar Ativo')
        print('2 > Comprar Ativo')
        print('3 > Vender Ativo')
        print('4 > Ver Perfil')
        print('5 > Editar Perfil')
        print('6 > Sair')
        slct = int(input('>> '))

        if slct == 1:
            printStock()
        if slct == 2: 
            buyStock()
        if slct == 3:
            s = 0
        if slct == 4:
            s = 0
        if slct == 5: 
            s = 0
        if slct == 6: 
            break




#Texto de input padrão para receber o nome do ativo selecionado
def defaultinput():
    stockname = str(input('Código do ativo >> ').upper())
    return stockname

def leaveinput():
    input('Digite qualquer coisa para sair > ')

def errorfoundstock(e):
    if e:
        print(f'Erro: {e}')
    else:
        print('[!] Ação não encontrada!')

#Limpar o Chat do Terminal
def clearTerminal():
    try:
        os.system('cls')
    except:
        os.system('clear')

#Mostrar todos os dados recebidos do ativo
def printStock():
    clearTerminal()
    stockname = defaultinput()
    try:
        stock = searchStock(stockname)
        print()
        print(f'>>> {stock.symbol} <<<')
        print(f'- Preço: ${stock.price:.2f}')
        print(f'- Abriu em: ${stock.open:.2f}')
        print(f'- Lucro/Perda: {stock.performance:.2f}%')
        print(f'- Alta do mês: ${stock.high:.2f}')
        print(f'- Baixa do mês: ${stock.low:.2f}')
        print(f'- Fechou ontem em: ${stock.closeprice}')
        print(f'- Movimentações: {stock.volume}')
        print(f'- Data dos dados: {stock.date}')
        print('\n')
        leaveinput()
    except:
        errorfoundstock()
        leaveinput()


#Comprar uma ação
def buyStock():
    clearTerminal()
    stockname = defaultinput()
    try:
        stock = searchStock(stockname)
        
        clearTerminal()
        print(f'>>> {stock.symbol} <<<')
        print(f'- Preço: ${stock.price:.2f}')
        print(f'- Lucro/Perda: {stock.performance:.2f}%')
        print(f'> Seu saldo: ${profile.money:.2f}')

        qtd = float(input('\nQuantos ativos você quer comprar?\n>> '))
        totalprice = float(qtd * stock.price)

        if totalprice <= profile.money:
            print(f'\nTotal: ${totalprice:.2f} <-> Quantidade: {qtd}')
            slct = str(input('Confirme a compra (s/n) >> '))

            if slct == "s" or slct == "S":
                    #Verifica se esta na carteira
                    if stock.symbol in profile.assets:
                        profile.assets[stock.symbol]["amount"] += qtd
                        profile.assets[stock.symbol]["totalspent"] += totalprice

                    #Se não, cria um dicionario novo
                    else:
                        profile.assets[stock.symbol] = {
                            "price": stock.price,
                            "amount": qtd,
                            "totalspent": totalprice
                        }

                    clearTerminal()
                    profile.money -= totalprice

                    saveHistorical(stock, qtd, totalprice, "buy")


                    profile.save()
                    print(f'Saldo restante: ${profile.money:.2f}')
                    leaveinput()
                        
        else:
            clearTerminal()
            print(f'[!] Saldo Insuficiente para esta compra!')        
            leaveinput()      
    except Exception as e:
        errorfoundstock(e)
        leaveinput()


#Salvar dados da sua ação no histórico
def saveHistorical(stock, qtd, totalprice, action):
    #iso.format faz a data ficar em string pra verificação do action
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
    print('Histórico salvo!')




system_setup()
