#-------------------------------------
#All Imports
from core.menu_handler import mainmenu
from data.handler import load, save
from carteira import Stock, Profile
from core.menu_handler import mainmenu
from data.handler import load
from carteira import Profile
#-------------------------------------

#json data
try:
    data = load('carteira.json')
    profile = Profile(name=data['name'], money=float(data['money']), assets=data['assets'], historical=data['historical'])
    profile.save()
except Exception as e:
    print(f'Erro ao buscar dados de perfil: {e}') 

#Start System
def system_setup():
    try: 
        mainmenu(profile)
    except Exception as e:
        print(f'Erro: {e}')

system_setup()