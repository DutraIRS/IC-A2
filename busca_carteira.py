import requests
from bs4 import BeautifulSoup

def buscar_site(url):
    resposta = requests.get(url)
    site = BeautifulSoup(resposta.text, "lxml")

    return site