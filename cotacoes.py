import yfinance as yf

def obtem_cotacao(acao, dias):
   return yf.Ticker(acao).history(f"{dias}d")

def moeda_em_reais(moeda):
    return yf.Ticker(f"{moeda}BRL=X").info["regularMarketPrice"]