import qrcode
import openpyxl as opx
from openpyxl.drawing.image import Image
#openpyxl requer a biblioteca pillow instalada para trabalhar com imagens

def criar_qr(arquivo, planilha, total, celula):
# arquivo é o nome do arquivo a ser editado (ex: 'carteira_joaozinho.xlsx')
# planilha é a planilha do workbook a ser editada (ex: 'Planilha1')
# total é a célula onde está o valor total da carteira na planilha (ex: 'A2')
# celula é a célula perto da qual a imagem deve ser inserida (ex: 'D2')

    wb = opx.load_workbook(arquivo)
    sh = wb[planilha]
    valor = sh[total].value
# carrega o arquivo, olha para a planilha desejada e descobre o valor total da carteira

    mensagem = str('Esta carteira de investimentos vale ' + str(valor) + ' ao todo.')
    img = qrcode.make(mensagem)
    img.save(str('aaa.png'))
    img = Image("aaa.png")
#cria e salva a imagem

    sh.add_image(img, celula)
    wb.save(arquivo)
# insere a imagem e salva o arquivo
