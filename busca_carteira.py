import requests
from bs4 import BeautifulSoup


carteiras_salvas = {}


def buscar_site(url):
    """Retorna o site da url parseado usando BS4 e lxml

    :param url: URL do site
    :type url: str
    :return: Informações do site parseadas com BS4 e lxml
    :rtype: bs4.BeautifulSoup
    """
    resposta = requests.get(url)
    site = BeautifulSoup(resposta.text, "lxml")

    return site


def encontrar_div_com_classe(conteudo, classe):
    """Retorna o primeiro div com a classe especificada

    :param conteudo: De onde será obtido o div
    :type conteudo: bs4.BeautifulSoup
    :param classe: A classe que o div deve ter
    :type classe: str
    :return: O primeiro div encontrado que tenha a classe
    :rtype: bs4.element.Tag
    """
    return conteudo.find("div", class_=classe)


def ler_table_data(conteudo):
    """Retorna um dicionário com o conteúdo de todas tags 'td'

    As strings de todas as tags 'td' encontradas no parâmetro são agrupadas em
    pares chave-valor de um dicionário na ordem que forem encontradas. O
    parâmetro deve ter um número par de tags 'td' e cada segunda tag deve
    conter uma string que possa ser convertida em float.

    :param conteudo: Onde serão buscadas as tags 'td'
    :type conteudo: bs4.element.Tag
    :return: O dicionário com o conteúdo das tags 'td'
    :rtype: dict(str, float)
    """
    celulas = conteudo.find_all("td")
    dicionario = {}

    iterador = iter(celulas)
    for celula in iterador:
        dicionario[celula.string] = float(next(iterador).string)

    return dicionario


def ler_ativos(conteudo):
    """Retorna os ativos contidos no conteúdo recebido

    Retorna os ativos contidos no conteúdo em um dicionário de duas chaves. As
    moedas são armazenadas em um dicionário na chave 'moedas' e as ações são
    armazenadas em um dicionário na chave 'acoes'. Os ativos devem estar em
    pares de tags 'td' na ordem (nome, quantidade) que devem estar dentro de
    divs com a classe 'moeda' para as moedas e 'acao' para ações.

    :param conteudo: Onde serão buscados os ativos
    :type conteudo: bs4.BeautifulSoup
    :return: O dicionário com os ativos
    :rtype: dict(str, dict(str, float))
    """
    div_moedas = encontrar_div_com_classe(conteudo, "moeda")
    moedas_lidas = ler_table_data(div_moedas)

    # Trata as moedas para conterem apenas o código
    moedas = {}
    for moeda_lida, quantidade in moedas_lidas.items():
        if moeda_lida.endswith("BRL=X"):
            if moeda_lida == "BRL=X":
                # O código "BRL=X" retorna por padrão o valor do dólar em reais
                codigo_moeda = "USD"
                print(
                    "-> Atenção! \"BRL=X\" convertido para \"USD\" pelo padrão do YahooFinance")
            else:
                codigo_moeda = moeda_lida[0:3]
                print(
                    f"-> Atenção! \"{moeda_lida}\" convertido para \"{codigo_moeda}\"")

        else:
            codigo_moeda = moeda_lida

        moedas[codigo_moeda] = quantidade

    div_acoes = encontrar_div_com_classe(conteudo, "acao")
    acoes = ler_table_data(div_acoes)

    ativos = {"moedas": moedas, "acoes": acoes}

    return ativos


def buscar_carteira(url):
    """Busca a carteira na URL recebida

    Retorna os ativos contidos no site em um dicionário de duas chaves. As
    moedas são armazenadas em um dicionário na chave 'moedas' e as ações são
    armazenadas em um dicionário na chave 'acoes'.

    :param url: A URL onde se encontra a carteira
    :type url: str
    :return: Um dicionário com os ativos
    :rtype: dict(str, dict(str, float))
    """
    # Verifica se a carteira já foi buscada
    if url in carteiras_salvas:
        return carteiras_salvas[url]

    site = buscar_site(url)
    carteira = ler_ativos(site)

    # Salva carteira para possível uso futuro
    carteiras_salvas[url] = carteira

    return carteira
