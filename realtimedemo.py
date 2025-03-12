import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from comum import arquivozip, extrair_arquivos, listar_arquivos,renameVar,convertTypes
import shutil
import os


def app():
    col01, col02 = st.columns(gap='large', spec=[1,1])

    with col01:

        modelo = arquivozip()

        if modelo is not None:
            # 🛠 Apagar e recriar diretórios para evitar arquivos antigos
            temp = "temp"
            caminho_extraido = "arquivosExtraidos"

            shutil.rmtree(temp, ignore_errors=True)
            os.makedirs(temp, exist_ok=True)

            shutil.rmtree(caminho_extraido, ignore_errors=True)
            os.makedirs(caminho_extraido, exist_ok=True)

            # Salvar o ZIP temporariamente
            pastaZip = os.path.join(temp, modelo.name)
            with open(pastaZip, "wb") as f:
                f.write(modelo.getvalue())

            # Extrair os arquivos
            extrair_arquivos(pastaZip, extrair=caminho_extraido)

            csvLista =listar_arquivos(caminho_extraido)
            
            # 🔍 Identificar automaticamente o arquivo CSV dentro da pasta extraída
            csv_files = [f for f in (csvLista) if f.endswith(".csv")]

            if not csv_files:
                st.error("Nenhum arquivo CSV encontrado no ZIP!")
                return
            
            # Considerando que sempre há um único CSV relevante
            caminhoArquivo = csv_files[0]
            
    with col02:
                        # 🛠 Verificar se o CSV pode ser carregado
                            # # Título principal do aplicativo
        st.markdown("<h2 style='text-align: center; color: black;'>Simulação de predição em tempo real</h1>", unsafe_allow_html=True)
        try:
            df = pd.read_csv(caminhoArquivo, sep=';')
            # st.success(f"Arquivo carregado: {csv_files[0]}")
            renameVar(df)
            df['mediaReg'] = df['anomalies']/df['totalReg']*100

        except Exception as e:
            # st.error(f"Erro ao carregar o CSV: {e}")
            return
            
    
    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ # 


    # # Criando duas colunas para seleção de parâmetros
    col03, col04 = st.columns(spec=[1,1])
        
    # # Configuração da coluna esquerda - Parâmetros de entrada do reator
    with col03:
    
        st.markdown("<h4 style='text-align: justify; color: black;'> Variaveis de Saída </h1>", unsafe_allow_html=True)
        entrada = ['EngLoad_RC_All_%','EngRPM_RC_All_%','GndSped_RC_All_%','BaseCutPrs_RC_All_%','BaseCutHght_RC_All_%','ChopperHydPrs_RC_All_%','ChopperRPM_RC_All_%','HydrostatChrgPrs_RC_All_%']
        select_upleft = st.selectbox('', entrada)


    with col04:
        st.markdown("<h4 style='text-align: justify; color: black;'> Variáveis de saída</h1>", unsafe_allow_html=True)
        saida01 = ['EngLoad_Above_%','EngRPM_Above_%','GndSpd_Above_%','BaseCutPrs_Above_%','BaseCutHght_%','ChopperHyd_Above_%','AboveChopperRPM_Above_%','HydrostatChrgPrs_Above_%']         
        select_upright = st.selectbox('', saida01)
        
    n = len(df)  # Número total de linhas do DataFrame

    convertTypes(df)

    # 🔹 Função para criar gráficos
    def make_chart(df, y_col, ymin, ymax):
        fig = go.Figure(layout_yaxis_range=[ymin, ymax])
        fig.add_trace(go.Scatter(
            x=df['dateDir'],
            y=df[y_col],  # 🔹 Arredondamento dos valores
            mode='lines+markers',
            text=df[y_col],  # 🔹 Exibir valores no gráfico
            textposition="top center"
        ))
        fig.update_layout(width=700, height=570, xaxis_title='Tempo', yaxis_title=y_col)
        return fig
        
    col05, col06 = st.columns(spec=[1, 1])
    with col05:
        st.markdown("<h4 style='text-align: justify; color: black;'> Variáveis de saída</h1>", unsafe_allow_html=True)
        chart_upleft = col05.empty()
        chart_upright = col06.empty()

    col07, col08 = st.columns(spec=[1, 1])
    with col07:
        st.markdown("<h4 style='text-align: justify; color: black;'> Porcentagem de Anomalia por Dia </h1>", unsafe_allow_html=True)
        saida02 = ['mediaReg']
        select_downleft = st.selectbox('', saida02)

    with col08:
        st.markdown("<h4 style='text-align: justify; color: black;'> Porcentagem de Anomalia por Dia </h1>", unsafe_allow_html=True)
        media = ['anomalies', 'notAanomalie']
        select_downright = st.selectbox('', media)

    col09, col10 = st.columns(spec=[1, 1])
    with col09:
        chart_downleft = col09.empty()
        chart_downright = col10.empty()

    # 🔄 Loop otimizado para atualização dos gráficos
    for i in range(0, n - 30, 1):
        df_tmp = df.iloc[i:i + 30, :]

        ymin_entrada, ymax_entrada = df[select_upleft].min() - 10, df[select_upleft].max() + 10
        ymin_saida01, ymax_saida01 = df[select_upright].min() - 10, df[select_upright].max() + 10
        ymin_saida02, ymax_saida02 = df[select_downleft].min() - 10, df[select_downleft].max() + 10
        ymin_media, ymax_media = df[select_downright].min() - 10, df[select_downright].max() + 10

        # 🔄 Atualizar gráficos sem recriar o layout
        chart_upleft.write(make_chart(df_tmp, select_upleft, ymin_entrada, ymax_entrada))
        chart_upright.write(make_chart(df_tmp, select_upright, ymin_saida01, ymax_saida01))
        chart_downleft.write(make_chart(df_tmp, select_downleft, ymin_saida02, ymax_saida02))
        chart_downright.write(make_chart(df_tmp, select_downright, ymin_media, ymax_media))

        time.sleep(0.8)  # ⏳ Reduzindo o tempo de espera para tornar mais fluido