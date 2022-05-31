import yfinance as yf

def obtem_cotacao(acao, dias):
    ticker = yf.Ticker(acao)
    cotacao = ticker.history(f"{dias}d")
    return cotacao

def moeda_em_real(moeda):
    texto_conversao = f"{moeda}BRL=X"
    ticker = yf.Ticker(texto_conversao)
    moeda_em_real = ticker.info["regularMarketPrice"]
    return moeda_em_real