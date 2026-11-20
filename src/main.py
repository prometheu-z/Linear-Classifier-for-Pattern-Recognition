"""Interface de linha de comando do classificador linear."""
import argparse
import os
import sys

PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_RAIZ = os.path.dirname(PASTA_SRC)
if PASTA_SRC not in sys.path:
    sys.path.insert(0, PASTA_SRC)

import dados
import matriz
import solver
import classificador
import grafico

DADOS_PADRAO = os.path.join(PASTA_RAIZ, "dados", "caso1.csv")
GRAFICO_PADRAO = os.path.join(PASTA_RAIZ, "resultados", "grafico.png")


def normalizar_caminho(caminho):
    """Resolve caminhos relativos a partir da raiz do repositório."""
    if not os.path.isabs(caminho):
        caminho = os.path.join(PASTA_RAIZ, caminho)
    return os.path.abspath(caminho)


def gerar_resumo(w, pontos, rotulos, novos, nome_caso):
    """Formata e salva o relatório técnico solicitado pelo edital."""
    X = classificador.montar_X(pontos)
    XT = matriz.transposta(X)
    A = matriz.multiplicar(XT, X)
    y = [float(rotulo) for rotulo in rotulos]
    b = matriz.matriz_vetor(XT, y)
    _, determinante = solver.resolver_sistema(A, b)
    avaliacao = classificador.avaliar_modelo(w, pontos, rotulos)
    n_hat = matriz.versor([w[0], w[1]])

    linhas = []
    linhas.append("RELATORIO TECNICO - {}".format(nome_caso))
    linhas.append("=" * 72)
    linhas.append("Matriz X^T X:")
    for linha in A:
        linhas.append("  " + str(["{:+.6f}".format(v) for v in linha]))
    linhas.append("Vetor X^T y:")
    linhas.append("  " + str(["{:+.6f}".format(v) for v in b]))
    linhas.append("Determinante(X^T X): {:.12e}".format(determinante))
    linhas.append("Pesos w = [w1, w2, w0]^T:")
    linhas.append("  " + str(["{:+.9f}".format(v) for v in w]))
    linhas.append("Equacao: " + classificador.equacao_reta(w))
    linhas.append("Normal unitario n_hat: [{:+.9f}, {:+.9f}]".format(n_hat[0], n_hat[1]))
    linhas.append("SSE: {:.9f}".format(avaliacao["sse"]))
    linhas.append("RMSE: {:.9f}".format(avaliacao["rmse"]))
    linhas.append("")
    linhas.append("Matriz de confusao:")
    conf = avaliacao["matriz_confusao"]
    linhas.append("  VP={VP}  VN={VN}  FP={FP}  FN={FN}".format(**conf))
    linhas.append("Acuracia={:.2f}%  Precisao={:.2f}%  Recall={:.2f}%".format(
        avaliacao["acuracia"], avaliacao["precisao"], avaliacao["recall"]))
    linhas.append("")
    linhas.append("Pontos de teste:")
    linhas.append("  x1\t\tx2\t\tf(x)\t\td\t\tProjecao\t\tClasse")
    for ponto in novos:
        score = classificador.decisao(w, ponto)
        distancia = classificador.distancia_reta(w, ponto)
        proj = classificador.projetar_na_reta(w, ponto)
        rotulo, nome = classificador.classificar(w, ponto)
        linhas.append("  {:.6f}\t{:.6f}\t{:+.6f}\t{:+.6f}\t({:+.6f}, {:+.6f})\t{}"
                      .format(ponto[0], ponto[1], score, distancia,
                              proj[0], proj[1], nome))
    return "\n".join(linhas)


def main():
    """Orquestra leitura, treino, classificação e geração do painel."""
    parser = argparse.ArgumentParser(description="Classificador linear por mínimos quadrados")
    parser.add_argument("--dados", default=DADOS_PADRAO,
                        help="Caminho do CSV de treinamento")
    parser.add_argument("--novo", action="append", default=[],
                        help="Ponto de teste no formato x1,x2")
    parser.add_argument("--nao-interativo", action="store_true",
                        help="Não solicita pontos pelo teclado")
    parser.add_argument("--mostrar", action="store_true",
                        help="Mostra o gráfico após gerar o arquivo")
    parser.add_argument("--sem-grafico", action="store_true",
                        help="Não gera gráfico")
    args = parser.parse_args()

    try:
        caminho_dados = normalizar_caminho(args.dados)
        pontos, rotulos = dados.carregar_csv(caminho_dados)
        w = classificador.treinar(pontos, rotulos)
        novos = []
        for texto in args.novo:
            novos.append(dados.parse_ponto(texto))
        if not novos:
            nome_caso_previo = "Caso 1" if caminho_dados.endswith("caso1.csv") else "Caso 2"
            if nome_caso_previo == "Caso 1":
                novos = [[3.0, 10.0], [3.0, 2.0]]
            else:
                x_fronteira = 3.0
                y_fronteira = classificador.coordenada_x2(w, x_fronteira)
                novos = [[3.0, 9.0], [6.0, 1.0], [x_fronteira, y_fronteira]]

        if not args.nao_interativo:
            print("Digite pontos no formato x1,x2. Enter vazio encerra.")
            while True:
                try:
                    entrada = input("> ").strip()
                except EOFError:
                    break
                if not entrada:
                    break
                try:
                    novos.append(dados.parse_ponto(entrada))
                except ValueError as erro:
                    print("Erro:", erro)

        avaliacao = classificador.avaliar_modelo(w, pontos, rotulos)
        nome_caso = "Caso 1" if caminho_dados.endswith("caso1.csv") else "Caso 2"
        resumo = gerar_resumo(w, pontos, rotulos, novos, nome_caso)
        print(resumo)

        pasta_resultados = os.path.join(PASTA_RAIZ, "resultados")
        os.makedirs(pasta_resultados, exist_ok=True)
        nome_saida = "resumo_{}.txt".format("caso1" if nome_caso == "Caso 1" else "caso2")
        with open(os.path.join(pasta_resultados, nome_saida),
                  "w", encoding="utf-8") as arquivo:
            arquivo.write(resumo)

        for indice, ponto in enumerate(novos, start=1):
            rotulo, nome_classe = classificador.classificar(w, ponto)
            print("Teste {}: f(x)={:+.6f}, classe={}, d={:+.6f}"
                  .format(indice, classificador.decisao(w, ponto),
                          nome_classe, classificador.distancia_reta(w, ponto)))

        if not args.sem_grafico:
            destino = os.path.join(pasta_resultados,
                                   "painel_{}.png".format(
                                       "caso1" if nome_caso == "Caso 1" else "caso2"))
            grafico.plotar_analise_completa(
                pontos, rotulos, w, novos,
                titulo="{} - Classificador linear".format(nome_caso),
                salvar_em=destino)
            print("Grafico salvo em:", destino)
            if args.mostrar:
                print("Modo --mostrar: gráfico salvo em PNG; janela não aberta em modo automático.")
        return 0
    except (OSError, ValueError, RuntimeError) as erro:
        print("Erro:", erro)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
