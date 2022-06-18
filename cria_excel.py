import busca_carteira
import openpyxl
import pandas as pd
import xlsxwriter
import cotacoes
import cria_qr_code
from openpyxl.drawing.image import Image
from openpyxl.styles import Font

def criar_excel(url):
    
    # Lê o dicionário advindo do módulo busca_carteira e transforma em lista
    carteira = busca_carteira.buscar_carteira(url)
    ativos = list(carteira.items())
    moedas = ativos[0]
    acoes = ativos[1]

    #tranforma o dicionário moedas em lista
    moedas_nomes_quantidades = moedas[1]
    moedas_nomes = []
    moedas_quantidades = []

    for key, val in moedas_nomes_quantidades.items(): 
        moedas_nomes.append(key) 
    for val in moedas_nomes_quantidades.values():
        moedas_quantidades.append(val)
    
    #transforma o dicionário acoes em lista
    acoes_nomes_quantidades = acoes[1]
    acoes_nomes = []
    acoes_quantidades = []

    for key, val in acoes_nomes_quantidades.items(): 
        acoes_nomes.append(key) 
    for val in acoes_nomes_quantidades.values():
        acoes_quantidades.append(val)

    #obtém as cotações
    info_cotacoes = cotacoes.obtem_cotacoes(acoes_nomes)
    valor_acoes = []
    moeda_acao = []
    for val in info_cotacoes.values():
        valor_acoes.append(val['regularMarketPrice'])
        moeda_acao.append(val['currency'])
        
    #valor individual ativo em Real
    valor_uni = cotacoes.unidade_ativos_real(carteira)
    valor_uni_ativos = list(valor_uni.items())
    valor_uni_moedas = valor_uni_ativos[1]
    valor_uni_acoes = valor_uni_ativos[0]

    valor_uni_moedas_nomes_quantidades = valor_uni_moedas[1]
    valor_moedas_BRL = []

    for val in valor_uni_moedas_nomes_quantidades.values():
        valor_moedas_BRL.append(val)
    

    valor_uni_acoes_nomes_quantidades = valor_uni_acoes[1]
    valor_acoes_BRL = []

    for val in valor_uni_acoes_nomes_quantidades.values():
        valor_acoes_BRL.append(val)
    
    #valor Total ativo em Real                          
    valor_total = cotacoes.valor_ativos_reais(carteira)
    valor_total_ativos = list(valor_total.items())
    valor_total_moedas = valor_total_ativos[1]
    valor_total_acoes = valor_total_ativos[0]

    valor_total_moedas_nomes_quantidades = valor_total_moedas[1]
    valor_moedas_BRL_total = []

    for val in valor_total_moedas_nomes_quantidades.values():
        valor_moedas_BRL_total.append(val)
    

    valor_total_acoes_nomes_quantidades = valor_total_acoes[1]
    valor_acoes_BRL_total = []

    for val in valor_total_acoes_nomes_quantidades.values():
        valor_acoes_BRL_total.append(val)
    
    #valor total da Carteira
    a = ["==="]
    valor_total_carteira_BRL = cotacoes.valor_carteira_reais(carteira)

    # Cria Excel com openpyxl
    wb = openpyxl.Workbook()
    wb.save("Carteira.xlsx")
        
    # Adiciona as informações advindas do webscraping no Excel
    coluna_moedas = {"moedas": moedas_nomes, "quantidade": moedas_quantidades, "valor unidade(BRL)":valor_moedas_BRL, "valor total(BRL)": valor_moedas_BRL_total}
    coluna_acoes = {"ações": acoes_nomes, "quantidade": acoes_quantidades, "valor da ação": valor_acoes, "moeda (ação)": moeda_acao, "valor unidade(BRL)": valor_acoes_BRL, "valor total(BRL)":valor_acoes_BRL_total}
    df = pd.DataFrame(coluna_moedas)
    da = pd.DataFrame(coluna_acoes)
    writer = pd.ExcelWriter('Carteira.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Carteira', index=False,)
    da.to_excel(writer, sheet_name='Carteira', index=False, startcol=6)
    writer.save()

    #Insere o valor total da carteira e formata as colunas
    wb = openpyxl.load_workbook("Carteira.xlsx")
    ws = wb.active
    Carteira_page = wb["Carteira"]
    Carteira_page['N1'] = "Valor Total Carteira(BRL)"
    Carteira_page['N2'] = round(valor_total_carteira_BRL, 2)
    Carteira_page['N1'].font = Font(bold=True)
    Carteira_page.column_dimensions['A'].width = 20
    Carteira_page.column_dimensions['B'].width = 20
    Carteira_page.column_dimensions['C'].width = 20
    Carteira_page.column_dimensions['D'].width = 20
    Carteira_page.column_dimensions['G'].width = 20
    Carteira_page.column_dimensions['H'].width = 20
    Carteira_page.column_dimensions['I'].width = 20
    Carteira_page.column_dimensions['J'].width = 20
    Carteira_page.column_dimensions['K'].width = 20
    Carteira_page.column_dimensions['L'].width = 20
    Carteira_page.column_dimensions['N'].width = 22
    
    #salva o excel
    wb.save("Carteira.xlsx")

    #Chama a função para criar o qr code
    cria_qr_code.criar_qr("Carteira.xlsx","Carteira", 'N2','N5')
