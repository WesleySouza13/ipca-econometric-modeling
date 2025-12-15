from fastapi import FastAPI
import os
import joblib
from src.DataEng.DataRequests import DataRequest
from datetime import date
import pandas as pd
import statsmodels.api as sm
app = FastAPI()
model_path = os.path.join('OLS.pkl')
model = joblib.load(model_path)

async def get_data(start, end):
    return DataRequest(code=433, start=start, limit=end)
@app.get('/')
def home():
    return {'api:':'no ar'}
@app.post('/inference')
async def inference(start_date:str, end_date:str):
    data = await get_data(start_date, end_date)
    df = pd.DataFrame(data)
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    try:
        df['lag_1'] = df['valor'].shift(1)
        last = df['lag_1'].iloc[-1:].values
        return last
    except Exception as e:
        raise e 