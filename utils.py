from services import searchStock
from data.handler import load
from carteira import Profile, Stock

data = load('carteira.json')
profile = Profile(name="test", money=1250.50, assets=[{}], historical=[{}])
profile.save()



#Main system
def system_setup():
    selectmenu()

#Menu
def selectmenu():
    while True:
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
            s = 0
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

#Mostrar todos os dados recebidos do ativo
def printStock():
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
    print('\n\n')

