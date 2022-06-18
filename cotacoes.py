import yahooquery as yq
import busca_carteira as bc


def obtem_cotacoes(acoes):
    """Obtém as cotações das ações dadas.

    Recebe uma lista de códigos de ações, busca as cotações das ações utilizando a biblioteca yahooquery e retorna um dicionário ligando os códigos das ações com suas respectivas cotações.

    :param acoes: Lista dos códigos das ações
    :type acoes: list(str)
    :return: Um dicionário ligando as ações com suas cotações
    :rtype: dict(str, dict(str, Any))
    """
    texto_acoes = ' '.join(acoes)
    tickers_acoes = yq.Ticker(texto_acoes)

    dicionario_cotacoes = tickers_acoes.price

    return dicionario_cotacoes


def moedas_em_real(moedas):
    """Recebe uma lista de moedas e retorna os valores delas em reais.

    Recebe uma lista de códigos de moedas, busca os valores de conversão para
    real (BRL) utilizando a biblioteca yahooquery e retorna um dicionário ligando
    os códigos com seus respectivos valores de conversão para real.

    :param moedas: Lista de códigos de moedas
    :type moedas: list(str)
    :return: Dicionário ligando os códigos com os valores de conversão
    :rtype: dict(str, float)
    """
    dicionario_valor_real = {}
    conjunto_moedas = set(moedas)

    # Checa se BRL está no conjunto pois ele não precisado ser buscado
    if "BRL" in conjunto_moedas:
        dicionario_valor_real["BRL"] = 1
        conjunto_moedas.remove("BRL")

    textos_moedas = []
    for moeda in conjunto_moedas:
        # Checa se o texto já está no formato necessário para o ticker
        if moeda.endswith("=X"):
            texto_conversao = moeda
        else:
            texto_conversao = f"{moeda}BRL=X"

        textos_moedas.append(texto_conversao)

    texto_conversoes = ' '.join(textos_moedas)
    tickers_moedas = yq.Ticker(texto_conversoes)
    dicionario_cotacoes = tickers_moedas.price

    for texto_conversao, ticker in dicionario_cotacoes.items():
        moeda_em_real = ticker["regularMarketPrice"]

        if texto_conversao.endswith("BRL=X"):
            moeda = texto_conversao[:-5]
        else:
            moeda = texto_conversao

        dicionario_valor_real[moeda] = moeda_em_real

    return dicionario_valor_real


def multiplica_cotacao(cotacao, razao):
    """Multiplica uma cotação por um valor.

    Multiplica os valores "Open", "High", "Low" e "Close" de uma cotação pela
    razão dada. Multiplicar a cotação diretamente resulta no volume vendido
    ("Volume") também sendo multiplicado, o que pode ser indesejado.

    :param cotacao: Cotação obtida de Ticker.history()
    :type cotacao: pandas.core.frame.DataFrame
    :param razao: Razão pela qual a cotação será multiplicada
    :type razao: float
    """
    cotacao["Open"] *= razao
    cotacao["High"] *= razao
    cotacao["Low"] *= razao
    cotacao["Close"] *= razao


def valor_carteira_reais(carteira):
    """Calcula o valor de uma carteira em reais.

    Busca os valores dos ativos que estão na carteira usando a biblioteca
    yahooquery, converte para reais e os soma. A carteira deve conter uma chave
    "moedas" com valor de um dicionário composto de chaves com o código das
    moedas e valores com a quantidade possuida. A carteira também deve conter
    uma chave "acoes" com valor de um dicionário composto de chaves com o
    código das ações e valores com a quantidade possuida.

    :param carteira: A carteira cujos ativos serão avaliados.
    :type carteira: dict(str, dict(str, float))
    :return: O valor da carteira em reais
    :rtype: int
    """
    valores = valor_ativos_reais(carteira)
    acoes = valores["acoes"]
    moedas = valores["moedas"]

    total_reais = 0

    for valor in acoes.values():
        total_reais += valor

    for valor in moedas.values():
        total_reais += valor

    return total_reais


def hist_acoes(acoes, dias):
    """Obtém o histórico das ações com o número de dias especificado

    :param ativo: Lista de códigos das ações
    :type ativo: list(str)
    :param dias: Número de dias de histórico
    :type dias: int
    :return: Data frame contendo os históricos
    :rtype: pandas.core.frame.DataFrame
    """
    texto_acoes = ' '.join(acoes)
    ticker = yq.Ticker(texto_acoes)

    texto_periodo = f"{dias}d"
    df = ticker.history(texto_periodo)

    return df


def hist_moedas_real(moedas, dias):
    """Obtém o histórico do valor das moedas em reais

    :param moedas: Lista dos códigos das moedas, ignorando "BRL" se presente
    :type moedas: list(str)
    :param dias: Número de dias de histórico
    :type dias: int
    :return: Data frame contendo os históricos
    :rtype: pandas.core.frame.DataFrame
    """
    # Descarta BRL pois ele não posssui histórico de conversão para si mesmo
    conjunto_moedas = set(moedas)
    conjunto_moedas.discard("BRL")

    textos_conversao = []
    for moeda in conjunto_moedas:
        if moeda.endswith("=X"):
            texto_conversao = moeda
        else:
            texto_conversao = f"{moeda}BRL=X"

        textos_conversao.append(texto_conversao)

    texto_moedas = ' '.join(textos_conversao)
    ticker = yq.Ticker(texto_moedas)

    texto_periodo = f"{dias}d"
    df = ticker.history(texto_periodo)

    # Remove entradas duplicadas
    df = df[~df.index.duplicated(keep="last")]

    return df


