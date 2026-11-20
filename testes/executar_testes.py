"""Testes automáticos dos dois casos do classificador."""
import os
import sys

PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SRC = os.path.join(PASTA_RAIZ, "src")
if PASTA_SRC not in sys.path:
    sys.path.insert(0, PASTA_SRC)

import matriz
import solver
import dados
import classificador
import grafico


def testar_algebra_linear():
    """Testa matrizes, norma, versor e eliminação de Gauss."""
    verificacoes = 0
    falhas = []
    casos = [
        (matriz.transposta([[1, 2, 3], [4, 5, 6]]),
         [[1, 4], [2, 5], [3, 6]], "transposta"),
        (matriz.produto_interno([1, 2, 3], [4, 5, 6]),
         32.0, "produto_interno"),
        (matriz.norma([3, 4]), 5.0, "norma"),
    ]
    for obtido, esperado, nome in casos:
        verificacoes += 1
        if obtido != esperado:
            falhas.append("{}: obtido {!r}, esperado {!r}".format(nome, obtido, esperado))
    verificacoes += 1
    w, det = solver.resolver_sistema([[2, 1], [1, 3]], [5, 7])
    if abs(w[0] - 1.6) > 1e-9 or abs(w[1] - 1.8) > 1e-9:
        falhas.append("Gauss: solução 2x2 incorreta")
    verificacoes += 1
    if abs(det - 5.0) > 1e-9:
        falhas.append("Gauss: determinante incorreto")
    try:
        solver.resolver_sistema([[1, 2], [2, 4]], [3, 6])
        falhas.append("Gauss: matriz singular não lançou ValueError")
    except ValueError:
        pass
    verificacoes += 1
    return verificacoes, falhas


def testar_caso1():
    """Testa dados separáveis, métricas, geometria e geração do gráfico."""
    verificacoes = 0
    falhas = []
    pontos, rotulos = dados.carregar_caso(1)
    w = classificador.treinar(pontos, rotulos)
    avaliacao = classificador.avaliar_modelo(w, pontos, rotulos)
    novos = [[3, 10], [3, 2]]

    verificacoes += 1
    if abs(avaliacao["acuracia"] - 100.0) > 1e-9:
        falhas.append("Caso 1: acurácia de treino deveria ser 100%")
    verificacoes += 1
    if not (w[0] != 0 or w[1] != 0):
        falhas.append("Caso 1: vetor normal nulo")
    for ponto, esperado in zip(novos, [1, -1]):
        verificacoes += 1
        obtido = classificador.classificar(w, ponto)[0]
        if obtido != esperado:
            falhas.append("Caso 1: {} deveria ser {}, obteve {}".format(ponto, esperado, obtido))
    verificacoes += 1
    n_hat = matriz.versor([w[0], w[1]])
    if not (classificador.decisao(w, [3, 10]) * n_hat[1] > 0):
        falhas.append("Caso 1: direção do vetor normal não aponta para a classe +1")

    pasta = os.path.join(PASTA_RAIZ, "resultados")
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, "painel_caso1.png")
    grafico.plotar_analise_completa(pontos, rotulos, w, novos,
                                    titulo="Caso 1 - dados linearmente separáveis",
                                    salvar_em=destino)
    verificacoes += 1
    if not os.path.isfile(destino):
        falhas.append("Caso 1: gráfico não foi gerado")
    return verificacoes, falhas


def testar_caso2():
    """Testa sobreposição, erro destacado, fronteira e regra de desempate."""
    verificacoes = 0
    falhas = []
    pontos, rotulos = dados.carregar_caso(2)
    w = classificador.treinar(pontos, rotulos)
    avaliacao = classificador.avaliar_modelo(w, pontos, rotulos)
    ponto_frente = [3.0, classificador.coordenada_x2(w, 3.0)]
    novos = [[3, 9], [6, 1], ponto_frente]

    verificacoes += 1
    if not (avaliacao["acuracia"] < 100.0):
        falhas.append("Caso 2: acurácia deveria ser menor que 100%")
    verificacoes += 1
    if not avaliacao["indices_errados"]:
        falhas.append("Caso 2: esperado pelo menos um ponto mal classificado")
    verificacoes += 1
    if abs(classificador.decisao(w, ponto_frente)) > 1e-7:
        falhas.append("Caso 2: ponto da fronteira não possui f(x)=0")
    verificacoes += 1
    if classificador.classificar(w, ponto_frente)[0] != 1:
        falhas.append("Caso 2: desempate sobre a reta deveria ser +1")

    pasta = os.path.join(PASTA_RAIZ, "resultados")
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, "painel_caso2.png")
    grafico.plotar_analise_completa(pontos, rotulos, w, novos,
                                    titulo="Caso 2 - sobreposição e ruído",
                                    salvar_em=destino)
    verificacoes += 1
    if not os.path.isfile(destino):
        falhas.append("Caso 2: gráfico não foi gerado")
    return verificacoes, falhas


def main():
    """Executa todos os testes e imprime um resumo."""
    total = 0
    todas_falhas = []
    for nome, funcao in (
        ("Álgebra linear", testar_algebra_linear),
        ("Caso 1", testar_caso1),
        ("Caso 2", testar_caso2),
    ):
        try:
            quantidade, falhas = funcao()
            total += quantidade
            todas_falhas.extend(falhas)
            print("{}: {} verificacoes, {} falhas".format(
                nome, quantidade, len(falhas)))
        except Exception as erro:
            total += 1
            todas_falhas.append("{} lançou exceção: {}".format(nome, erro))
    print("Resumo: {} verificacoes, {} falhas".format(total, len(todas_falhas)))
    for falha in todas_falhas:
        print("ERRO:", falha)
    return 0 if not todas_falhas else 1


if __name__ == "__main__":
    raise SystemExit(main())
