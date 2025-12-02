import requests
import pandas as pd
import os
class DataEng():
    def load(self, code:int, start_date:str):
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json&dataInicial={start_date}&dataFinal=01/01/2025'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                self.data = response.json()
                print('carregando dados')
                print(f'requisiçao bem sucedida: {response.status_code} | {response.text}')
                return self.data
            except Exception as e:
                print(f'Erro: {e} |  {response.status_code} | {response.text}')
                return None
    def feature_eng(self):
        json = self.data
        self.df = pd.DataFrame(json)
        if 'data' in self.df:
            try:
                self.df['data'] = pd.to_datetime(self.df['data'])
            except ValueError as value_e:
                print(f'Erro: {value_e}')
                return None
        if 'valor' in self.df:
            try:
                self.df['valor'] = pd.to_numeric(self.df['valor'], errors='coerce')
            except ValueError as value_e:
                print(f'Erro: {value_e}')
                return None
        return self.df
    def to_parquet(self, name: str):
        basedir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(basedir,'..', '..', 'data', f'serie_{name}.parquet')
        return self.df.to_parquet(data_path)
