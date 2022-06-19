import busca_carteira
import cotacoes as ctc
import matplotlib.pyplot as plt

def gerar_grafico_acoes(carteira, num):
    """Gera o gráfico das ações da carteira
    Obtem as moedas e ações de uma carteira a partir de seu link html e retorna
    o gráfico da variação ao longo do número especificado de dias.
        num: número de dias dejesado para fazer análise da carteira
        carteira: html da carteira
        :type num: int
        :type acao: str
        :return: Gráfico da variação das ações
    """
    #Usando o busca_carteira para obter as ações e moedas
    portifolio = busca_carteira.buscar_carteira(carteira)
    portifolio_list = list(portifolio.values())

    #Retirando as moedas e ações dos dicionários
    """Passando para listas separadas para poderem ser usadas
    nos comandos hist_moedas_real e hist_acoes"""
    portifolio_moedas = (portifolio_list[0])
    portifolio_acoes = (portifolio_list[1])

    lista_moedas = list(portifolio_moedas.keys())
    lista_acoes = list(portifolio_acoes.keys())

    #Gerando os datasets do histórico das ações e moedas
    histacoes = ctc.hist_acoes(lista_acoes, num)
    histacoes.reset_index(level = "date", inplace = True)
    histacoes.reset_index(level = "symbol", inplace = True)

    #gerando datasets individuais
    histacoes1 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[0]}'), ["date", "close"]]
    histacoes2 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[1]}'), ["date", "close"]]
    histacoes3 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[2]}'), ["date", "close"]]
    if len(lista_acoes) >= 4:
        histacoes4 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[3]}'), ["date", "close"]]
    else:
        histacoes4 = []
    if len(lista_acoes) >= 5:
        histacoes5 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[4]}'), ["date", "close"]]
    else:
        histacoes5 = []
    if len(lista_acoes) >= 6:
        histacoes6 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[5]}'), ["date", "close"]]
    else:
        histacoes6 = []
    if len(lista_acoes) >= 7:
        histacoes7 = histacoes.loc[(histacoes["symbol"] == f'{lista_acoes[6]}'), ["date", "close"]]
    else:
        histacoes7 = []

    #gerando o plot
    plt.plot(histacoes1.date, histacoes1.close, label = f'{lista_acoes[0]}')
    plt.plot(histacoes2.date, histacoes2.close, label = f'{lista_acoes[1]}')
    plt.plot(histacoes3.date, histacoes3.close, label = f'{lista_acoes[2]}')
    if len(lista_acoes) >= 4:
        plt.plot(histacoes4.date, histacoes4.close, label = f'{lista_acoes[3]}')
        
    if len(lista_acoes) >= 5:
        plt.plot(histacoes5.date, histacoes5.close, label = f'{lista_acoes[4]}')
        
    if len(lista_acoes) >= 6:
        plt.plot(histacoes6.date, histacoes6.close, label = f'{lista_acoes[5]}')
        
    if len(lista_acoes) >= 7:
        plt.plot(histacoes7.date, histacoes7.close, label = f'{lista_acoes[6]}')
        
    plt.legend()
    plt.title(f'Variação do preço das ações ao longo de {num} dias')
    plt.savefig('variacao_acoes.png')
    plot = plt.show()

    return plot

def gerar_grafico_moedas(carteira, num):
    """Gera o gráfico das moedas da carteira
    Obtem as moedas e ações de uma carteira a partir de seu link html e retorna
    o gráfico da variação ao longo do número especificado de dias.
        :param num: número de dias dejesado para fazer análise da carteira
        :param carteira: html da carteira
        :type num: int
        :type acao: str
        :return: Gráfico da variação das ações
    """
    #Usando o busca_carteira para obter as ações e moedas
    portifolio = busca_carteira.buscar_carteira(carteira)
    portifolio_list = list(portifolio.values())

    #Retirando as moedas e ações dos dicionários
    """Passando para listas separadas para poderem ser usadas
    nos comandos hist_moedas_real e hist_acoes"""
    portifolio_moedas = (portifolio_list[0])

    lista_moedas = list(portifolio_moedas.keys())
    #Gerando os datasets do histórico das ações e moedas
    histmoedas = ctc.hist_moedas_real(lista_moedas, num)
    histmoedas.reset_index(level = "date", inplace = True)
    histmoedas.reset_index(level = "symbol", inplace = True)

    #gerando datasets individuais
    histmoedas1 = histmoedas.loc[(histmoedas["symbol"] == f'{lista_moedas[0]}BRL=X'), ["date", "close"]]
    histmoedas2 = histmoedas.loc[(histmoedas["symbol"] == f'{lista_moedas[1]}BRL=X'), ["date", "close"]]
    histmoedas3 = histmoedas.loc[(histmoedas["symbol"] == f'{lista_moedas[2]}BRL=X'), ["date", "close"]]
    if len(lista_moedas) >= 4:
        histmoedas4 = histmoedas.loc[(histmoedas["symbol"] == f'{lista_moedas[3]}BRL=X'), ["date", "close"]]
    else:
        histmoedas4 = []
    if len(lista_moedas) >= 5:
        histmoedas5 = histmoedas.loc[(histmoedas["symbol"] == f'{lista_moedas[4]}BRL=X'), ["date", "close"]]
    else:
        histmoedas5 = []

    #gerando o plot
    plt.plot(histmoedas1.date, histmoedas1.close, label = f'{lista_moedas[0]}')
    plt.plot(histmoedas2.date, histmoedas2.close, label = f'{lista_moedas[1]}')
    plt.plot(histmoedas3.date, histmoedas3.close, label = f'{lista_moedas[2]}')
    if len(lista_moedas) >= 4:
        plt.plot(histmoedas4.date, histmoedas4.close, label = f'{lista_moedas[3]}')
        
    if len(lista_moedas) >= 5:
        plt.plot(histmoedas5.date, histmoedas5.close, label = f'{lista_moedas[4]}')
        
    plt.legend()
    plt.title(f'Variação do preço das moedas ao longo de {num} dias')
    plt.savefig('variacao_moedas.png')
    plot = plt.show()
    
    return plot

def gerar_grafico_carteira(carteira, num):
    #Usando o busca_carteira para obter as ações e moedas
    portifolio = busca_carteira.buscar_carteira(carteira)

    #Gerando dataset
    histcarteira = ctc.hist_carteira_total(portifolio, num)
    histcarteira.reset_index(level = "date", inplace = True)

    #Gerando o plot
    plt.plot(histcarteira.date, histcarteira.open, label = "Valor total da carteira em Reais")
    plt.legend()
    plt.title(f'Variação do valor total da carteira ao longo de {num} dias')
    plt.savefig('variacao_carteira.png')
    plot = plt.show()

    return plot

