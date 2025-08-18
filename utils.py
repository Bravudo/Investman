from services import searchStock
from data.handler import load
from carteira import Profile, Stock
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
    stock = searchStock(stockname)

    print()
    print(f'>>> {stock.symbol} <<<')
    print(f'- Preço: ${stock.price:.2f}')
    print(f'- Abriu em: ${stock.open:.2f}')
    print(f'- Lucro/Perda: {stock.performance}%')
    print(f'- Alta do mês: ${stock.high:.2f}')
    print(f'- Baixa do mês: ${stock.low:.2f}')
    print(f'- Fechou ontem em: ${stock.closeprice}')
    print(f'- Movimentações: {stock.volume}')
    print(f'- Data dos dados: {stock.date}')
    print('\n')
    leaveinput()

#Comprar uma ação
def buyStock():
    clearTerminal()
    stockname = defaultinput()
    stock = searchStock(stockname)
    print(f'>>> {stock.symbol} <<<')
    print(f'- Preço: ${stock.price:.2f}')
    print(f'- Lucro/Perda: {stock.performance}%')

    qtd = float(input('\nQuantos ativos você quer comprar?\n>> '))
    totalprice = float(qtd * stock.price)

    if totalprice <= profile.money:
        print(f'Total: ${totalprice:.2f} <-> Quantidade: {qtd}')
        slct = str(input('Confirme a compra (s/n) >> '))
        if slct == "s":
            for ativo in profile.assets:
                if stock.symbol in profile.assets:
                    print(f'Você já tinha {stock.symbol} na carteira')
                    leaveinput()
                else:
                    print('Você ainda não tinha')
                    leaveinput()
                    
    else:
        print(f'Saldo Insuficiente para esta compra!')        
        leaveinput()      

    print()

system_setup()
