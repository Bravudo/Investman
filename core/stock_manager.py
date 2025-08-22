from core.utils import clearTerminal, defaultinput, leaveinput, debugtracebackprint, saveHistorical
from services.services import searchStock

#---------------------------
#Exibir dados salvos da ação
#---------------------------

def printStock():
    clearTerminal()
    try:
        stockname = defaultinput()
        stock = searchStock(stockname)
        print()
        print(f'>>> {stock.symbol} <<<')
        print(f'- Preço: ${stock.price:.2f}')
        print(f'- Abriu em: ${stock.open:.2f}')
        print(f'- Lucro/Perda: {stock.performance:.2f}%')
        print(f'- Alta do dia: ${stock.high:.2f}')
        print(f'- Baixa do mês: ${stock.low:.2f}')
        print(f'- Fechou ontem em: ${stock.closeprice}')
        print(f'- Movimentações: {stock.volume}')
        print(f'- Data dos dados: {stock.date}')
        leaveinput()

    except Exception as e:
        debugtracebackprint(e)


#-------------
#Comprar ações
#-------------
def buyStock(profile):
    try:
        clearTerminal()
        stockname = defaultinput()
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
                    saveHistorical(profile, stock, qtd, totalprice, "buy")
                    profile.save()

                    print('Compra Realizada com Sucesso!')
                    print(f'Saldo restante: ${profile.money:.2f}')
                    leaveinput()
                        
        else:
            clearTerminal()
            print(f'[!] Saldo Insuficiente para esta compra!')        
            leaveinput()      
    except Exception as e:
        debugtracebackprint(e)

#-------------
#Vender Ativos
#-------------
def sellStock(profile):
    try:
        clearTerminal()
        stockname = defaultinput()
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
                saveHistorical(profile, stock, qtd, venda, 'sell')
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
        debugtracebackprint(e)