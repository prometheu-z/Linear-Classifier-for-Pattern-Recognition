# Classificador Linear Simples para Reconhecimento de Padrões

Atividade Prática de **Vetores, GA e Álgebra Linear** (SPOMVAL) — IFSP, Bacharelado em Sistemas de Informação, Profa. Josceli.

## Descrição

Este projeto implementa, em Python, um classificador linear binário para pontos bidimensionais. A partir de um conjunto de treinamento com duas classes (por exemplo, aprovado/reprovado), o programa encontra a reta que separa os grupos usando o **método dos mínimos quadrados**, resolvendo as equações normais `(XᵀX)w = Xᵀy`.

Com a reta calculada, novos pontos podem ser classificados automaticamente pela posição em relação a ela, usando o **produto interno** entre o vetor de pesos e o ponto. O programa também gera um gráfico com os pontos de treino, a reta separadora e as regiões de decisão.

Toda a parte de álgebra linear (transposta, multiplicação de matrizes, produto interno e resolução de sistemas lineares) é implementada manualmente, sem usar pacotes que resolvam o problema diretamente.

## Integrantes

- Lucas Eduardo
- Gabriel Sampaio
- Vitor Henrique