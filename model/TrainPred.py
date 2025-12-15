from statsmodels.regression.linear_model import OLS
import pandas as pd
import statsmodels.api as sm
from modeling.Metrics import Metrics
class train_pred:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.data['valor'] = pd.to_numeric(self.data['valor'], errors='coerce')
        self.data = self.data.dropna()
        self.model = None

    def fit(self):
        df = self.data.copy()
        df['lag_1'] = df['valor'].shift(1)
        df = df.dropna()
        X = sm.add_constant(df['lag_1'])
        y = df['valor']
        self.model = OLS(y, X).fit()
        return self

    def inference(self):
        if self.model is None:
            raise RuntimeError("Modelo não treinado")
        last_value = float(self.data['valor'].iloc[-1])
        exog_names = self.model.model.exog_names
        X_last = pd.DataFrame(
            [[1.0, last_value]],
            columns=exog_names
        )
        return float(self.model.predict(X_last).iloc[0])
    def metrics(self):
        return self.model.summary()
