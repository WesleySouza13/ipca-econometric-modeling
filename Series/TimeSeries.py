# %% 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Series'))
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import seaborn as sns
from analytics.SerieDecomposition import SerieDecomposer
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
from FourierTransform import Fft
# %% 
data_path = os.path.join('..', 'data', 'serie_IPCA_Janeiro_2000_a_outubro_2025.parquet')
df = pd.read_parquet(data_path)
display(df)
# %%
plt.figure(figsize=(10,5))
plt.title('indice nacional de preços ao consumidor amplo (IPCA)')
plt.plot(df['valor'], label='IPCA', color='red')
plt.legend()
# %%
obj = SerieDecomposer(data=df['valor'])

# %%
obj.sazo()
# %%
obj.move_avg(28)
# %%
plt.figure(figsize=(10,5))
plot_acf(df['valor'], lags=28)
plt.title('Autocorrelaçao Serie Valor - IPCA')
plt.xlabel('N Lags')
plt.ylabel('Autocorrelaçao')
plt.tight_layout()
plt.show()
# %%
df['shift'] = df['valor'].shift(1)
residual = (df['valor'] - df['shift'])
print(residual)

# %%
plt.figure(figsize=(10,5))
plt.title('Residuo da serie atrasada')
plt.plot(residual, marker='o', linestyle='None', color='green')
plt.ylabel('variaçao')
plt.xlabel('janelamento')
plt.tight_layout()
plt.show()
# %%
sns.pairplot(df, palette='dark')
# %% 
plt.figure(figsize=(10,5))
plot_acf(residual[1:], lags=28)
plt.title('Autocorrelaçao dos residuos')
plt.tight_layout()
plt.show()
# %%
residual = residual.fillna(0) # coloquei zero onde foi feito o primeiro atrasdo
acorr_ljungbox(residual)
# %%
fft = Fft(df['valor'], fs=620)
fft.fft()
# %%
plt.figure(figsize=(10,5))
plt.title('Distribuiçao dos residuos')
sns.histplot(residual, kde=True, label='residuo')
plt.legend()
plt.show()
# %%
