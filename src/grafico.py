"""Painel visual duplo do classificador linear."""
import os
import sys

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
if PASTA_SRC not in sys.path:
    sys.path.insert(0, PASTA_SRC)

import classificador
import matriz


def plotar(pontos, rotulos, w, novos=None,
           titulo="Classificador linear - mínimos quadrados",
           salvar_em=None):
    """Gera painel 2D com mapa de decisão, vetor normal e perfil de scores."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("Matplotlib não está instalado. Execute: pip install -r requirements.txt")

    w = [float(valor) for valor in w]
    novos = novos or []
    todos_x1 = [p[0] for p in pontos] + [p[0] for p in novos]
    todos_x2 = [p[1] for p in pontos] + [p[1] for p in novos]
    margem_x = max(1.0, (max(todos_x1) - min(todos_x1)) * 0.18)
    margem_y = max(1.0, (max(todos_x2) - min(todos_x2)) * 0.18)
    x_min, x_max = min(todos_x1) - margem_x, max(todos_x1) + margem_x
    y_min, y_max = min(todos_x2) - margem_y, max(todos_x2) + margem_y

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    grade = 220
    xs = [x_min + (x_max - x_min) * i / (grade - 1) for i in range(grade)]
    ys = [y_min + (y_max - y_min) * i / (grade - 1) for i in range(grade)]
    zs = [[classificador.decisao(w, [xs[j], ys[i]]) for j in range(grade)]
          for i in range(grade)]
    ax1.contourf(xs, ys, zs, levels=16, cmap="RdBu_r", alpha=0.78)

    if abs(w[1]) > 1e-12:
        x_reta = [x_min, x_max]
        y_reta = [classificador.coordenada_x2(w, x) for x in x_reta]
        y_meta_mais = [-(w[0] * x + w[2] - 1.0) / w[1] for x in x_reta]
        y_meta_menos = [-(w[0] * x + w[2] + 1.0) / w[1] for x in x_reta]
    else:
        x_reta = [-w[2] / w[0], -w[2] / w[0]]
        y_reta = [y_min, y_max]
        y_meta_mais = y_meta_menos = None
    ax1.plot(x_reta, y_reta, "k-", linewidth=2.2, label="f(x)=0")
    if y_meta_mais is not None:
        ax1.plot(x_reta, y_meta_mais, "k--", linewidth=1.0, alpha=0.7, label="f(x)=+1")
        ax1.plot(x_reta, y_meta_menos, "k--", linewidth=1.0, alpha=0.7, label="f(x)=-1")

    avaliacao = classificador.avaliar_modelo(w, pontos, rotulos)
    errados = set(avaliacao["indices_errados"])
    for classe, marcador, cor in ((1, "o", "#1565c0"), (-1, "s", "#ef6c00")):
        indices = [i for i, r in enumerate(rotulos) if r == classe]
        ax1.scatter([pontos[i][0] for i in indices], [pontos[i][1] for i in indices],
                    marker=marcador, s=70, c=cor, edgecolors="white",
                    linewidths=0.8, label="Treino {}".format("+1" if classe == 1 else "-1"))
    for i in errados:
        ax1.scatter(pontos[i][0], pontos[i][1], s=180, facecolors="none",
                    edgecolors="red", linewidths=2.0)

    for i, ponto in enumerate(novos):
        proj = classificador.projetar_na_reta(w, ponto)
        ax1.scatter(ponto[0], ponto[1], marker="*", s=220, c="gold",
                    edgecolors="black", linewidths=0.7, zorder=5)
        ax1.plot([ponto[0], proj[0]], [ponto[1], proj[1]], "k:",
                 linewidth=1.3, zorder=4)
        distancia = classificador.distancia_reta(w, ponto)
        ax1.annotate("T{} d={:+.3f}".format(i + 1, distancia),
                     (ponto[0], ponto[1]), xytext=(7, 7),
                     textcoords="offset points", fontsize=8)

    n_hat = matriz.versor([w[0], w[1]])
    ponto_normal = [(x_min + x_max) / 2.0,
                    (y_min + y_max) / 2.0]
    if abs(w[1]) > 1e-12:
        ponto_normal[1] = classificador.coordenada_x2(w, ponto_normal[0])
    escala = min(x_max - x_min, y_max - y_min) * 0.10
    ax1.annotate("", xy=(ponto_normal[0] + escala*n_hat[0],
                         ponto_normal[1] + escala*n_hat[1]),
                 xytext=ponto_normal,
                 arrowprops=dict(arrowstyle="->", color="black", lw=2))

    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    ax1.set_xlabel("x1")
    ax1.set_ylabel("x2")
    ax1.set_title("Geometria do classificador")
    ax1.grid(True, alpha=0.18)
    ax1.legend(loc="best", fontsize=8)

    indices = list(range(len(pontos)))
    scores_treino = [classificador.decisao(w, ponto) for ponto in pontos]
    scores_teste = [classificador.decisao(w, ponto) for ponto in novos]
    ax2.scatter(indices, scores_treino, c=[rotulos[i] for i in indices],
                cmap="RdBu_r", s=60, edgecolors="black")
    deslocamento = len(pontos)
    ax2.scatter([deslocamento + i for i in range(len(novos))], scores_teste,
                marker="*", s=180, c="gold", edgecolors="black")
    ax2.axhline(0, color="black", linewidth=2, label="Fronteira f=0")
    ax2.axhline(1, color="gray", linestyle="--", linewidth=1, label="Metas ±1")
    ax2.axhline(-1, color="gray", linestyle="--", linewidth=1)
    ax2.fill_between([-1, deslocamento + max(1, len(novos))], -1, 1,
                     color="yellow", alpha=0.12, label="Zona de ambiguidade")
    ax2.set_xlim(-1, deslocamento + max(1, len(novos)))
    ax2.set_xlabel("Índice da amostra (treino + teste)")
    ax2.set_ylabel("Score f(x)")
    ax2.set_title("Perfil de scores")
    ax2.grid(True, alpha=0.25)
    ax2.legend(loc="best", fontsize=8)

    fig.suptitle(titulo)
    fig.tight_layout()
    if salvar_em:
        destino = os.path.abspath(salvar_em)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        fig.savefig(destino, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return destino
    import matplotlib.pyplot as plt
    plt.show()
    plt.close(fig)
    return None


def plotar_analise_completa(pontos, rotulos, w, novos=None,
                            titulo="Classificador linear",
                            salvar_em=None):
    """Nome público solicitado pelo RFC para o painel analítico completo."""
    return plotar(pontos, rotulos, w, novos, titulo, salvar_em)
