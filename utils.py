from services import searchActive


def system_setup():
    selectmenu()

def selectmenu():
    while True:
        print('1 > Buscar Ativo')
        print('2 > Comprar Ativo')
        print('3 > Vender Ativo')
        print('4 > Ver Perfil')
        print('5 > Sair')
        slct = int(input('>> '))

        if slct == 1:
            stockname = str(input('Código do ativo >> ').upper())
            stock = searchActive(stockname)
            print()
        if slct == 2: 
            s = 0
        if slct == 3:
            s = 0
        if slct == 4:
            s = 0
        if slct == 5: 
            break

selectmenu()