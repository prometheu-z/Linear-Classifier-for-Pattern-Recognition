"""Interface de linha de comando (ESQUELETO).

Fluxo previsto:
    1. Ler os dados de treinamento de um CSV.
    2. Treinar o classificador (mínimos quadrados / equações normais).
    3. Mostrar pesos, equação da reta e acurácia de treino.
    4. Permitir digitar novos pontos e classificá-los.
    5. Gerar o gráfico com pontos, reta e regiões de decisão.

Interface planejada (a detalhar na implementação):
    python src/main.py
    python src/main.py --dados dados/caso2.csv
    python src/main.py --novo "13,90" --novo "2,30"
    python src/main.py --nao-interativo
    python src/main.py --mostrar
    python src/main.py --sem-grafico

A função ``main`` está apenas definida; a implementação deve orquestrar
os demais módulos, sem recalcular álgebra linear aqui.
"""

import os

# Caminhos padrão previstos.
PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_PADRAO = os.path.join(PASTA_RAIZ, "dados", "caso1.csv")
GRAFICO_PADRAO = os.path.join(PASTA_RAIZ, "grafico_resultado.png")


def main():
    """Executa o fluxo completo do programa.

    Contrato:
        - Ler argumentos da linha de comando (argparse).
        - Carregar e validar o CSV indicado.
        - Treinar o classificador e exibir w, equação e acurácia.
        - Classificar os pontos passados por --novo.
        - Se não estiver em modo não interativo, ler pontos no formato
          x1,x2 até o usuário encerrar.
        - Gerar/salvar o gráfico, salvo quando --sem-grafico for usado.
        - Retornar 0 em caso de sucesso e 1 em caso de erro de entrada.

    TODO: implementar, reutilizando os módulos dados, classificador e
    grafico. Não duplicar cálculos de álgebra linear.
    """
    raise NotImplementedError(
        "TODO: implementar main.main()."
    )


if __name__ == "__main__":
    raise SystemExit(main())
