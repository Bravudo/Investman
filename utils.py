#==================================
#All Imports
from services import searchStock
from data.handler import load
from carteira import Profile, Stock
from datetime import date
import os
#===================================

#json data bd
data = load('carteira.json')
profile = Profile(name=data['name'], money=float(data['money']), assets=data['assets'], historical=data['historical'])
profile.save()


#Main Menu
def mainmenu():
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
            try:
                printStock()
            except Exception as e:
                print(f'Erro: {e}')
        if slct == 2: 
            try:
                buyStock()
            except Exception as e:
                print(f'Erro: {e}')
        if slct == 3:
            try:
                sellStock()
            except Exception as e:
                print(f'Erro: {e}')
        if slct == 4:
            try:
                viewProfile()
            except Exception as e:
                print(f'Erro: {e}')
        if slct == 5: 
            try:
                editProfile()
            except Exception as e:
                print(f'Erro: {e}')
        if slct == 6: 
            clearTerminal()
            break


#===============
#Generic systems
#===============

#Texto de input padrão para receber o nome do ativo selecionado
def defaultinput():
    stockname = str(input('Código do ativo >> ').upper())
    return stockname

#Texto de saída de input
def leaveinput():
    input('\n>$> Digite qualquer coisa para sair >$> ')

#Texto de Erro da busca por ativos
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

#=====================#
#System Main Functions#
#=====================#

#---------------------------
#Exibir dados salvos da ação
#---------------------------

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

#-------------
#Comprar ações
#-------------
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
#-------------
#Vender Ativos
#-------------
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

#-----------------
#Visualizar Perfil
#-----------------
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
        print(f'> Total Investido: ${totalinvestido:.2f}')
    else:
        print(f'Ativos: Nenhum')

    print('')
    print('1 - Calcular Lucro/Perda')
    print('2 - Voltar')
    slct = int(input('>> '))
        
    if slct == 1:
        clearTerminal()
        totalstockprice = 0
        totalstockqtd = 0
        totalprofilestockprice = 0
        totalprofilestockqtd = 0
        stocknametext = ''
        stockorder = False

        for ticker, ativo in profile.assets.items():
            stock = searchStock(ticker)

            ativo['price'] = stock.price
            
            #Ordenação de texto
            if stockorder == False:
                stocknametext += ticker
                stockorder = True
            else:
                stocknametext += ', ' + ticker

            #dados da busca
            totalstockprice += stock.price * ativo['amount']
            totalstockqtd += ativo['amount']

            #dados do perfil
            totalprofilestockprice += ativo['totalspent']
            totalprofilestockqtd += ativo['amount']

        media_compra = totalstockprice / totalstockqtd 
        media_atual = totalprofilestockprice / totalprofilestockqtd
        porcentagem = (((media_compra - media_atual) / media_atual)* 100)
        print(f'Utilizados: {stocknametext}.')
        print(f'Lucro/Perda: {porcentagem:.2f}%')
        profile.save()
        leaveinput()



    if slct == 2:
        return

#------------------------
#Menu de Edição de Perfil
#------------------------
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
            editProfileMoney()
        if slct == 3:
            editProfileStock()

        if slct == 4:
         return


#---------------------------
#Funções da edição de Perfil
#---------------------------

#Edição do nome do usuário
def editProfileName():
    while True:
        clearTerminal()
        print('__Nome__')
        print('1 - Novo Nome')
        print('2 - Voltar')
        slct = int(input('>> '))

        if slct == 1:
            clearTerminal()
            print(f'>> Nome atual: {profile.name}')
            newname = input(f'Novo nome >> ')
            if newname == '':
                print('Erro: Você não escreveu nada.')
            
            else:    
                profile.name = newname
                profile.save()

            clearTerminal()
            print(f'>> Nome atualizado para > {profile.name}')
            leaveinput()
        if slct == 2:
            return

