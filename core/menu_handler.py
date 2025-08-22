#------------
# All imports
from core.stock_manager import printStock, buyStock, sellStock
from core.profile_manager import viewProfile, editProfile
from core.utils import clearTerminal
#------------


#----------------
#Main Menu System
#-----------------
def mainmenu(profile):
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
                buyStock(profile)
        if slct == 3:
                sellStock(profile)
        if slct == 4:
                viewProfile(profile)
        if slct == 5: 
                editProfile(profile)
        if slct == 6: 
                clearTerminal()
                break

