# %% 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import seaborn as sns
from analytics.SerieDecomposition import SerieDecomposer
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
