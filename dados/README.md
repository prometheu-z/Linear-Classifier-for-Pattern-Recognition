# Pasta de dados

Arquivos CSV usados pelo classificador. Neste esqueleto, os arquivos
contêm apenas o cabeçalho; os pontos devem ser definidos pelo grupo.

Formato:

```csv
x1,x2,classe
12,85,1
2,40,-1
```

- `x1`, `x2`: características numéricas do ponto.
- `classe`: `1` (classe A) ou `-1` (classe B). Também podem ser aceitos
  `A`/`B`, `aprovado`/`reprovado`, `positivo`/`negativo` e `true`/`false`.
- Linhas iniciadas por `#` são comentários e devem ser ignoradas pelo
  carregador.

## Casos previstos

| Arquivo | Objetivo |
|---|---|
| `caso1.csv` | Dados bem separáveis: ~8–10 pontos, duas nuvens distintas, acurácia esperada de 100%. |
| `caso2.csv` | Dados com sobreposição/ruído: acurácia menor que 100% e um ponto exatamente sobre a reta. |

Depois de preencher os arquivos, calcular os pesos esperados e registrá-los
no relatório e em `testes/executar_testes.py`.
