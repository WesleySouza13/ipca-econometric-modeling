from src.DataEng.DataEng import DataEng
url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/2000&dataFinal=01/01/2025'

obj = DataEng()
data_inicio = '01/01/2000'
obj.load(code=433, start_date=data_inicio)
obj.feature_eng()
obj.to_parquet(name='IPCA')