def hist_carteira_reais(carteira, dias):
    """Obtém os históricos em reais de todos ativos da carteira

    :param carteira: A carteira com os ativos
    :type carteira: dict(str, dict(str, float))
    :param dias: Número de dias de histórico
    :type dias: int
    :return: Dicionário de duas entradas com os históricos
    :rtype: dict(str, pandas.core.frame.DataFrame)
    """
    moedas = carteira["moedas"]
    acoes = carteira["acoes"]

    cotacoes = obtem_cotacoes(acoes.keys())

    moedas_para_conversao = set(moedas.keys())
    for cotacao in cotacoes.values():
        moeda_da_cotacao = cotacao["currency"]
        moedas_para_conversao.add(moeda_da_cotacao)

    hist_conversoes = hist_moedas_real(moedas_para_conversao, dias)
    historico_acoes = hist_acoes(acoes.keys(), dias)

    # Obtém os nomes dos índices de conversão. (ex: USDBRL=X)
    nomes_conversoes = hist_conversoes.index.get_level_values("symbol")

    dict_novos_nomes = {}
    for nome_antigo in nomes_conversoes:
        if not nome_antigo.endswith("BRL=X"):
            continue

        novo_nome = nome_antigo[:-5]
        dict_novos_nomes[nome_antigo] = novo_nome

    # Remove o texto "BRL=X" dos índices
    hist_conversoes = hist_conversoes.rename(index=dict_novos_nomes)

    for acao in acoes:
        moeda_acao = cotacoes[acao]["currency"]

        if moeda_acao == "BRL":
            continue

        linhas_moeda_indexadas = hist_conversoes.loc[[moeda_acao]]

        # Remove os índices para permitir a multiplicação de data frames
        linhas_moeda = linhas_moeda_indexadas.reset_index(
            level="symbol", drop=True)

        # Multiplica os valores entrada por entrada, exceto o volume
        historico_acoes.loc[[acao],
                            historico_acoes.columns != "volume"] *= linhas_moeda

    # Prepara as moedas da carteira, exceto BRL por não possuir histórico
    lista_moedas = list(moedas.keys())
    if "BRL" in lista_moedas:
        lista_moedas.remove("BRL")

    # Remove as moedas usadas apenas para calcular os valores das ações
    hist_conversoes = hist_conversoes.loc[lista_moedas]

    historicos = {"acoes": historico_acoes, "moedas": hist_conversoes}

    return historicos


def unidade_ativos_real(carteira):
    """Calcula quanto vale a unidade de cada ativo em reais

    :param carteira: A carteira com os ativos
    :type carteira: dict(str, dict(str, float))
    :return: Dicionário com duas entradas "moedas" e "acoes" com os valores
    :rtype: dict(str, dict(str, float))
    """
    moedas = carteira["moedas"]
    acoes = carteira["acoes"]

    cotacoes = obtem_cotacoes(acoes.keys())

    moedas_para_conversao = set(moedas.keys())
    for cotacao in cotacoes.values():
        moeda_da_cotacao = cotacao["currency"]
        moedas_para_conversao.add(moeda_da_cotacao)

    moedas_para_real = moedas_em_real(moedas_para_conversao)

    valor_un_acoes = {}
    valor_un_moedas = {}

    for moeda in moedas:
        # Não inclui moedas apenas usadas para converter ações
        valor_un_moedas[moeda] = moedas_para_real[moeda]

    for acao, cotacao in cotacoes.items():
        moeda_acao = cotacao["currency"]
        preco_original = cotacao["regularMarketPrice"]
        preco_convertido = preco_original * moedas_para_real[moeda_acao]

        valor_un_acoes[acao] = preco_convertido

    unidade_ativo_reais = {"acoes": valor_un_acoes, "moedas": valor_un_moedas}

    return unidade_ativo_reais


def valor_ativos_reais(carteira):
    """Calcula quantos reais a carteira tem em cada ativo

    :param carteira: A carteira com os ativos
    :type carteira: dict(str, dict(str, float))
    :return: Dicionário com duas entradas "moedas" e "acoes" com os valores
    :rtype: dict(str, dict(str, float))
    """
    moedas = carteira["moedas"]
    acoes = carteira["acoes"]

    valores_un = unidade_ativos_real(carteira)
    valor_un_acoes = valores_un["acoes"]
    valor_un_moedas = valores_un["moedas"]

    total_por_acao = {}
    total_por_moeda = {}

    for moeda, quantidade in moedas.items():
        total_moeda = quantidade * valor_un_moedas[moeda]
        total_por_moeda[moeda] = total_moeda

    for acao, quantidade in acoes.items():
        total_acao = quantidade * valor_un_acoes[acao]
        total_por_acao[acao] = total_acao

    ativos_em_real = {"acoes": total_por_acao, "moedas": total_por_moeda}

    return ativos_em_real
