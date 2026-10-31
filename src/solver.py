"""Resolução de sistemas lineares (ESQUELETO).

Escopo deste módulo:
    Resolver ``A · x = b`` manualmente por eliminação de Gauss com
    pivotamento parcial. Não usar numpy.linalg.solve, numpy.linalg.inv,
    scipy nem funções equivalentes.

O método será usado para resolver as equações normais do classificador:
    (XᵀX) w = Xᵀ y
"""


def resolver_sistema(A, b, tolerancia=1e-12):
    """Resolve o sistema linear ``A · x = b``.

    Parâmetros:
        A: matriz quadrada n x n (lista de listas).
        b: vetor de termos independentes com n elementos.
        tolerancia: valor abaixo do qual um pivô é considerado zero
            (detecção de matriz singular/mal condicionada).

    Retorno:
        Lista ``x`` com os n valores da solução.

    Contrato:
        - Validar dimensões e tipos antes de calcular.
        - Aplicar eliminação de Gauss com pivotamento parcial.
        - Lançar ValueError com mensagem clara se o sistema não tiver
          solução única.
        - Não alterar as listas A e b recebidas.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar solver.resolver_sistema(A, b, tolerancia)."
    )
