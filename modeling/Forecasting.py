# %% 
import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modeling'))
from DataEng.DataEng import DataEng
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
from Metrics import Metrics
import joblib
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, HistGradientBoostingRegressor, RandomForestRegressor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import jarque_bera
import statsmodels.api as sm
# %%
# vou usar dados de 2000 até 31/12/2024 para treinar e o restante até a ultima serie para testar
train_start = '01/01/2000'
train_end = '31/12/2024'
# %%
def load_data(start, end):
    eng = DataEng(433,start, end)
    eng.load()
    return eng.feature_eng()

# %%
train = load_data(train_start, train_end)
train
# %%
for i in range(1, 5):
    col = f'lag_{i}'
    train[col] = train['valor'].shift(i)
# %%
train = train.fillna(0)
train
# %%
sns.pairplot(train)
# %%
def plot_autocorrelation(X:pd.DataFrame):
    if 'data' in X:
        data = X.drop('data', axis=1)
    try: 
        for i in data.columns:
            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10,10))
            for row in axes:
                for ax in row:
                    plot_acf(data[i], ax=ax)
    except Exception as e:
            return {f'erro: {e}'}
            
# %%
plot_autocorrelation(train)
# %%
""""notas: apenas o primeiro lag foi significativo e capaz de passar as informaçoes e variaçoes temporais para o modelo
irei trabalhar apenas com 1 atraso agora, e farei alguns testes
    tirei essas conclusoes fazendo testes de forma separda
"""
X_train = sm.add_constant(train['lag_1'])
y_train = train['valor']
# %% 
model_ols = sm.OLS(y_train, X_train).fit()
print(model_ols.summary())
pred_train = model_ols.predict(X_train)
# %%
plt.figure('Serie real - IPCA X previsto')
plt.figure(figsize=(10,5))
plt.plot(y_train, label='Sinal - IPCA', color='blue')
plt.plot(pred_train, color='red', label='previsao - IPCA')
plt.tight_layout()
plt.legend()
plt.show()
# %%
""""
    irei calcular residuos da previsao e da serie
"""
residual = (y_train-pred_train)
plt.figure(figsize=(10,5))
plt.title('residuo entre a serie real e o previsto')
plt.plot(residual, color='red', marker='o', linestyle='None')
plt.show()
# %%
test_start = '01/01/2025'
test_end = '04/12/2025'
test = load_data(test_start, test_end)
test['lag_1'] = test['valor'].shift(1)
test['lag_1'] = test['lag_1'].fillna(0)
test.isnull().sum()
# %%
X_test = sm.add_constant(test['lag_1'])
y_test = test['valor']
# %%
y_pred = model_ols.predict(X_test)
# %%
print(model_ols.summary())
# %%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste')
plt.plot(y_test, label='IPCA', color='blue')
plt.plot(y_pred, label='previsto', color='red')
plt.tight_layout()
plt.legend()
plt.show()
# %%
residual_test = (y_test-y_pred)
plt.figure(figsize=(10,5))
plt.title('residuo entre o teste e o previsto')
plt.plot(residual_test, color='red', marker='o', linestyle='None')
plt.show()
# %% 

""""
    irei fazer alguns testes com modelos ARMA
    """
    
#  %% 
arima = ARIMA(y_train, order=(1,0,0), seasonal_order=(1,0,1,12), enforce_stationarity=False, enforce_invertibility=False).fit()
# %%
arima_prev_train = arima.predict(start=train.index[0], end=train.index[299])
#%%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste (ARIMA)')
plt.plot(y_train, label='IPCA', color='blue')
plt.plot(arima_prev_train, label='previsto - ARIMA', color='red')
plt.tight_layout()
plt.legend()
plt.show()

# %%
print(arima.summary())
# %%
# busca para paramentros 
auto_arima(train['valor'], seasonal=True, m=12, trace=True)
# %%
arima_prev_test = arima.predict(start=test.index[0], end=test.index[9])
# %%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste (ARIMA)')
plt.plot(y_test, label='IPCA', color='blue')
plt.plot(arima_prev_test, label='previsto - ARIMA', color='red')
plt.tight_layout()
plt.legend()
plt.show()
# %%
arima_path = os.path.join('..', 'ModelArima.pkl')
joblib.dump(arima, arima_path)
# %%

"""vou testar o modelo sarima, que lida melhor com sazonalidade """

# %% 
sarima = SARIMAX(y_train, order=(1,0,0), seasonal_order=(1,0,1,12),
                enforce_stationarity=False, enforce_invertibility=False).fit()
