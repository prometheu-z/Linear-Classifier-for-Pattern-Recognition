"""Classificador linear binário (ESQUELETO).

Modelo planejado:
    - Ponto de treino: (x1, x2).
    - Matriz aumentada X (m x 3): cada linha é [x1, x2, 1].
    - Vetor de rótulos y: +1 (classe A) ou -1 (classe B).
    - Pesos w = [w1, w2, w0], obtidos por mínimos quadrados:
          (Xᵀ X) w = Xᵀ y
      resolvidas pelo módulo ``solver``.

Função de decisão:
    f(x) = w1·x1 + w2·x2 + w0 = w · [x1, x2, 1]

Regra de classificação:
    f(x) >= 0 -> +1
    f(x) <  0 -> -1

Todos os métodos estão apenas definidos (assinatura + contrato).
"""

# Nomes amigáveis previstos para apresentação dos resultados.
NOMES_CLASSES = {
    1: "Classe A (+1)",
    -1: "Classe B (-1)",
}

# Tolerância prevista para tratar pontos numericamente sobre a reta.
TOLERANCIA_DECISAO = 1e-9


def montar_X(pontos):
    """Monta a matriz de dados aumentada X (m x 3).

    Contrato:
        - Cada ponto (x1, x2) vira a linha [x1, x2, 1].
        - A coluna de 1s permite incluir o termo independente w0 no
          produto interno.
        - Validar que todos os pontos têm duas coordenadas numéricas.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.montar_X(pontos)."
    )


def treinar(pontos, rotulos):
    """Calcula os pesos w por mínimos quadrados (equações normais).

    Contrato:
        - Montar X com ``montar_X``.
        - Calcular Xᵀ, A = XᵀX e b = Xᵀy.
        - Resolver A·w = b com ``solver.resolver_sistema``.
        - Retornar w = [w1, w2, w0].
        - Validar tamanhos, quantidade mínima de pontos e rótulos ±1.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.treinar(pontos, rotulos)."
    )


def decisao(w, ponto):
    """Retorna f(x) = w1·x1 + w2·x2 + w0.

    Contrato:
        - Equivale ao produto interno w · [x1, x2, 1].
        - O sinal indica o lado da reta; o módulo é proporcional à
          distância do ponto à reta.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.decisao(w, ponto)."
    )


def classificar(w, ponto):
    """Classifica um ponto e retorna (rótulo, nome da classe).

    Contrato:
        - f(x) >= 0 -> (+1, "Classe A (+1)").
        - f(x) < 0  -> (-1, "Classe B (-1)").
        - Pontos com |f(x)| <= TOLERANCIA_DECISAO são empate e recebem +1,
          seguindo a regra f(x) >= 0.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.classificar(w, ponto)."
    )


def acuracia(w, pontos, rotulos):
    """Retorna o percentual de acerto no conjunto informado.

    Contrato:
        - Comparar a classificação prevista com cada rótulo esperado.
        - Retornar um número entre 0 e 100 (ex.: 8/10 -> 80.0).
        - Validar que as listas têm o mesmo tamanho.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.acuracia(w, pontos, rotulos)."
    )


def distancia_reta(w, ponto):
    """Retorna a distância com sinal do ponto à reta f(x) = 0.

    Contrato:
        - Fórmula: f(x) / ‖(w1, w2)‖.
        - Sinal positivo para o lado da classe +1; negativo para -1.
        - Lançar ValueError se w1 = w2 = 0 (não há reta).

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.distancia_reta(w, ponto)."
    )


def equacao_reta(w):
    """Retorna uma string legível da equação f(x) = 0.

    Contrato:
        - Exemplo: "f(x) = -0.5321·x1 + 1.2044·x2 - 12.5 = 0".
        - Tratar o caso w1 = w2 = 0 (reta indefinida).

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.equacao_reta(w)."
    )


def coordenada_x2(w, x1):
    """Retorna x2 da reta para um dado x1.

    Contrato:
        - Fórmula: x2 = -(w1·x1 + w0) / w2.
        - Lançar ValueError quando w2 ≈ 0 (reta vertical).
        - Usada pelo módulo de gráfico.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar classificador.coordenada_x2(w, x1)."
    )
