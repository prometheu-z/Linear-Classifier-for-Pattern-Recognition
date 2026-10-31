"""Operações básicas de álgebra linear (ESQUELETO).

Escopo deste módulo:
    Implementar manualmente, com listas Python, as operações usadas pelo
    classificador linear. Não é permitido usar numpy.linalg nem funções
    prontas que resolvam as operações por nós.

Convenções:
    - Matriz: lista de listas (A[i][j] = linha i, coluna j).
    - Vetor: lista de números.

Todos os métodos abaixo estão apenas definidos (assinatura + contrato).
As implementações devem ser feitas pelo grupo.
"""


def transposta(A):
    """Retorna a transposta da matriz ``A``.

    Contrato:
        - Se A é m x n, o resultado é n x m.
        - Exemplo: [[1, 2, 3], [4, 5, 6]] -> [[1, 4], [2, 5], [3, 6]].

    TODO: implementar.
    """
    raise NotImplementedError("TODO: implementar matriz.transposta(A).")


def multiplicar(A, B):
    """Retorna o produto matricial ``A · B``.

    Contrato:
        - O número de colunas de A deve ser igual ao número de linhas de B.
        - O elemento (i, j) é o produto interno da linha i de A com a
          coluna j de B.
        - Dimensões incompatíveis devem gerar ValueError com mensagem clara.

    TODO: implementar.
    """
    raise NotImplementedError("TODO: implementar matriz.multiplicar(A, B).")


def matriz_vetor(A, v):
    """Retorna o produto ``A · v`` (matriz por vetor coluna).

    Contrato:
        - O número de colunas de A deve ser igual ao tamanho de v.
        - O resultado é uma lista com uma componente por linha de A.

    TODO: implementar.
    """
    raise NotImplementedError("TODO: implementar matriz.matriz_vetor(A, v).")


def produto_interno(u, v):
    """Retorna o produto interno ``u · v = Σ uᵢ·vᵢ``.

    Contrato:
        - Os vetores devem ter o mesmo tamanho.
        - É a operação central da função de decisão do classificador.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar matriz.produto_interno(u, v)."
    )


def norma(v):
    """Retorna a norma euclidiana ``‖v‖ = √(v · v)``.

    Contrato:
        - Usada, por exemplo, no cálculo da distância de um ponto à reta.
        - Deve reutilizar produto_interno (ou implementar a soma dos
          quadrados manualmente).

    TODO: implementar.
    """
    raise NotImplementedError("TODO: implementar matriz.norma(v).")
