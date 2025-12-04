from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import pandas as pd
class Metrics():
    def __init__(self, y_pred, y_true):
        self.y_pred = y_pred
        self.y_true = y_true
    def metrics(self):
        out_metrics = {
            'R²': r2_score(self.y_true, self.y_pred),
            'MAE': mean_absolute_error(self.y_true, self.y_pred),
            'MSE': mean_squared_error(self.y_true, self.y_pred),
            'MAPE(%)': (mean_absolute_percentage_error(self.y_true, self.y_pred)*100)
        }
        return pd.DataFrame([out_metrics])