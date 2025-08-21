from utils import mainmenu


def system_setup():
    try: 
        mainmenu()


    except Exception as e:
        print(f'Erro: {e}')


system_setup()