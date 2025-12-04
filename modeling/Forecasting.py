# %% 
import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modeling'))
from DataEng.DataEng import DataEng
from sklearn.linear_model import LinearRegression
from statsmodels.graphics.tsaplots import plot_acf
import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
from Metrics import Metrics
# %%
# vou usar dados de 2000 até 31/12/2024 para treinar e o restante até a ultima serie para testar
train_start = '01/01/2000'
train_end = '31/12/2024'
# %%
def load_train(start, end):
    eng = DataEng(433,start, end)
    eng.load()
    return eng.feature_eng()

def load_test(start, end):
    eng = DataEng(433, start, end)
    eng.load()
    return eng.feature_eng()
# %%
train = load_train(train_start, train_end)
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
model = LinearRegression(n_jobs=1000).fit(X_train, y_train)
pred_train = model.predict(X_train)
# %% 
metrics = Metrics(pred_train, y_train).metrics()
metrics
# %%

