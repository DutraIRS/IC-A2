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

def iniciar_interface():
    resposta = -1

    while resposta != '2':
        mostrar_menu()

        resposta = input('Escolha: ')

        match resposta:
            case '1':
                print("TODO: inserir função certa")
            case '2':
                print('Encerrando programa...')