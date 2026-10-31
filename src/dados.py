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
    raise NotImplementedError(
        "TODO: implementar dados.normalizar_rotulo(valor)."
    )


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
    raise NotImplementedError(
        "TODO: implementar dados.carregar_csv(caminho)."
    )


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
    raise NotImplementedError(
        "TODO: implementar dados.validar_pontos(pontos, rotulos)."
    )


def parse_ponto(texto):
    """Converte a entrada do usuário "x1,x2" em [x1, x2].

    Contrato:
        - Aceitar vírgula, ponto e vírgula ou espaço como separador.
        - Exigir exatamente dois valores numéricos.
        - Exemplo: "12.5, 80" -> [12.5, 80.0].
        - Lançar ValueError com mensagem clara em caso de formato inválido.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar dados.parse_ponto(texto)."
    )


def caminho_caso(numero):
    """Retorna o caminho absoluto de ``dados/caso<numero>.csv``.

    Contrato:
        - Validar que ``numero`` é inteiro.
        - Não abrir o arquivo; apenas montar o caminho.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar dados.caminho_caso(numero)."
    )


def carregar_caso(numero):
    """Atalho para carregar diretamente ``dados/caso<numero>.csv``.

    Contrato:
        - Reutilizar ``caminho_caso`` e ``carregar_csv``.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar dados.carregar_caso(numero)."
    )
