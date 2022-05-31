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
        dicionario_cotacoes[acao] = dicionario_cotacoes[acao].history(texto_historico)
    
    return dicionario_cotacoes

print(obtem_cotacoes(["NFLX", "AAPL"], 1))