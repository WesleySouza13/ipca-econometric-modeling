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

# %%
drop_cols = ['data', 'valor']
X_train = train.drop(drop_cols, axis=1)
y_train = train['valor']
# %%
model = sm.OLS(y_train, X_train).fit()
print(model.summary())
pred_train = model.predict(X_train)
# %% 
metrics = Metrics(pred_train, y_train).metrics()
metrics
# %%
plt.plot(train['valor'], color='red', label='sinal real')
plt.plot(pred_train, color='blue', label='predict-train')
plt.legend()
# %%
""""notas: apenas o primeiro lag foi significativo e capaz de passar as informaçoes e variaçoes temporais para o modelo
irei trabalhar apenas com 1 atraso agora, e farei alguns testes"""

X_train = X_train['lag_1']
X_train
# %% 
model = sm.OLS(y_train, X_train).fit()
print(model.summary())
new_pred_train = model.predict(X_train)
# %%
plt.figure('Serie real - IPCA X previsto')
plt.figure(figsize=(10,5))
plt.plot(y_train, label='Sinal - IPCA', color='blue')
plt.plot(new_pred_train, color='red', label='previsao - IPCA')
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
X_test = test['lag_1']
y_test = test['valor']
# %%
y_pred = model.predict(X_test)
# %%
print(model.summary())
# %%
plt.figure(figsize=(10,5))
plt.title('Serie real - IPCA X previsto teste')
plt.plot(X_test, label='IPCA', color='blue')
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
metrics_test = Metrics(y_pred, y_test).metrics()
print(metrics_test)
# %%
