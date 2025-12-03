import pandas as pd
import matplotlib.pyplot as plt
class SerieDecomposer():
    def __init__(self, data:pd.Series):
        if isinstance(data, pd.Series):
            try:
                self.serie = data
                print(f'Serie {self.serie.name} carregada com sucesso')
            except ValueError as e:
                return {f'Erro: {e}'}
    def sazo(self):
        sazo = self.serie.diff() # calculando sazonalidade
        plt.figure(figsize=(10,5))
        plt.title(f'Comportamento sazonal do {self.serie.name} - IPCA')
        plt.plot(sazo, color='fuchsia', label='Sazonalidade - IPCA')
        plt.legend()
        plt.tight_layout()
        plt.show()
    def move_avg(self, window:int):
        move_avg = self.serie.rolling(window).mean()
        plt.figure(figsize=(10,5))
        plt.title(f'Media movel da serie {self.serie.name} em relaçao a serie original')
        plt.plot(self.serie, color='red', label='IPCA')
        plt.plot(move_avg, color='blue', label=f'Media Movel | Janela (dias): {window}')
        plt.legend()
        plt.tight_layout()
        plt.show()