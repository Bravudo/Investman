import json
import os
from pathlib import Path

file_name = 'carteira.json'


def save(dados: dict, filename: str = file_name):
    path = os.path.join("data", filename)
    os.makedirs("data", exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)

def load(file_name: str) -> dict:
    path = os.path.join("data", file_name)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    

try:
    data = load('carteira.json')
    
except json.decoder.JSONDecodeError:

    #Iniciando o sistema pela primeira vez
    print('<💲 Bem vindo ao Investman 💲>')
    print('')
    name = input('Para começar, digite seu nome >> ')
    while True:
        try:
            money = float(input('Digite um saldo para sua conta >> $'))
            if money < 0:
                print('Erro: O saldo não pode ser negativo.')
                continue
            break
        except ValueError as e:
            print('Erro: Digite um valor numérico válido, tente novamente.') 

    data = {
        'name': name,
        'money': money,
        'assets': {},
        'historical':{}
             }
    save(data, 'carteira.json')  