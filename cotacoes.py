import pandas as pd
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

    dicionario_acoes_cot = {}
    dicionario_cotacoes = tickers_acoes.price

    for acao, infos in dicionario_cotacoes.items():
        # Se a ação não for encontrada, uma string é retornada
        if isinstance(infos, str):
            print(
                f"-> Atenção! Ignorando cotação de \"{acao}\" pois não foi encontrada")
            continue

        dicionario_acoes_cot[acao] = infos

    return dicionario_acoes_cot


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
        if texto_conversao.endswith("BRL=X"):
            moeda = texto_conversao[:-5]
        else:
            moeda = texto_conversao

        # Se a moeda não for encontrada, uma string é retornada
        if isinstance(ticker, str):
            print(
                f"-> Atenção! Ignorando cotação de \"{moeda}\" pois não foi encontrada")
            continue

        moeda_em_real = ticker["regularMarketPrice"]

        dicionario_valor_real[moeda] = moeda_em_real

    return dicionario_valor_real


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


def concatena_historico(dicionario):
    """Obtém os dataframes dos valores do dicionário e os concatena juntos

    Obtém os dataframes dos valores do dicionário e os une usando a chave como
    índice de nome "symbol" no dataframe resultante

    :param dicionario: Dicionário 
    :type dicionario: dict(str, any)
    :return: Dataframe resultante da concatenação
    :rtype: pandas.core.frame.DataFrame
    """
    data_frames = {}

    for ativo, valor in dicionario.items():
        # Encontra todos data frames para juntar depois
        if isinstance(valor, pd.DataFrame):
            # Renomeia o índice para ser consistente com outros data frames
            valor.index.name = "date"
            data_frames[ativo] = valor
        else:
            print(f"-> Atenção! Ignorando histórico de \"{ativo}\" pois não foi encontrado")

    # Especifica que a chave do dicionário será um novo índice chamado "symbol"
    df = pd.concat(data_frames, names=["symbol"])

    return df


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

    # Se algum ativo não tiver histórico, um dicionário é retornado
    if isinstance(df, dict):
        df = concatena_historico(df)

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

    # Se algum ativo não tiver histórico, um dicionário é retornado
    if isinstance(df, dict):
        df = concatena_historico(df)

    # Remove entradas duplicadas
    df = df[~df.index.duplicated(keep="last")]

    return df


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
        # Testa para checar se foi encontrada uma conversão da moeda
        if moeda in moedas_para_real:
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


def hist_carteira_por_ativo(carteira, dias):
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

    conjunto_acoes = set(acoes.keys())
    acoes_com_hist = historico_acoes.index.get_level_values("symbol")
    acoes_carteira_com_hist = conjunto_acoes.intersection(acoes_com_hist)

    for acao in acoes_carteira_com_hist:
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

    conjunto_moedas = set(moedas.keys())
    moedas_com_historico = dict_novos_nomes.values()

    # Lista de moedas na carteira que têm histórico
    lista_hist_moedas = list(
        conjunto_moedas.intersection(moedas_com_historico))

    # Remove as moedas usadas apenas para calcular os valores das ações
    hist_conversoes = hist_conversoes.loc[lista_hist_moedas]

    historicos = {"acoes": historico_acoes, "moedas": hist_conversoes}

    return historicos


def hist_carteira_total(carteira, dias):
    """Calcula o histórico do valor total da carteira

    Calcula o histórico do valor total da carteira. Se todos os ativos não possuírem histórico para os dias especificados, será retornado o histórico para o maior número de dias possíveis.

    :param carteira: A carteira com os ativos
    :type carteira: dict(str, dict(str, float))
    :param dias: Número de dias de histórico
    :type dias: int
    :return: Dataframe contendo os dias de histórico e seus valores
    :rtype: pandas.core.frame.DataFrame
    """    
    historicos = hist_carteira_por_ativo(carteira, dias)
    min_dias = dias

    for hist in historicos.values():
        ativos = hist.index.get_level_values("symbol").unique()

        for ativo in ativos:
            hist_ativo = hist.loc[[ativo]]

            # Obtém a primeira dimensão do data frame, linhas
            num_dias = hist_ativo.shape[0]

            if num_dias < min_dias:
                min_dias = num_dias
    
    if min_dias < dias:
        print(f"-> Atenção! O histórico do valor total da carteira será do período de {min_dias} dias por limitações dos históricos dos ativos")
    
    todos_hist = pd.concat(historicos.values())

    # Remove os índices "symbol" pois apenas as datas importam
    todos_hist.reset_index(level="symbol", drop=True, inplace=True)

    # Remove a coluna "volume" pois é irrelevante para esse histórico
    todos_hist.drop(columns="volume", inplace=True)

    lista_dias = todos_hist.index.unique()
    dias_com_tds_hists = lista_dias[-min_dias:]

    hist_dias_completos = todos_hist.loc[dias_com_tds_hists]

    # Calcula a soma das colunas agrupando pela data
    hist_total_carteira = hist_dias_completos.groupby(level=0).sum()

    return hist_total_carteira
