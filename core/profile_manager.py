from core.utils import clearTerminal, leaveinput, debugtracebackprint, brazilian_data_format, selectNumber
from services.services import searchStock


#-----------------
#Visualizar Perfil
#-----------------
def viewProfile(profile):
    try:
        if profile:
            clearTerminal()
            print(f'___{profile.name}___')
            print(f'- Saldo: ${profile.money}')
            if profile.assets:
                print('> Ativos <')  
                totalinvestido = 0
                for ticker, data in profile.assets.items():
                    print(f'| {ticker} - Quantidade: {data['amount']:.5f} - Investido: ${data['totalspent']:.2f}')
                    totalinvestido += data['totalspent']
                print(f'> Total Investido: ${totalinvestido:.2f}')
            else:
                print(f'Ativos: Nenhum')

            print('')
            print('1 - Calcular Lucro/Perda')
            print('2 - Histórico de atividades')
            print('3 - Voltar')
            slct = selectNumber()
                
            if slct == 1:
                profit_loss(profile)
            if slct == 2:
                historicalProfile(profile)
            if slct == 3:
                return
            
        if not profile.name or not profile.money or not profile.assets or not profile.historical:
            print('Erro: Dados Faltando em Perfil.')

    
    except KeyError as e:
        print(f'Erro: Campo "{e.args[0]}" não encontrado.')
    except TypeError as e:
        print(f'Erro: cálculo indevido entre números e letras: {e}')
    except Exception as e:
        debugtracebackprint(e)

def profit_loss(profile):
    clearTerminal()
    totalstockprice = 0
    totalstockqtd = 0
    totalprofilestockprice = 0
    totalprofilestockqtd = 0
    stocknametext = ''
    stockorder = False
                
    try:
        for ticker, ativo in profile.assets.items():
            stock = searchStock(ticker)
            if ativo['price']:
                ativo['price'] = stock.price
            else:
                print('Dados Faltantes: Preço do ativo')
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

    except ZeroDivisionError:
                    print('<!> Você não possui nenhum ativo para calcular.')
    except Exception as e:
                    print(f'Erro: {e}')
    leaveinput()



#------------------------
# Historico de atividades
#------------------------


def historicalProfile(profile):
    clearTerminal()
    for date, data in profile.historical.items():
        date = brazilian_data_format(date)
        print(f'\n>> 📅 {date}')
        for op in data:
                print(f"{op['symbol']} > Ação: {op['action']} - Quantidade: {op['amount']:.4f} - Preço: ${op['price']:.2f} - Total: ${op['total']:.2f}")
    leaveinput()


#------------------------
#Menu de Edição de Perfil
#------------------------
def editProfile(profile):
    try:
        while True:
            clearTerminal()
            print('__Editar Perfil__')
            print('1 > Nome')
            print('2 > Saldo')
            print('3 > Ativos')
            print('4 < Voltar')
            slct = selectNumber()

            if slct == 1:
                editProfileName(profile)
            if slct == 2:
                editProfileMoney(profile)
            if slct == 3:
                editProfileStock(profile)

            if slct == 4:
                return
    except Exception as e:
        debugtracebackprint(e)



#---------------------------
#Funções da edição de Perfil
#---------------------------

#Edição do nome do usuário
def editProfileName(profile):
    try:
        while True:
            clearTerminal()
            print('__Nome__')
            print('1 - Novo Nome')
            print('2 - Voltar')
            slct = selectNumber()

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
    except Exception as e:
            debugtracebackprint(e)


#-----------------------------
#Edição do dinheiro do usuário
#-----------------------------
def editProfileMoney(profile):
    try:
        while True:
            clearTerminal()
            print('__Saldo__')
            print('1 - Adicionar Saldo')
            print('2 - Remover Saldo')
            print('3 - Editar Saldo')
            print('4 - Voltar')
            slct = selectNumber()

            if slct == 1:
              editProfileMoneyAdd(profile)
            if slct == 2:
                editProfileMoneyRemove(profile)
            if slct == 3:
                editProfileMoneyEdit(profile)
            if slct == 4:
                return
    except Exception as e:
        debugtracebackprint(e)


