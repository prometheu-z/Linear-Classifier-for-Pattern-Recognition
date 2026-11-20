"""Leitura e validação dos dados (ESQUELETO).

Formato previsto dos arquivos CSV em ``dados/``:
    x1,x2,classe
    12,85,1
    2,40,-1

A classe pode ser +1/-1 ou A/B (também podem ser aceitos
"aprovado"/"reprovado"). Internamente, o programa trabalhará com +1/-1.

Todos os métodos estão apenas definidos (assinatura + contrato).
"""

import os
import csv
import re

# Pasta raiz do projeto: .../vetores (um nível acima de src/).
PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(PASTA_RAIZ, "dados")


def normalizar_rotulo(valor):
    """Converte um rótulo lido do CSV para +1 ou -1.

    Contrato:
        - Aceitar +1/1/A/aprovado/positivo/true -> +1.
        - Aceitar -1/B/reprovado/negativo/false -> -1.
        - Não diferenciar maiúsculas/minúsculas.
        - Lançar ValueError com mensagem clara para qualquer outro valor.

    TODO: implementar.
    """
    texto = str(valor).strip().lower()
    if texto in ("+1", "1", "a", "aprovado", "positivo", "true"):
        return 1
    if texto in ("-1", "-1.0", "b", "reprovado", "negativo", "false"):
        return -1
    raise ValueError("Rótulo inválido: {!r}. Use +1/-1, A/B ou aprovado/reprovado.".format(valor))


def carregar_csv(caminho):
    """Carrega um CSV de treinamento e retorna (pontos, rotulos).

    Contrato:
        - Ignorar linhas vazias e comentários iniciados por '#'.
        - Aceitar cabeçalho na primeira linha (detectar quando o primeiro
          campo não é numérico).
        - Exigir três colunas: x1, x2, classe.
        - Retornar pontos como [[x1, x2], ...] e rótulos como [+1/-1, ...].
        - Lançar FileNotFoundError/ValueError com mensagens claras.

    TODO: implementar.
    """
    if not os.path.isfile(caminho):
        raise FileNotFoundError("Arquivo CSV não encontrado: {}".format(caminho))
    pontos, rotulos = [], []
    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            try:
                campos = next(csv.reader([linha]))
            except csv.Error as erro:
                raise ValueError("Linha CSV inválida {}: {}".format(numero_linha, erro))
            if len(campos) != 3:
                raise ValueError("Linha {} deve conter exatamente três colunas: x1,x2,classe.".format(numero_linha))
            if numero_linha == 1 and campos[0].strip().lower() == "x1":
                continue
            try:
                x1 = float(campos[0].strip())
                x2 = float(campos[1].strip())
            except ValueError:
                if campos[0].strip().lower() in ("x1", "feature1"):
                    continue
                raise ValueError("Coordenadas inválidas na linha {}.".format(numero_linha))
            pontos.append([x1, x2])
            rotulos.append(normalizar_rotulo(campos[2]))
    validar_pontos(pontos, rotulos)
    return pontos, rotulos


def validar_pontos(pontos, rotulos=None):
    """Valida uma lista de pontos e, opcionalmente, os rótulos.

    Contrato:
        - A lista de pontos não pode estar vazia.
        - Cada ponto deve ter exatamente duas coordenadas numéricas.
        - Se rotulos for informado, deve ter o mesmo tamanho e conter
          apenas +1 ou -1.
        - Lançar ValueError com mensagem clara em caso de problema.

    TODO: implementar.
    """
    if not isinstance(pontos, list) or not pontos:
        raise ValueError("A lista de pontos não pode estar vazia.")
    for indice, ponto in enumerate(pontos):
        if not isinstance(ponto, (list, tuple)) or len(ponto) != 2:
            raise ValueError("O ponto {} deve ter exatamente duas coordenadas.".format(indice))
        if any(isinstance(valor, bool) or not isinstance(valor, (int, float)) for valor in ponto):
            raise ValueError("As coordenadas do ponto {} devem ser numéricas.".format(indice))
    if rotulos is not None:
        if not isinstance(rotulos, list) or len(rotulos) != len(pontos):
            raise ValueError("A quantidade de rótulos deve ser igual à quantidade de pontos.")
        if any(rotulo not in (-1, 1) for rotulo in rotulos):
            raise ValueError("Os rótulos devem conter apenas +1 ou -1.")
    return True


def parse_ponto(texto):
    """Converte a entrada do usuário "x1,x2" em [x1, x2].

    Contrato:
        - Aceitar vírgula, ponto e vírgula ou espaço como separador.
        - Exigir exatamente dois valores numéricos.
        - Exemplo: "12.5, 80" -> [12.5, 80.0].
        - Lançar ValueError com mensagem clara em caso de formato inválido.

    TODO: implementar.
    """
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Formato inválido: informe duas coordenadas, por exemplo '12,80'.")
    partes = re.split(r"[,;\s]+", texto.strip())
    if len(partes) != 2:
        raise ValueError("Formato inválido: devem existir exatamente duas coordenadas.")
    try:
        ponto = [float(partes[0]), float(partes[1])]
    except ValueError:
        raise ValueError("Formato inválido: as duas coordenadas devem ser números.")
    validar_pontos([ponto])
    return ponto


def caminho_caso(numero):
    """Retorna o caminho absoluto de ``dados/caso<numero>.csv``.

    Contrato:
        - Validar que ``numero`` é inteiro.
        - Não abrir o arquivo; apenas montar o caminho.

    TODO: implementar.
    """
    if not isinstance(numero, int) or isinstance(numero, bool):
        raise ValueError("O número do caso deve ser um inteiro.")
    if numero not in (1, 2):
        raise ValueError("Caso desconhecido: use 1 ou 2.")
    return os.path.join(PASTA_DADOS, "caso{}.csv".format(numero))


def carregar_caso(numero):
    """Atalho para carregar diretamente ``dados/caso<numero>.csv``.

    Contrato:
        - Reutilizar ``caminho_caso`` e ``carregar_csv``.

    TODO: implementar.
    """
    return carregar_csv(caminho_caso(numero))
