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


class Terminal:
    """Cores simples e seguras para melhorar a leitura da saída."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"

    @staticmethod
    def habilitar_cor():
        if os.environ.get("NO_COLOR"):
            return False
        if hasattr(sys.stdout, "isatty") and not sys.stdout.isatty():
            return False
        if os.name == "nt":
            try:
                import ctypes
                handle = ctypes.windll.kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
                ctypes.windll.kernel32.SetConsoleMode(handle, mode.value | 0x0004)
            except Exception:
                pass
        return True


CORES = Terminal.habilitar_cor()


def cor(texto, codigo):
    if not CORES:
        return texto
    return "{}{}{}".format(codigo, texto, Terminal.RESET)


def titulo(texto):
    print("\n" + cor("[ {} ]".format(texto), Terminal.BOLD + Terminal.CYAN))
    print(cor("-" * (len(texto) + 4), Terminal.CYAN))


def linha_chave_valor(chave, valor):
    print("  {:<16} {}".format(chave + ":", valor))


def tabela(titulo_colunas, linhas):
    """Exibe uma tabela compacta, alinhada e sem caracteres especiais."""
    largura = [len(coluna) for coluna in titulo_colunas]
    for linha in linhas:
        for indice, valor in enumerate(linha):
            largura[indice] = max(largura[indice], len(str(valor)))

    cabecalho = "  ".join(str(valor).ljust(largura[indice])
                          for indice, valor in enumerate(titulo_colunas))
    separador = "-+-".join("-" * tamanho for tamanho in largura)
    print(cor(cabecalho, Terminal.BOLD))
    print(separador)
    for linha in linhas:
        print("  ".join(str(valor).ljust(largura[indice])
                        for indice, valor in enumerate(linha)))


def exibir_resultado_terminal(w, pontos, rotulos, novos, nome_caso, avaliacao,
                              destino_grafico=None):
    """Apresenta o resultado principal em blocos legíveis no terminal."""
    print()
    print(cor("CLASSIFICADOR LINEAR", Terminal.BOLD + Terminal.CYAN))
    print(cor("RESULTADO - {}".format(nome_caso.upper()), Terminal.BOLD))

    titulo("Modelo")
    linha_chave_valor("Equacao", classificador.equacao_reta(w))
    n_hat = matriz.versor([w[0], w[1]])
    linha_chave_valor("Pesos", "[{:+.6f}, {:+.6f}, {:+.6f}]".format(*w))
    linha_chave_valor("Normal", "[{:+.6f}, {:+.6f}]".format(*n_hat))

    titulo("Desempenho")
    conf = avaliacao["matriz_confusao"]
    linha_chave_valor("Acuracia",
                      cor("{:.2f}%".format(avaliacao["acuracia"]), Terminal.GREEN))
    linha_chave_valor("Precisao", "{:.2f}%".format(avaliacao["precisao"]))
    linha_chave_valor("Recall", "{:.2f}%".format(avaliacao["recall"]))
    linha_chave_valor("RMSE", "{:.9f}".format(avaliacao["rmse"]))
    linha_chave_valor("Confusao",
                      "VP {VP} | VN {VN} | FP {FP} | FN {FN}".format(**conf))

    titulo("Pontos de teste")
    linhas = []
    for indice, ponto in enumerate(novos, start=1):
        score = classificador.decisao(w, ponto)
        distancia = classificador.distancia_reta(w, ponto)
        _, nome = classificador.classificar(w, ponto)
        linhas.append((
            "T{}".format(indice),
            "({:+.3f}, {:+.3f})".format(ponto[0], ponto[1]),
            "{:+.6f}".format(score),
            "{:+.6f}".format(distancia),
            nome,
        ))
    tabela(("Teste", "Ponto", "f(x)", "Distancia", "Classe"), linhas)

    if destino_grafico:
        print("\n" + cor("[ OK ]", Terminal.GREEN) + " Grafico salvo em: {}".format(destino_grafico))


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
            print(cor("Entrada de pontos", Terminal.BOLD))
            print("Digite no formato x1,x2. Enter vazio encerra.")
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
                    print(cor("[ ERRO ]", Terminal.RED) + " {}".format(erro))

        avaliacao = classificador.avaliar_modelo(w, pontos, rotulos)
        nome_caso = "Caso 1" if caminho_dados.endswith("caso1.csv") else "Caso 2"
        resumo = gerar_resumo(w, pontos, rotulos, novos, nome_caso)

        pasta_resultados = os.path.join(PASTA_RAIZ, "resultados")
        os.makedirs(pasta_resultados, exist_ok=True)
        nome_saida = "resumo_{}.txt".format("caso1" if nome_caso == "Caso 1" else "caso2")
        with open(os.path.join(pasta_resultados, nome_saida),
                  "w", encoding="utf-8") as arquivo:
            arquivo.write(resumo)

        destino_grafico = None
        if not args.sem_grafico:
            destino = os.path.join(pasta_resultados,
                                   "painel_{}.png".format(
                                       "caso1" if nome_caso == "Caso 1" else "caso2"))
            grafico.plotar_analise_completa(
                pontos, rotulos, w, novos,
                titulo="{} - Classificador linear".format(nome_caso),
                salvar_em=destino)
            destino_grafico = destino
            if args.mostrar:
                print(cor("[ INFO ]", Terminal.YELLOW) +
                      " Modo --mostrar ativo: grafico salvo em PNG.")

        exibir_resultado_terminal(w, pontos, rotulos, novos, nome_caso, avaliacao,
                                  destino_grafico)
        print(cor("[ OK ]", Terminal.GREEN) +
              " Relatorio salvo em: {}".format(os.path.join(pasta_resultados, nome_saida)))
        return 0
    except (OSError, ValueError, RuntimeError) as erro:
        print(cor("[ ERRO ]", Terminal.RED) + " {}".format(erro))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
