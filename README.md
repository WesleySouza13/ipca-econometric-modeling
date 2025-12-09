## Estimação de valores para o sinal de IPCA aplicando métodos de Minimos Quadrados

Este trabalho tem como objetivo avaliar o comportamento temporal da série do IPCA no Brasil, aplicando conceitos econométricos para a desconvolução e previsão do sinal. O estudo utiliza dados reais fornecidos pela API do SGS (Sistema Gerenciador de Séries Temporais), mantido pelo Banco Central do Brasil.

A série do IPCA permite compreender as variações e o comportamento do índice de preços ao consumidor no país. Nesse contexto, torna-se relevante desenvolver um modelo capaz de prever, ou ao menos estimar, o comportamento desse indicador.

# Comportamento do Sinal

Optou-se por trabalhar com a série temporal compreendida entre janeiro de 2000 e outubro de 2025, abrangendo aproximadamente 25 anos de dados. Essa faixa permite analisar o comportamento do índice diante de eventos econômicos e políticos significativos no Brasil, como impeachments, mudanças de governos, crises financeiras, pandemia e quedas na bolsa de valores, entre outros. Com base nesse contexto, é possível observar certa volatilidade na série, a qual será discutida ao longo deste estudo.

Estaremos explorando a coluna "valor", que será o alvo do estudo

# Série:
<img width="837" height="450" alt="image" src="https://github.com/user-attachments/assets/6b1c90fd-d1f7-4bb6-8b07-c21813c2a777" />

# Sazonalidade 

<img width="984" height="484" alt="image" src="https://github.com/user-attachments/assets/84ac5994-5e15-45af-b0eb-3d8d676a4157" />

# Média Movel 

<img width="988" height="486" alt="image" src="https://github.com/user-attachments/assets/ba59e5ac-80ac-46b5-b41c-88c2c050c0b2" />

Pelo próprio sinal, observa-se um comportamento esperado: volatilidade. Essa característica se confirma a partir das variações evidenciadas no gráfico de sazonalidade, indicando que a série não é estacionária, ou seja, seus padrões de comportamento variam ao longo do tempo e entre ciclos.

O gráfico de média móvel com janela de 28 dias, escolhida para ilustrar o comportamento mensal da série, revela pequenas flutuações ao longo do tempo. Isso demonstra que o sinal é fortemente influenciado por mudanças durante os ciclos, reforçando a presença de variabilidade temporal significativa.

# Autocorrelação 

  <img width="628" height="469" alt="image" src="https://github.com/user-attachments/assets/e26facc6-8ae9-46b6-80de-a9793b3df2f0" />
Analisando o gráfico de autocorrelação, observa-se o que já havia sido identificado anteriormente: a série não apresenta constância temporal, mas sim variações ao longo do tempo. Essas características devem ser consideradas, pois impactam diretamente a capacidade do modelo de lidar com mudanças e flutuações nos dados.
Optou-se por não tratar os ciclos e diferenças temporais, com o objetivo de treinar o modelo utilizando os dados em seu estado original, assumindo, consequentemente, a presença de erros de estimativa e menor variabilidade nas previsões.

# Aplicação da Transformada de Fourier para desconvolução do sinal

Para visualizar e analisar os picos presentes na série, aplicou-se a Transformada de Fourier ao sinal. Dessa forma, é possível reduzir o ruído e identificar apenas os picos mais significativos. Observa-se que os picos correspondem às componentes de maior energia do sinal, permitindo destacar os ciclos mais relevantes e suas variações ao longo do tempo.

Sinal decomposto: 

<img width="985" height="388" alt="image" src="https://github.com/user-attachments/assets/30e800f1-82df-4f60-852c-a88882aebf6f" />

Frequências Significativas: 

<img width="988" height="382" alt="image" src="https://github.com/user-attachments/assets/3c9e1575-693e-4842-a05f-d955379ee1d6" />

Observa-se a ocorrência de alguns picos significativos ao longo do tempo, indicando que o índice apresentou variações bruscas em determinados períodos.

# Aplicando Atrasos 

Para trabalhar com previsão em séries temporais, é necessário considerar que o modelo será treinado para prever com base em comportamentos passados. Com esse objetivo, realizou-se um teste de janelamento de ordem 1 sobre o alvo, a fim de comparar a autocorrelação do sinal com o do sinal original e de seus resíduos. Os resultados obtidos foram os seguintes:

<img width="630" height="470" alt="image" src="https://github.com/user-attachments/assets/b8665bbb-43b8-493b-ae2b-7a667447bdb7" />

<img width="496" height="496" alt="image" src="https://github.com/user-attachments/assets/12b24d47-c521-4c7f-b594-83bda83d9f31" />

Repare na distribuição dos residuos: 

<img width="841" height="451" alt="image" src="https://github.com/user-attachments/assets/04029cc7-ea82-44a7-83e0-561de4f1a076" />

Os resíduos obtidos a partir do uso de atrasos apresentam uma distribuição próxima da normal, o que é relevante para a inferência do modelo por diversos motivos. Primeiramente, muitos métodos de regressão, incluindo mínimos quadrados, assumem que os erros seguem uma distribuição normal para que testes estatísticos, como intervalos de confiança e testes de hipótese sobre os coeficientes, sejam válidos. Em segundo lugar, a normalidade dos resíduos indica que o modelo captura adequadamente o padrão central da série mesmo ao considerar os atrasos, sem apresentar viés sistemático ou padrões não modelados. Por fim, resíduos aproximadamente normais permitem que previsões e intervalos de confiança gerados pelo modelo sejam mais confiáveis.

<img width="989" height="490" alt="image" src="https://github.com/user-attachments/assets/b31f778a-4629-4bfc-b7d3-43f50f7ba917" />








