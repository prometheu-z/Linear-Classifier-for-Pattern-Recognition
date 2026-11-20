"""Eliminação de Gauss com pivotamento parcial."""


def resolver_sistema(A, b, tolerancia=1e-12):
    """Resolve ``A·x=b`` e retorna ``(x, det_A)``."""
    if not isinstance(A, list) or not A or not isinstance(b, list):
        raise ValueError("A e b devem ser listas válidas.")
    n = len(A)
    if len(b) != n:
        raise ValueError("O vetor b deve ter o mesmo tamanho da matriz A.")
    if any(not isinstance(linha, list) or len(linha) != n for linha in A):
        raise ValueError("A deve ser uma matriz quadrada.")
    if tolerancia <= 0:
        raise ValueError("A tolerância deve ser positiva.")

    aumentado = [list(A[i]) + [b[i]] for i in range(n)]
    determinante = 1.0
    troca_sinal = 1
    for coluna in range(n):
        pivor = max(range(coluna, n), key=lambda linha: abs(aumentado[linha][coluna]))
        if abs(aumentado[pivor][coluna]) <= tolerancia:
            raise ValueError("Sistema sem solução única: matriz singular.")
        if pivor != coluna:
            aumentado[coluna], aumentado[pivor] = aumentado[pivor], aumentado[coluna]
            troca_sinal *= -1
        pivot = aumentado[coluna][coluna]
        determinante *= pivot
        for linha in range(coluna + 1, n):
            fator = aumentado[linha][coluna] / pivot
            aumentado[linha][coluna] = 0.0
            for j in range(coluna + 1, n + 1):
                aumentado[linha][j] -= fator * aumentado[coluna][j]

    determinante *= troca_sinal
    if abs(determinante) <= tolerancia:
        raise ValueError("Sistema sem solução única: determinante nulo.")

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(aumentado[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (aumentado[i][n] - soma) / aumentado[i][i]
    return x, determinante


def determinante_gauss(A, tolerancia=1e-12):
    """Calcula o determinante pelo mesmo processo de eliminação de Gauss."""
    n = len(A)
    _, det = resolver_sistema(A, [0.0] * n, tolerancia)
    return det
