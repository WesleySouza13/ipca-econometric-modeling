## Estimação de valores para o sinal de IPCA aplicando métodos de Minimos Quadrados

Este trabalho tem como objetivo avaliar o comportamento temporal da série do IPCA no Brasil, aplicando conceitos econométricos para a desconvolução e a previsão do sinal. O estudo utiliza dados reais fornecidos pela API do SGS (Sistema Gerenciador de Séries Temporais), mantido pelo Banco Central do Brasil.

A série do IPCA permite compreender as variações e o comportamento do índice de preços ao consumidor no país. Nesse contexto, torna-se relevante desenvolver um modelo capaz de prever, ou ao menos estimar, o comportamento futuro desse indicador, dado o seu papel central na formulação de políticas monetárias, na indexação de contratos e na tomada de decisão econômica.

Cálculo do IPCA

O IPCA (Índice Nacional de Preços ao Consumidor Amplo) é calculado mensalmente pelo Instituto Brasileiro de Geografia e Estatística (IBGE) e representa a inflação oficial do país. O índice reflete a variação do custo de vida de famílias com rendimentos mensais entre 1 e 40 salários mínimos, residentes em áreas urbanas.

O cálculo do IPCA baseia-se na coleta sistemática de preços de uma cesta representativa de bens e serviços, organizada em grandes grupos de consumo, tais como Alimentação e Bebidas, Habitação, Transportes, Saúde e Cuidados Pessoais, Educação, entre outros.

De forma resumida, o processo de cálculo ocorre conforme as seguintes etapas:

Definição da cesta de produtos e serviços:
O IBGE define a cesta de consumo a partir da Pesquisa de Orçamentos Familiares (POF), que identifica a estrutura de gastos das famílias brasileiras. Essa cesta é composta por nove grandes grupos de consumo, cujos itens representam os padrões médios de consumo da população-alvo.

Coleta mensal de preços:
A coleta de preços é realizada mensalmente, geralmente entre os dias 1º e 30 de cada mês. Aproximadamente 430 mil preços são coletados em cerca de 30 mil estabelecimentos comerciais, domicílios e prestadores de serviços, distribuídos em 13 regiões metropolitanas e áreas urbanas do país.

Cálculo das variações de preços:
Para cada item da cesta, calcula-se a variação percentual de preços em relação ao período anterior. Essas variações capturam os aumentos ou reduções observados nos preços ao consumidor.

Ponderação dos itens:
As variações de preços são ponderadas de acordo com a importância relativa de cada item no orçamento das famílias, conforme definido pela POF. Grupos como Transportes e Habitação possuem pesos mais elevados, enquanto itens como Comunicação tendem a apresentar menor participação relativa.

Cálculo da média ponderada:
A soma das variações ponderadas resulta no valor final do IPCA do período, que expressa a variação média do custo de vida da população considerada.

Essa metodologia confere ao IPCA uma forte dependência temporal e estrutural, uma vez que o índice é resultado da agregação ponderada de múltiplos subcomponentes com dinâmicas próprias. Essa característica justifica o uso de modelos econométricos e de séries temporais para análise, decomposição e previsão do comportamento do índice ao longo do tempo.

Estaremos explorando a coluna "valor", que será o alvo do estudo

# Aplicação

Para fins de visualização e utilização prática dos resultados obtidos, foi desenvolvida uma aplicação interativa que implementa o modelo econométrico proposto. A aplicação permite a análise do comportamento da série do IPCA e a exploração das previsões geradas pelo modelo de forma acessível e intuitiva.

A aplicação encontra-se disponível publicamente no seguinte endereço:

https://ipca-econometric-modeling-djh2hu2pv8xzkr7acuzg6a.streamlit.app/

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

# Teste de portmanteau - Ljungbox

Para validar estatisticamente minhas hipóteses, apliquei o teste de portmanteau (Ljung-Box no statsmodels), obtendo p-valores consistentemente abaixo do limiar de 5%, o que confirma a presença de dependência temporal e não estacionariedade do sinal. 

<img width="184" height="293" alt="image" src="https://github.com/user-attachments/assets/160d8830-f7d1-4e35-bfb2-0073a8f2ee61" />

# Rodando Modelo de Minimos Quadrados

Foram realizados os primeiros testes utilizando um modelo de Regressao por Minimos Quadrados Ordinarios (OLS). Inicialmente, o desempenho foi insatisfatorio, com um R2 em torno de 0.38.

Diante desse resultado, foram avaliados outros modelos, incluindo abordagens da familia ARMA (ARIMA e SARIMA) e modelos de Machine Learning convencionais. Contudo, ao serem aplicados aos dados, esses modelos nao conseguiram capturar adequadamente as variacoes da serie, apresentando, em alguns casos, R2 negativo, residuos de previsao com comportamento nao normal e outras instabilidades.

Em funcao desses resultados, optou-se por manter o modelo de Minimos Quadrados, apesar do R2 relativamente baixo. Esse problema foi mitigado por meio de uma estrategia de retreinamento dinamico do modelo a cada requisicao, considerando o intervalo de dados definido pelo cliente ou usuario, o que permitiu maior aderencia as caracteristicas locais dos dados.


<img width="749" height="627" alt="image" src="https://github.com/user-attachments/assets/f952a578-dc00-4a06-9f44-45eb7e9d585d" />\

Ao analisar o histograma dos resíduos, vemos que não temos amostras suficientes para determinar se os resíduos seguem uma normalidade, a fim de decidir se o modelo contém heterocedasticidade ou homocedasticidade. Com isso, realizei outros testes para verificar essa propriedade, como testes de hipóteses. Assim, utilizando um nível de confiança de 95%, validei que as previsões seguem a normalidade.

Utilizei um atraso de 1 período para trabalhar nessa série, pois os demais testados (4 atrasos) não apresentaram significância na inferência do modelo. Com isso, trabalhei com um modelo AR de ordem 1.

Seguem as métricas do modelo:


| Variável | Coeficiente | Erro Padrão | Estatística t | P-valor | IC 2.5% | IC 97.5% |
| -------- | ----------- | ----------- | ------------- | ------- | ------- | -------- |
| const    | 0.1866      | 0.029       | 6.487         | 0.000   | 0.130   | 0.243    |
| lag_1    | 0.6223      | 0.045       | 13.678        | 0.000   | 0.533   | 0.712    |


| Métrica          | Valor     |
| ---------------- | --------- |
| Omnibus          | 87.113    |
| Prob (Omnibus)   | 0.000     |
| Jarque-Bera (JB) | 662.415   |
| Prob (JB)        | 1.44e-144 |
| Skew             | 0.954     |
| Kurtosis         | 10.038    |
| Durbin-Watson    | 2.076     |
| Cond. Number     | 3.29      |

Os coeficientes estimados são estatisticamente significativos, indicando que o atraso de um período possui forte influência sobre o valor atual da série, enquanto as estatísticas de diagnóstico sugerem ausência de autocorrelação relevante nos resíduos. Além disso, os testes de Omnibus e Jarque-Bera não são significativos para determinar a não normalidade dos resíduos.







