"""Testes automáticos do projeto (ESQUELETO).

Estrutura prevista:
    1. Testar as operações de matrizes e o solver.
    2. Testar o Caso 1 (dados bem separáveis).
    3. Testar o Caso 2 (dados com sobreposição/ruído).

Os testes devem comparar os resultados obtidos com valores calculados e
documentados pelo grupo (não inventar valores esperados).

Uso previsto (a partir da raiz do projeto):
    python testes/executar_testes.py
"""

import os
import sys

# Garante que os módulos de src/ possam ser importados quando este arquivo
# for executado diretamente.
PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SRC = os.path.join(PASTA_RAIZ, "src")
if PASTA_SRC not in sys.path:
    sys.path.insert(0, PASTA_SRC)


def testar_algebra_linear():
    """Testa transposta, produtos, norma e o solver de Gauss.

    Contrato:
        - Verificar resultados conhecidos das funções de matriz.
        - Verificar que o solver resolve um sistema 2x2 simples.
        - Verificar que uma matriz singular gera ValueError.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar testes.testar_algebra_linear()."
    )


def testar_caso1():
    """Testa o Caso 1 (dados bem separáveis).

    Contrato:
        - Carregar dados/caso1.csv após preencher o dataset.
        - Treinar e conferir os pesos esperados.
        - Conferir acurácia de treino (esperado: 100%).
        - Conferir a classificação de pelo menos dois pontos novos.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar testes.testar_caso1()."
    )


def testar_caso2():
    """Testa o Caso 2 (dados com sobreposição/ruído).

    Contrato:
        - Carregar dados/caso2.csv após preencher o dataset.
        - Conferir que a acurácia é menor que 100%.
        - Documentar/verificar o ponto classificado incorretamente.
        - Verificar um ponto sobre a reta (f(x) = 0) e a regra de
          desempate (+1).

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar testes.testar_caso2()."
    )


def main():
    """Executa todos os testes e retorna 0 (sucesso) ou 1 (falha).

    Contrato:
        - Chamar os três grupos de teste.
        - Exibir um resumo com total de verificações e falhas.
        - Retornar o código de saída adequado.

    TODO: implementar.
    """
    raise NotImplementedError(
        "TODO: implementar testes.main()."
    )


if __name__ == "__main__":
    raise SystemExit(main())
