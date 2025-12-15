import streamlit as st
from src.DataEng.DataRequests import DataRequest
import pandas as pd
import plotly.express as px
from datetime import date
from model.TrainPred import train_pred
#from src.analytics.SerieDecomposition import SerieDecomposer

st.set_page_config(page_title='Modelagem IPCA', page_icon='📈') # talvez eu mude o titulo da pg

st.markdown("""
            # Bem vindo(a)!
            
            Essa solução foi modelada por Wesley de Souza Matos para estimar valores do Indice de Preços do Consumidor Aberto (IPCA)
            
            Sinta-se a vontade para usar essa aplicação, entrar em contato comigo pelo Linkedin ou dar fork pelo Github!
            """)
st.text('Entre em contato ou dê fork no Github!')
link_linkedin = 'https://www.linkedin.com/in/wesley-matos-5a4b84254/'
link_github = 'https://github.com/WesleySouza13'
st.link_button('Linkedin', url=link_linkedin, icon='💼')
st.link_button('Github', link_github, icon='💻')
st.text('Escolha uma data de inicio e uma data de limite para a série:')

start_date = st.date_input(label='Data de Inicio:',min_value='2000-01-01')
limit_date = st.date_input(label='Data Limite: ', max_value='today')
code = 433 # codigo do sinal do IPCA 

def dataframe_req(code, start, limit):
    if start is not None and limit is not None:
        start_form = start.strftime("%d/%m/%Y")
        limit_form = limit.strftime("%d/%m/%Y")
        data = DataRequest(code, start_form, limit_form)
        return pd.DataFrame(data)
    else:
        st.error('Você precisa inserir duas datas!')
df = dataframe_req(code, start_date, limit_date)
# plots de Graficos - Serie
if df is not None and not df.empty:
    #df['data'] = pd.to_datetime(df['data'])
    #df = df.sort_values('data')
    df['valor'] = pd.to_numeric(df['valor']) # a serie estava vindo como 'object'
    #st.write(df['valor'].dtype)
    fig = px.line(data_frame=df, x='data', y='valor',title='Sinal Série - IPCA' )
    fig.update_layout(
        width=500,
        height=350
    )
    st.plotly_chart(fig)

    #serie = df['valor']
# opçao de decomposiçao de serie
    def trend(data:pd.Series, window:int):
        return data.rolling(window).mean()
    
    def sazo(data: pd.Series, periods:int):
        return data.diff(periods)
    option = st.selectbox(
        "O que Você deseja fazer?",
        ('Decompor Serie', 'Prever')
    )
    if option == 'Decompor Serie':
        dec_options = st.selectbox(
            "Qual decomposição você deseja fazer?",
            ('Tendência da Serie', 'Sazonalidade')
        )
        if dec_options == 'Tendência da Serie':
            window_input_trend = st.number_input('Insira o número de janelas para a linha de tendência', min_value=1)
            if window_input_trend:
                trend_ = trend(data=df['valor'], window=window_input_trend)
                fig_trend = px.line(y=trend_,x=df['data'],
                                    labels='Tendencia - IPCA', color_discrete_sequence=['green'], title=f'Tendência - IPCA: Janelamento = {window_input_trend}')
                fig_trend.update_layout(
                    width=500,
                    height=350
                )
                st.plotly_chart(fig_trend)
        if dec_options == 'Sazonalidade':
            window_input_sazo = st.number_input('Deseja calcular a Sazonalidade em quantos periodos?', min_value=1)
            if window_input_sazo:
                sazo_ = sazo(data=df['valor'], periods=window_input_sazo)
                fig_sazo = px.line(y=sazo_, x=df['data'], labels=f'Sazonalidade - IPCA: periodos = {window_input_sazo}', 
                                color_discrete_sequence=['orange'], title=f'Sazonalidade - IPCA: Periodos = {window_input_sazo}')
                fig_sazo.update_layout(
                    width=500,
                    height=350
                )
                st.plotly_chart(fig_sazo)
    if option == 'Prever':
        window_pred_1 = st.date_input('janelamento para previsão [inicio]', min_value='2000-01-01')
        window_pred_2 = st.date_input('janelamento para previsão [final]', min_value='2001-01-01')
        if window_pred_1 and window_pred_2:
            st.text(f'Você irá infererir sobre a janela de {window_pred_1} e {window_pred_2}')
            data_value = dataframe_req(code=code, start=window_pred_1, limit=window_pred_2)
            if data_value.empty:
                st.text('Escolha uma janelamento válido!')
            else:
                st.dataframe(data_value)
                st.text('Iniciando inferencia:')
                st.text('Nota: Quanto maior a janela para a inferencia, melhores serão as previsões do modelo. Com isso, escolha um melhor janelamento. ')
                model = train_pred(data_value).fit()
                st.text(model.inference())
            