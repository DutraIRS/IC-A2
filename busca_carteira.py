import requests
from bs4 import BeautifulSoup

def buscar_site(url):
    resposta = requests.get(url)
    site = BeautifulSoup(resposta.text, "lxml")

    return site

def encontrar_div_com_classe(conteudo, classe):
    return conteudo.find("div", class_ = classe)

def ler_table_data(conteudo):
    celulas = conteudo.find_all("td")
    dicionario = {}

    iterador = iter(celulas)
    for celula in iterador:
        dicionario[celula.string] = float(next(iterador).string)
    
    return dicionario