def editProfileMoneyAdd(profile):
    clearTerminal()
    print(f'>> Saldo atual: ${profile.money:.2f}')
    newmoney = float(input(f'Adicionar saldo >> '))
    if newmoney < 0:
         print(' Saldo não adicionado.')
         print('<!>Você tentou adicionar menos que 0.')
         leaveinput()
    else:
        clearTerminal()
        profile.money += newmoney
        print(f'>> Saldo adicionado para > ${profile.money:.2f}')
        profile.save()
        leaveinput()

def editProfileMoneyRemove(profile):
    clearTerminal()
    print(f'>> Saldo atual: ${profile.money:.2f}')
    newmoney = float(input(f'Remover saldo >> '))

    if newmoney > profile.money:
        print('Saldo não removido.')
        print('<!> Você tentou remover mais do que você tinha!')
    else:
        profile.money -= newmoney
        profile.save()
        clearTerminal()
        print(f'>> Saldo restante > ${profile.money:.2f}')
    leaveinput()

def editProfileMoneyEdit(profile):
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
        
#----------------------------
#Edição dos ativos do usuário
#----------------------------
def editProfileStock(profile):
     try:
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
    
                if profile.assets[slct]:
                    while True:
                        slct2 = editStockMenu(profile, slct)
                        if slct2 == 1:
                            editStockPrice(profile,slct)
                        if slct2 == 2:
                            editStockAmount(profile,slct)
                        if slct2 == 3:
                            editStockTotalSpent(profile,slct)
                        if slct2 == 4:
                            return
                else: 
                    print('Nenhum ativo registrado com este nome.')
                    leaveinput()
            else:
                print('Sem ativos registrados.')
            if slct == 0:
                return
     except KeyError as e:
         print('Erro: Dado Inválido')
         leaveinput()
     except Exception as e:
        debugtracebackprint(e)


#Menu da edição de ativos
def editStockMenu(profile, slct):
    clearTerminal()
    print(f'{slct} - Preço: ${profile.assets[slct]['price']} - Quantidade: {profile.assets[slct]['amount']} - Total: {float(profile.assets[slct]['totalspent']):.2f} ')
    print(f'1 - Preço')
    print(f'2 - Quantidade')
    print(f'3 - Total Investido')
    print(f'4 - Voltar')
    return int(input('Qual informação editar? >> '))

#Edição do preço dos ativos
def editStockPrice(profile, slct):
    clearTerminal()
    print(f'>>> {slct} - Preço <<< ')
    print(f'- Preço atual: ${profile.assets[slct]['price']}')
    price = float(input('Novo Preço >> $'))

    clearTerminal()
    if price > 0:
        profile.assets[slct]['price'] = price
        print(f'{slct} > Novo Preço: ${price:.2f}')
        profile.save()
    else:
        print('O novo preço não pode ser 0 ou menor que isso!')
    leaveinput()

#Edição da quantidade de ativos
def editStockAmount(profile, slct):
    print(f'>>> {slct} - Quantidade <<< ')
    print(f'- Quantidade atual: {profile.assets[slct]['amount']}')
    qtd = float(input('Nova Quantidade >> '))
    clearTerminal()

    #Deleta o ativo do perfil caso ele seja igual ou menor que 0
    if qtd <= 0:
        del profile.assets[slct]

    else:
        profile.assets[slct]['amount'] = qtd
        print(f'{slct} > Nova Quantidade: {qtd}')
        profile.save()
    leaveinput()

#Edição do total investido dos ativos
def editStockTotalSpent(profile, slct):
    print(f'>>> {slct} - Total Investido <<< ')
    print(f'- Total investido atual: ${profile.assets[slct]['totalspent']}')
    total = float(input('Novo total >> $'))

    clearTerminal()
    if total <= 0:
        print('Você não pode ter um total investido menor que 0!')
    else:
        profile.assets[slct]['totalspent'] = total
        print(f'{slct} > Novo total: ${total}')
        profile.save()
    leaveinput()