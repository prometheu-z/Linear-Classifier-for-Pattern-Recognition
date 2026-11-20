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

import sys
import os
import math

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
if PASTA_SRC not in sys.path:
    sys.path.insert(0, PASTA_SRC)

import matriz
import solver
import dados

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
    dados.validar_pontos(pontos)
    return [[float(ponto[0]), float(ponto[1]), 1.0] for ponto in pontos]


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
    dados.validar_pontos(pontos, rotulos)
    if len(pontos) < 3:
        raise ValueError("São necessários pelo menos três pontos para o treino.")
    X = montar_X(pontos)
    XT = matriz.transposta(X)
    A = matriz.multiplicar(XT, X)
    y = [float(rotulo) for rotulo in rotulos]
    b = matriz.matriz_vetor(XT, y)
    w, _ = solver.resolver_sistema(A, b)
    if matriz.norma(w[:2]) <= 1e-12:
        raise ValueError("Os pesos calculados não definem uma reta.")
    return w


def decisao(w, ponto):
    """Retorna f(x) = w1·x1 + w2·x2 + w0.

    Contrato:
        - Equivale ao produto interno w · [x1, x2, 1].
        - O sinal indica o lado da reta; o módulo é proporcional à
          distância do ponto à reta.

    TODO: implementar.
    """
    if not isinstance(w, (list, tuple)) or len(w) != 3:
        raise ValueError("w deve conter três pesos: w1, w2 e w0.")
    dados.validar_pontos([ponto])
    return float(w[0]) * float(ponto[0]) + float(w[1]) * float(ponto[1]) + float(w[2])


def classificar(w, ponto):
    """Classifica um ponto e retorna (rótulo, nome da classe).

    Contrato:
        - f(x) >= 0 -> (+1, "Classe A (+1)").
        - f(x) < 0  -> (-1, "Classe B (-1)").
        - Pontos com |f(x)| <= TOLERANCIA_DECISAO são empate e recebem +1,
          seguindo a regra f(x) >= 0.

    TODO: implementar.
    """
    score = decisao(w, ponto)
    rotulo = 1 if score >= -TOLERANCIA_DECISAO else -1
    return rotulo, NOMES_CLASSES[rotulo]


def acuracia(w, pontos, rotulos):
    """Retorna o percentual de acerto no conjunto informado.

    Contrato:
        - Comparar a classificação prevista com cada rótulo esperado.
        - Retornar um número entre 0 e 100 (ex.: 8/10 -> 80.0).
        - Validar que as listas têm o mesmo tamanho.

    TODO: implementar.
    """
    dados.validar_pontos(pontos, rotulos)
    if not pontos:
        raise ValueError("O conjunto para avaliação não pode estar vazio.")
    acertos = sum(classificar(w, ponto)[0] == rotulo
                  for ponto, rotulo in zip(pontos, rotulos))
    return 100.0 * acertos / len(pontos)


def distancia_reta(w, ponto):
    """Retorna a distância com sinal do ponto à reta f(x) = 0.

    Contrato:
        - Fórmula: f(x) / ‖(w1, w2)‖.
        - Sinal positivo para o lado da classe +1; negativo para -1.
        - Lançar ValueError se w1 = w2 = 0 (não há reta).

    TODO: implementar.
    """
    norma_normal = matriz.norma([float(w[0]), float(w[1])])
    if norma_normal <= 1e-12:
        raise ValueError("A reta é indefinida: w1 e w2 são nulos.")
    return decisao(w, ponto) / norma_normal


def equacao_reta(w):
    """Retorna uma string legível da equação f(x) = 0.

    Contrato:
        - Exemplo: "f(x) = -0.5321·x1 + 1.2044·x2 - 12.5 = 0".
        - Tratar o caso w1 = w2 = 0 (reta indefinida).

    TODO: implementar.
    """
    if matriz.norma([float(w[0]), float(w[1])]) <= 1e-12:
        raise ValueError("Reta indefinida: w1 e w2 são nulos.")
    return "f(x) = {:+.6f}*x1 {:+.6f}*x2 {:+.6f} = 0".format(
        float(w[0]), float(w[1]), float(w[2])
    )


def coordenada_x2(w, x1):
    """Retorna x2 da reta para um dado x1.

    Contrato:
        - Fórmula: x2 = -(w1·x1 + w0) / w2.
        - Lançar ValueError quando w2 ≈ 0 (reta vertical).
        - Usada pelo módulo de gráfico.

    TODO: implementar.
    """
    if abs(float(w[1])) <= 1e-12:
        raise ValueError("A reta é vertical: w2 é aproximadamente nulo.")
    return -(float(w[0]) * float(x1) + float(w[2])) / float(w[1])
def projetar_na_reta(w, ponto):
    """Projeta ortogonalmente o ponto sobre a reta separadora."""
    normal = [float(w[0]), float(w[1])]
    n_hat = matriz.versor(normal)
    distancia = distancia_reta(w, ponto)
    return [float(ponto[0]) - distancia * n_hat[0],
            float(ponto[1]) - distancia * n_hat[1]]


def avaliar_modelo(w, pontos, rotulos):
    """Calcula confusão, métricas, resíduos e índices classificados incorretamente."""
    dados.validar_pontos(pontos, rotulos)
    vp = vn = fp = fn = 0
    errados = []
    for indice, (ponto, esperado) in enumerate(zip(pontos, rotulos)):
        previsto = classificar(w, ponto)[0]
        if previsto == 1 and esperado == 1:
            vp += 1
        elif previsto == -1 and esperado == -1:
            vn += 1
        elif previsto == 1 and esperado == -1:
            fp += 1
        else:
            fn += 1
        if previsto != esperado:
            errados.append(indice)
    total = len(pontos)
    acuracia_valor = 100.0 * (vp + vn) / total
    precisao = 100.0 * vp / (vp + fp) if vp + fp else 0.0
    recall = 100.0 * vp / (vp + fn) if vp + fn else 0.0
    residuos = [float(rotulo) - decisao(w, ponto)
                for ponto, rotulo in zip(pontos, rotulos)]
    sse = sum(residuo * residuo for residuo in residuos)
    rmse = math.sqrt(sse / total)
    return {
        "acuracia": acuracia_valor,
        "precisao": precisao,
        "recall": recall,
        "matriz_confusao": {"VP": vp, "VN": vn, "FP": fp, "FN": fn},
        "sse": sse,
        "rmse": rmse,
        "indices_errados": errados,
    }
