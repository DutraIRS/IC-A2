def mostrar_menu():
    titulo = 'O' + ' Selecione uma opção '.center(38, '-') + 'O'
    opcoes = ['Ler carteira', 'Sair']
    parte_inferior = 'O' + '-' * 38 + 'O'

    print(titulo)

    for num, opcao in enumerate(opcoes):
        numero_da_opcao = num + 1
        linha = f'| {numero_da_opcao}. ' + opcao.ljust(34) + '|'
        print(linha)
    
    print(parte_inferior)