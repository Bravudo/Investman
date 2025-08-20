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
            sellStock()
        if slct == 4:
            viewProfile()
        if slct == 5: 
            editProfile()
        if slct == 6: 
            break




#Texto de input padrão para receber o nome do ativo selecionado
def defaultinput():
    stockname = str(input('Código do ativo >> ').upper())
    return stockname

def leaveinput():
    input('\n>$> Digite qualquer coisa para sair >$> ')

def errorfoundstock(e):
    try:
        print(f'Erro: {e}')
    except Exception:
        print('[!] Ação não encontrada!')

#Limpar o Chat do Terminal
def clearTerminal():
    try:
        os.system('cls')
    except:
        os.system('clear')

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


#============================
#-------System Main Functions


#Mostrar todos os dados recebidos da ação
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
        leaveinput()
    except Exception as e:
        errorfoundstock(e)
        leaveinput()


#Comprar ações
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

                    print('Compra Realizada com Sucesso!')
                    print(f'Saldo restante: ${profile.money:.2f}')
                    leaveinput()
                        
        else:
            clearTerminal()
            print(f'[!] Saldo Insuficiente para esta compra!')        
            leaveinput()      
    except Exception as e:
        errorfoundstock(e)
        leaveinput()

#Vender Ações
def sellStock():
    clearTerminal()
    stockname = defaultinput()
    try:
        stock = searchStock(stockname)


        if stock.symbol in profile.assets:
            clearTerminal()
            print(f'>>> {stock.symbol} <<<')
            print(f'- Preço: ${stock.price:.2f}')
            print(f"- Quantidade: {profile.assets[stock.symbol]['amount']:.2f}")
            qtd = float(input('Quantos ativos você quer vender?\n>> '))

            clearTerminal()
            if qtd <= profile.assets[stock.symbol]['amount']:
                venda = stock.price * qtd
                profile.money += venda
                profile.assets[stock.symbol]['amount'] -= qtd
                saveHistorical(stock, qtd, venda, 'sell')
                profile.save()

                print(f'>>> {stock.symbol} <<<')
                print(f'- Quantidade Vendida:{qtd:.2f}')
                print(f'- Valor da Venda: + ${venda:.2f}')
                print(f'- Quantidade Restante: {profile.assets[stock.symbol]['amount']}')
                print(f'> Saldo: {profile.money:.2f}')

                    #Deleta ativo caso esteja zerado na carteira do perfil
                if profile.assets[stock.symbol]['amount'] <= 0:
                    del profile.assets[stock.symbol]
                    profile.save()
 
            else:
                print('Quantidade insuficiente para venda!')
        else:
            print('Você não possui este ativo para venda!')

        leaveinput()

    except Exception as e:
        print(f'[ERRO]: {e}')
        leaveinput()


#Visualizar Perfil
def viewProfile():
    clearTerminal()
    print(f'___{profile.name}___')
    print(f'- Saldo: {profile.money}')
    if profile.assets:
        print('> Ativos <')
        totalinvestido = 0
        for ticker, data in profile.assets.items():
            print(f'| {ticker} - Quantidade: {data['amount']} - Investido: ${data['totalspent']:.2f}')
            totalinvestido += data['totalspent']
        print(f'|> Total Investido: ${totalinvestido:.2f}')
        
    else:
        print(f'Ativos: Nenhum')
    leaveinput()

#Editar Perfil
def editProfile():
    while True:
        clearTerminal()
        print('__Editar Perfil__')
        print('1 > Nome')
        print('2 > Saldo')
        print('3 > Ativos')
        print('4 < Voltar')
        slct = int(input('>> '))

        if slct == 1:
            editProfileName()

        if slct == 2:
            print()
        if slct == 3:
            print()

        if slct == 4:
         return


#-----Profile Functions
def editProfileName():
    clearTerminal()
    print(f'Nome atual: {profile.name}')
    newname = input(f'Novo nome >> ')
    profile.name = newname
    profile.save()
    clearTerminal()

    print(f'Nome atualizado para > {profile.name}')
    leaveinput()
system_setup()
