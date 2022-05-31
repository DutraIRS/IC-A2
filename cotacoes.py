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