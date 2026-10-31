"""Geração do gráfico do classificador (ESQUELETO).

Escopo deste módulo:
    Desenhar, com matplotlib, os pontos de treino, a reta separadora e as
    regiões de decisão. O cálculo de f(x) deve continuar sendo feito pelos
    módulos do projeto, sem numpy.linalg.

O matplotlib deve ser importado apenas dentro de ``plotar`` para que o
treinamento e os testes funcionem mesmo sem a biblioteca instalada.
"""


def plotar(
    pontos,
    rotulos,
    w,
    novos=None,
    titulo="Classificador linear - mínimos quadrados",
    salvar_em=None,
):
    """Desenha pontos de treino, reta separadora e regiões de decisão.

    Parâmetros:
        pontos: lista de pontos de treino [x1, x2].
        rotulos: lista de rótulos +1/-1 na mesma ordem dos pontos.
        w: vetor de pesos [w1, w2, w0].
        novos: lista opcional de pontos novos a destacar.
        titulo: título do gráfico.
        salvar_em: caminho da imagem. Se None, abre a janela.

    Contrato:
        - Colorir as duas regiões conforme o sinal de f(x).
        - Desenhar a reta f(x) = 0, inclusive no caso vertical (w2 ≈ 0).
        - Destacar os pontos novos com marcador diferente e informar a
          classe prevista.
        - Salvar em arquivo quando ``salvar_em`` for informado e retornar
          o caminho; caso contrário, abrir a janela e retornar None.
        - Importar matplotlib dentro da função e lançar RuntimeError com
          instrução de instalação se ele não estiver disponível.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar grafico.plotar(...)."
    )
