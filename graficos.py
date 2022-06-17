import busca_carteira
import cotacoes as ctc
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf


#Usando o busca_carteira para obter as ações e moedas
portifolio = busca_carteira.buscar_carteira("https://g-mikael.github.io/investimentos/carteira2.html")
portifolio_list = list(portifolio.values())

#Retirando as moedas e ações dos dicionários
"""Passando para listas separadas para poderem ser usadas
nos comandos hist_moedas_real e hist_acoes"""
portifolio_moedas = (portifolio_list[0])
portifolio_acoes = (portifolio_list[1])

lista_moedas = list(portifolio_moedas.keys())
lista_acoes = list(portifolio_acoes.keys())

"Número de dias analisados (será removido ao transformar em módulo)"                        
num = int(input('Insira o número de dias a serem analisados: ', ))

#Gerando os datasets do histórico das ações e moedas
histmoedas = ctc.hist_moedas_real(lista_moedas, num)
histacoes = ctc.hist_acoes(lista_acoes, num)
histmoedas.reset_index(level = "date", inplace = True)
histacoes.reset_index(level = "date", inplace = True)
print(histmoedas)
print(histacoes)

#Gráfico da variação das moedas no período
plt.plot(histmoedas.date, histmoedas.close)
plt.show()

#Gráfico da variação das ações no período
plt.plot(histacoes.date, histacoes.close)
plt.show()

#Gráfico da variação da carteira em reais
histcarteira = ctc.hist_carteira_reais(portifolio, num)
plt.plot(histcarteira.date, histcarteira.close)
plt.show()
    



