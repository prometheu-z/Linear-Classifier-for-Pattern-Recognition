"""Operações básicas de álgebra linear implementadas com listas Python."""

import math


def transposta(A):
    """Retorna a transposta da matriz ``A``."""
    if not isinstance(A, list) or not A:
        raise ValueError("A matriz não pode estar vazia.")
    if not isinstance(A[0], list) or not A[0]:
        raise ValueError("A matriz deve ser uma lista de linhas não vazias.")
    largura = len(A[0])
    if any(not isinstance(linha, list) or len(linha) != largura for linha in A):
        raise ValueError("Todas as linhas da matriz devem ter o mesmo tamanho.")
    return [[A[i][j] for i in range(len(A))] for j in range(largura)]


def multiplicar(A, B):
    """Retorna o produto matricial ``A · B``."""
    if not isinstance(A, list) or not isinstance(B, list) or not A or not B:
        raise ValueError("As matrizes não podem estar vazias.")
    if not isinstance(A[0], list) or not isinstance(B[0], list):
        raise ValueError("A matriz deve ser formada por linhas em listas.")
    linhas_a, colunas_a = len(A), len(A[0])
    linhas_b, colunas_b = len(B), len(B[0])
    if any(len(linha) != colunas_a for linha in A):
        raise ValueError("Todas as linhas de A devem ter o mesmo tamanho.")
    if any(len(linha) != colunas_b for linha in B):
        raise ValueError("Todas as linhas de B devem ter o mesmo tamanho.")
    if colunas_a != linhas_b:
        raise ValueError("Dimensões incompatíveis: colunas de A devem ser iguais às linhas de B.")
    return [[sum(A[i][k] * B[k][j] for k in range(colunas_a))
             for j in range(colunas_b)] for i in range(linhas_a)]


def matriz_vetor(A, v):
    """Retorna o produto ``A · v``."""
    if not isinstance(A, list) or not isinstance(v, list) or not A or not v:
        raise ValueError("Matriz e vetor não podem estar vazios.")
    if any(not isinstance(linha, list) or len(linha) != len(v) for linha in A):
        raise ValueError("O tamanho do vetor deve ser igual ao número de colunas da matriz.")
    return [sum(linha[j] * v[j] for j in range(len(v))) for linha in A]


def produto_interno(u, v):
    """Retorna o produto interno ``u · v``."""
    if not isinstance(u, list) or not isinstance(v, list):
        raise ValueError("Os vetores devem ser listas.")
    if len(u) != len(v):
        raise ValueError("Vetores com tamanhos diferentes não possuem produto interno definido.")
    return sum(u[i] * v[i] for i in range(len(u)))


def norma(v):
    """Retorna a norma euclidiana ``‖v‖``."""
    if not isinstance(v, list) or not v:
        raise ValueError("O vetor não pode estar vazio.")
    return math.sqrt(produto_interno(v, v))


def versor(v):
    """Retorna o vetor unitário na mesma direção de ``v``."""
    valor_norma = norma(v)
    if valor_norma <= 1e-12:
        raise ValueError("Não existe versor de um vetor com norma aproximadamente nula.")
    return [componente / valor_norma for componente in v]
