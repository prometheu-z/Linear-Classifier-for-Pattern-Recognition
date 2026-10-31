# Classificador Linear Simples para Reconhecimento de Padrões

Atividade Prática de **Vetores, GA e Álgebra Linear** (SPOMVAL) — IFSP, Bacharelado em Sistemas de Informação, Profa. Josceli.

## Descrição

Este projeto implementará, em Python, um classificador linear binário para pontos bidimensionais. A partir de um conjunto de treinamento com duas classes (por exemplo, aprovado/reprovado), o programa encontrará a reta que separa os grupos usando o **método dos mínimos quadrados**, resolvendo as equações normais `(XᵀX)w = Xᵀy`.

Com a reta calculada, novos pontos poderão ser classificados automaticamente pela posição em relação a ela, usando o **produto interno** entre o vetor de pesos e o ponto. O programa também gerará um gráfico com os pontos de treino, a reta separadora e as regiões de decisão.

Toda a parte de álgebra linear (transposta, multiplicação de matrizes, produto interno e resolução de sistemas lineares) será implementada manualmente, sem usar pacotes que resolvam o problema diretamente.

> **Status atual: esqueleto (scaffold).**
> A arquitetura de pastas e os contratos das funções estão definidos, mas
> os métodos ainda **não foram implementados**. As funções levantem
> `NotImplementedError` com um `TODO` indicando o que falta.

## Integrantes

- Lucas Eduardo
- Gabriel Sampaio
- Vitor Henrique

## Estrutura do repositório

```text
vetores/
├── README.md                  # visão geral, escopo e instruções
├── requirements.txt           # única dependência: matplotlib (gráfico)
├── .gitignore
├── relatorio/
│   ├── LEIA-ME.md             # orientação do que deve ir no PDF
│   └── relatorio.pdf          # (a adicionar) relatório final
├── src/
│   ├── matriz.py              # [esqueleto] transposta, produtos, norma
│   ├── solver.py              # [esqueleto] Gauss com pivotamento parcial
│   ├── classificador.py       # [esqueleto] treino, decisão, classificação
│   ├── dados.py               # [esqueleto] leitura/validação dos CSVs
│   ├── grafico.py             # [esqueleto] pontos + reta + regiões
│   └── main.py                # [esqueleto] CLI
├── dados/
│   ├── README.md              # formato dos CSVs e objetivos dos casos
│   ├── caso1.csv              # cabeçalho + instruções (preencher)
│   └── caso2.csv              # cabeçalho + instruções (preencher)
└── testes/
    └── executar_testes.py     # [esqueleto] testes dos 2 casos
```

## Contratos definidos

As assinaturas seguem a seção 4.4 do documento de requisitos.

| Módulo | Funções |
|---|---|
| `src/matriz.py` | `transposta(A)`, `multiplicar(A, B)`, `matriz_vetor(A, v)`, `produto_interno(u, v)`, `norma(v)` |
| `src/solver.py` | `resolver_sistema(A, b, tolerancia=1e-12)` |
| `src/classificador.py` | `montar_X(pontos)`, `treinar(pontos, rotulos)`, `decisao(w, ponto)`, `classificar(w, ponto)`, `acuracia(w, pontos, rotulos)`, `distancia_reta(w, ponto)`, `equacao_reta(w)`, `coordenada_x2(w, x1)` |
| `src/dados.py` | `normalizar_rotulo(valor)`, `carregar_csv(caminho)`, `validar_pontos(pontos, rotulos=None)`, `parse_ponto(texto)`, `caminho_caso(numero)`, `carregar_caso(numero)` |
| `src/grafico.py` | `plotar(pontos, rotulos, w, novos=None, titulo=..., salvar_em=None)` |
| `src/main.py` | `main()` |
| `testes/executar_testes.py` | `testar_algebra_linear()`, `testar_caso1()`, `testar_caso2()`, `main()` |

Cada função contém docstring com parâmetros, retorno e contrato. As
implementações devem preservar essas assinaturas.

## Modelo matemático planejado

- Matriz aumentada `X` (m × 3): cada linha é `[x1, x2, 1]`.
- Vetor de rótulos `y` (m × 1): `+1` ou `-1`.
- Pesos `w = [w1, w2, w0]ᵀ`.
- Equações normais: `(XᵀX)w = Xᵀy`, resolvidas por eliminação de Gauss.
- Decisão: `f(x) = w1·x1 + w2·x2 + w0 = w · [x1, x2, 1]`.
- Classificação: `f(x) ≥ 0 → +1`; caso contrário `−1`.
- `(w1, w2)` é o vetor normal à reta; `f(x) / ‖(w1, w2)‖` é a distância
  com sinal do ponto à reta.

## Formato dos dados

```csv
x1,x2,classe
12,85,1
2,40,-1
```

- `x1`, `x2`: características numéricas do ponto.
- `classe`: `+1`/`-1` (ou `A`/`B`, `aprovado`/`reprovado`).
- Linhas iniciadas por `#` são comentários e devem ser ignoradas.

Os arquivos `dados/caso1.csv` e `dados/caso2.csv` estão apenas com
cabeçalho e instruções; os pontos ainda devem ser definidos pelo grupo.

## Interface prevista

Depois da implementação, a execução será:

```bash
pip install -r requirements.txt

# Caso 1 (padrão), modo interativo
python src/main.py

# Caso 2
python src/main.py --dados dados/caso2.csv

# Classificar pontos direto pela linha de comando
python src/main.py --novo "13,90" --novo "2,30"

# Não pedir pontos pelo teclado
python src/main.py --nao-interativo

# Abrir a janela do gráfico em vez de salvar
python src/main.py --mostrar

# Apenas treinar/classificar, sem gráfico
python src/main.py --sem-grafico

# Testes automáticos
python testes/executar_testes.py
```

Por padrão, o gráfico será salvo em `grafico_resultado.png`.

## Próximos passos

- [ ] Definir os datasets `caso1.csv` e `caso2.csv`.
- [ ] Implementar `src/matriz.py` e `src/solver.py`.
- [ ] Implementar `src/classificador.py` e validar o Caso 1 à mão.
- [ ] Implementar `src/dados.py`, `src/grafico.py` e `src/main.py`.
- [ ] Preencher `testes/executar_testes.py` com os valores esperados.
- [ ] Redigir o relatório e salvar em `relatorio/relatorio.pdf`.
- [ ] Revisar o checklist final do documento de requisitos.

## Relatório

O PDF final deve ser colocado em `relatorio/relatorio.pdf`. A estrutura
sugerida está em `relatorio/LEIA-ME.md`, conforme a seção 4.6 do documento
de requisitos.
