import yfinance as yf

def obtem_cotacao(acao, dias):
    ticker = yf.Ticker(acao)
    texto_historico = f"{dias}d"

    cotacao = ticker.history(texto_historico)
    return cotacao

def moeda_em_real(moeda):
    texto_conversao = f"{moeda}BRL=X"
    ticker = yf.Ticker(texto_conversao)

    moeda_em_real = ticker.info["regularMarketPrice"]
    return moeda_em_real

def obtem_cotacoes(acoes, dias):
    texto_acoes = ' '.join(acoes)
    tickers_acoes = yf.Tickers(texto_acoes)

    dicionario_cotacoes = dict(tickers_acoes.tickers)
    texto_historico = f"{dias}d"
    for acao in dicionario_cotacoes.keys():
        cotacao = dicionario_cotacoes[acao].history(texto_historico)
        dicionario_cotacoes[acao] = cotacao
    
    return dicionario_cotacoes

def moedas_em_real(moedas):
    textos_moedas = []
    for moeda in moedas:
        texto_conversao = f"{moeda}BRL=X"
        textos_moedas.append(texto_conversao)
    
    texto_conversoes = ' '.join(textos_moedas)
    tickers_moedas = yf.Tickers(texto_conversoes)
    dicionario_cotacoes = dict(tickers_moedas.tickers)

    dicionario_valor_real = {}
    for texto_conversao in dicionario_cotacoes.keys():
        ticker = dicionario_cotacoes[texto_conversao]
        moeda_em_real = ticker.info["regularMarketPrice"]

        moeda = texto_conversao[:-5]
        dicionario_valor_real[moeda] = moeda_em_real
    
    return dicionario_valor_real

def multiplica_cotacao(cotacao, razao):
    """
    Multiplica uma cotação por um valor

    Multiplica os valores "Open", "High", "Low" e "Close" de uma cotação pela razão dada. Multiplicar a cotação diretamente resulta no volume vendido ("Volume") também sendo multiplicado, o que pode ser indesejado.

    :param cotacao: Cotação obtida de Ticker.history()
    :type cotacao: pandas.core.frame.DataFrame
    :param razao: Razão pela qual a cotação será multiplicada
    :type razao: float
    """
    cotacao["Open"] *= razao
    cotacao["High"] *= razao
    cotacao["Low"] *= razao
    cotacao["Close"] *= razao

def valor_carteira_reais(carteria):
    """
    Calcula o valor de uma carteira em reais

    Busca os valores dos ativos que estão na carteira usando a biblioteca
    yfinance, converte para reais e os soma. A carteira deve conter uma chave
    "moedas" com valor de um dicionário composto de chaves com o código das
    moedas e valores com a quantidade possuida. A carteira também deve conter
    uma chave "acoes" com valor de um dicionário composto de chaves com o
    código das ações e valores com a quantidade possuida.

    :param carteira: A carteira cujos ativos serão avaliados.
    :type carteira: dict(str, int)
    :return: O valor da carteira em reais
    :rtype: int
    """
    moedas = carteria["moedas"]
    acoes = carteria["acoes"]

    cotacoes = obtem_cotacoes(acoes.keys(), 1)

    moedas_para_conversao = set(moedas.keys())
    for cotacao in cotacoes:
        moeda_da_cotacao = cotacao.info["currency"]
        moedas_para_conversao.add(moeda_da_cotacao)

    #Descarta BRL do set pois ele é a moeda para qual se está convertendo
    moedas_para_conversao.discard("BRL")
    moedas_para_real = moedas_em_real(moedas_para_conversao)
    moedas_para_real["BRL"] = 1

    total_reais = 0

    for moeda, quantidade in moedas:
        moeda_em_reais = quantidade * moedas_para_real[moeda]
        total_reais += moeda_em_reais
    
    for acao, cotacao in cotacoes:
        moeda_acao = cotacao.info["currency"]
        preco_original = cotacao.info["Close"]
        preco_convertido = preco_original * moedas_para_real[moeda_acao]

        acao_em_reais = preco_convertido * acoes[acao]
        total_reais += acao_em_reais
    
    return acao_em_reais