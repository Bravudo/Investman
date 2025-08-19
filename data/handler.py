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
    print('<-=-> Bem vindo ao Invest-man <-=->')
    print('\n')
    name = input('Para começar, digite seu nome >> ')
    money = float(input('Digite a quantidade de dinheiro para sua conta >> '))
    
    data = {
        'name': name,
        'money': money,
        'assets': {},
        'historical':{}
             }
    save(data, 'carteira.json')  