#Edição do dinheiro do usuário
def editProfileMoney():
    while True:
        clearTerminal()
        print('__Saldo__')
        print('1 - Adicionar Saldo')
        print('2 - Remover Saldo')
        print('3 - Editar Saldo')
        print('4 - Voltar')
        slct = int(input('>> '))

        if slct == 1:
            clearTerminal()
            print(f'>> Saldo atual: ${profile.money:.2f}')
            newmoney = float(input(f'Adicionar saldo >> '))
            if newmoney < 0:
                print(' Saldo não adicionado.')
                print('<!>Você tentou adicionar menos que 0.')
            else:
                clearTerminal()
                profile.money += newmoney
                print(f'>> Saldo adicionado para > ${profile.money:.2f}')
                profile.save()
            leaveinput()

        if slct == 2:
            clearTerminal()
            print(f'>> Saldo atual: ${profile.money:.2f}')
            newmoney = float(input(f'Remover saldo >> '))

            if newmoney > profile.money:
                print('Saldo não removido.')
                print('<!> Você tentou remover mais do que você tinha!')
                leaveinput()
            else:
                profile.money -= newmoney
                profile.save()

                clearTerminal()
                print(f'>> Saldo restante > ${profile.money:.2f}')
                leaveinput()

        if slct == 3:
            clearTerminal()
            print(f'>> Saldo atual: ${profile.money:.2f}')
            newmoney = float(input(f'Novo saldo >> '))
            
            if newmoney < 0:
                print('Saldo não editado.')
                print('<!> Você tentou colocar um saldo negativo!')
                leaveinput()
            else:
                profile.money = newmoney
                profile.save()

                clearTerminal()
                print(f'>> Saldo atualizado para > ${profile.money:.2f}')
                leaveinput()

        if slct == 4:
            return
        

#Edição dos ativos do usuário
def editProfileStock():
     while True:
        clearTerminal()
        print('__Ativos__')
        #Exibição de ativos salvos
        if profile.assets:
            for ticker, dado in profile.assets.items():
                    print(f'> {ticker} < Quantidade: {dado['amount']} - Investido: {dado['totalspent']:.2f} ')

            print('1 - Voltar')
            slct = str(input('Digite o nome do ativo para edição >> ').upper())
            if slct == '1':
                return
 
            clearTerminal()
            if profile.assets[slct]:
                while True:
                    clearTerminal()
                    print(f'{slct} - Preço: ${profile.assets[slct]['price']} - Quantidade: {profile.assets[slct]['amount']} - Total: {float(profile.assets[slct]['totalspent']):.2f} ')
                    print(f'1 - Preço')
                    print(f'2 - Quantidade')
                    print(f'3 - Total Investido')
                    print(f'4 - Voltar')
                    slct2 = int(input('Qual informação editar? >> '))

                    clearTerminal()
                    if slct2 == 1:
                        print(f'>>> {slct} - Preço <<< ')
                        print(f'- Preço atual: ${profile.assets[slct]['price']}')
                        price = float(input('Novo Preço >> $'))

                        clearTerminal()
                        if price > 0:
                            profile.assets[slct]['price'] = price
                            print(f'{slct} > Novo Preço: ${price:.2f}')
                            profile.save()
                            leaveinput()

                        else:
                            print('O novo preço não pode ser 0 ou menor que isso!')
                            leaveinput()


                    if slct2 == 2:
                        print(f'>>> {slct} - Quantidade <<< ')
                        print(f'- Quantidade atual: {profile.assets[slct]['amount']}')
                        qtd = float(input('Nova Quantidade >> '))

                        clearTerminal()
                        #Deleta o ativo do perfil caso ele seja igual ou menor que 0
                        if qtd <= 0:
                            del profile.assets[slct]
                            leaveinput()

                        else:
                            profile.assets[slct]['amount'] = qtd
                            print(f'{slct} > Nova Quantidade: {qtd}')
                            leaveinput()

                        profile.save()
     

                    if slct2 == 3:
                        print(f'>>> {slct} - Total Investido <<< ')
                        print(f'- Total investido atual: ${profile.assets[slct]['totalspent']}')
                        total = float(input('Novo total >> $'))

                        clearTerminal()
                        if total <= 0:
                            print('Você não pode ter um total investido menor que 0!')
                            leaveinput()

                        else:
                            profile.assets[slct]['totalspent'] = total
                            print(f'{slct} > Novo total: ${total}')
                            profile.save()
                            leaveinput()

                       
                    if slct2 == 4:
                        return
            else: 
                print('Nenhum ativo registrado com este nome.')
                leaveinput()
        else:
            print('Sem ativos registrados.')

        if slct == 0:
            return