# %%
print(sarima.summary())
# %%
sarima_prev_train = sarima.predict(train.index[0], train.index[299])

# %%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste (SARIMA)')
plt.plot(y_train, label='IPCA', color='blue')
plt.plot(sarima_prev_train, label='previsto - SARIMA', color='red')
plt.tight_layout()
plt.legend()
plt.show()
# %%
sarima_prev_test = sarima.predict(test.index[0], test.index[9])

# %%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste (SARIMA)')
plt.plot(y_test, label='IPCA', color='blue')
plt.plot(sarima_prev_test, label='previsto - SARIMA', color='red')
plt.tight_layout()
plt.legend()
plt.show()

# %%
auto_arima(y_train, seasonal=True, 
        m=12,
        trace=True, 
        stepwise=False)
# %%
sarima.plot_diagnostics(figsize=(12,6))
# %%
print(sarima.summary())
# %%

""""
irei fazer testes com modelos nao lineares comuns """

models = {
    'DecisionTree':DecisionTreeRegressor(random_state=42),
    'AdaBoost': AdaBoostRegressor(random_state=42),
    'HistGradient': HistGradientBoostingRegressor(random_state=42),
    'RandomForest': RandomForestRegressor(random_state=42)
}

#treinando modelos
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(12,9))
axes = axes.flatten()
for idx, (name, model) in enumerate(models.items()):
    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    metrics_obj = Metrics(y_pred_train, y_train)
    metrics_train = metrics_obj.metrics()
    print(f'metricas de treino [{name}]:', metrics_train)
    
    ax = axes[idx]
    ax.set_title(f'{name} - IPCA real x previsto')
    ax.plot(y_train, label='Real (train)', color='blue')
    ax.plot(y_pred_train, label='Previsto (train)', color='red')
    ax.legend()
    
plt.tight_layout()
plt.show()

# %%
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(12,9))
axes = axes.flatten()
for idx, (name, model) in enumerate(models.items()):
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    metrics_obj = Metrics(y_pred_test, y_test)
    metrics_test = metrics_obj.metrics()
    print(f'metricas de teste [{name}]:', metrics_test)

    ax = axes[idx]
    ax.set_title(f'{name} - IPCA real x previsto')
    ax.plot(y_test, label='Real (test)', color='blue')
    ax.plot(y_pred_test, label='Previsto (test)', color='red')
    ax.legend()
plt.tight_layout()
plt.show()

# %%

"""" 
    Mesmo parecendo um modelo mais simples comparado aos outros testados, o modelo de minimos quadrados se mostrou melhor em captar as variaçoes dos dados
    Fiz testes como modelos do tipo ARMA e modelo de machine learning convencionais, e, mesmo com a diferença de robustez matematica e computacional, o OLS trouxe maior confiabilidade em suas previsoes
    ainda com um R^2 baixo, porem, comum no tipo de dado que estamos trabalhando. Com isso, devo seguir com o estudo em cima desse modelo"""
# %%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste')
plt.plot(y_test, label='IPCA', color='blue', marker='o', linestyle='none')
plt.plot(y_pred, label='previsto', color='red', marker='o', linestyle='none')
plt.tight_layout()
plt.legend()
plt.show()
# %%
residual_test_ols = y_pred_test - y_test
plt.figure(figsize=(10,8))
plt.title('Residuos da previsao - OLS')
sns.histplot(residual_test_ols, kde=True, label=f'media: {residual_test_ols.mean()} | std: {residual_test_ols.std()}')
plt.legend()
plt.grid()
plt.show()
# %%
#teste de heterocedasticidade para verivicar se os residuos nao é constante 
def heteroscedasticity(residual: float, X:pd.Series):
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(residual, X, robust=True)
    out = {
        'lm_stats':lm_stat, 
        'lm_pvalue':lm_pvalue,
        'f_stat': f_stat,
        'f_pvalue': f_pvalue
        }
    return pd.DataFrame([out])
        

# %%
heteroscedasticity(residual_test_ols, X_test)
# %%
plt.figure(figsize=(10,8))
plot_acf(residual_test_ols)
plt.title('autocorrelaçao dos residuos - Previsao OLS')

# %%
def normal_test(residual_test:float):
    jb_stat, pvalue_j, skew, kurt = jarque_bera(residual_test)
    out = {
        'pvalue': pvalue_j,
        'jb_stat':jb_stat, 
        'skew':skew,
        'kurt':kurt
    }
    plt.figure(figsize=(10,8))
    sm.qqplot(residual_test, line='45')
    print(out)
# %%
normal_test(residual_test_ols)
# %%
