import yfinance as yf

def obtem_cotacao(acao, dias):
   return yf.Ticker(acao).history(f"{dias}d")