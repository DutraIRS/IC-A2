import busca_carteira
import openpyxl
import pandas as pd
import xlsxwriter

def criar_excel(url):
    carteira = busca_carteira.buscar_carteira(url)
    ativos = list(carteira.items())
    moedas = ativos[0]
    acoes = ativos[1]
    # Lê o dicionário advindo do módulo busca_carteira e transforma em lista

    moedas_nomes_quantidades = moedas[1]
    moedas_nomes = []
    moedas_quantidades = []

    for key, val in moedas_nomes_quantidades.items(): 
        moedas_nomes.append(key) 
    for val in moedas_nomes_quantidades.values():
        moedas_quantidades.append(val)

    acoes_nomes_quantidades = acoes[1]
    acoes_nomes = []
    acoes_quantidades = []

    for key, val in acoes_nomes_quantidades.items(): 
        acoes_nomes.append(key) 
    for val in acoes_nomes_quantidades.values():
        acoes_quantidades.append(val)
    # Cria Excel com openpyxl
    wb = openpyxl.Workbook()
    wb.create_sheet("Carteira")
    wb.remove(wb['Sheet'])
    wb.save("Carteira.xlsx")
        
    # Adiciona as informações advindas do webscraping no Excel
    coluna_moedas = {"moedas": moedas_nomes, "quantidade": moedas_quantidades}
    coluna_acoes = {"ações": acoes_nomes, "quantidade": acoes_quantidades}
    df = pd.DataFrame(coluna_moedas)
    da = pd.DataFrame(coluna_acoes)
    writer = pd.ExcelWriter('Carteira.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False,)
    da.to_excel(writer, sheet_name='welcome', index=False, startcol=3)

    writer.save()
