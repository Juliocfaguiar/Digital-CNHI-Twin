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
             
            except Exception as e:
                # st.error(f"Erro ao carregar o CSV: {e}")
                return
            
    



    # §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ # 


    # # Criando duas colunas para seleção de parâmetros
    col03, col04 = st.columns(2)
        
    # # Configuração da coluna esquerda - Parâmetros de entrada do reator
    with col03:
       
        st.markdown("<h4 style='text-align: justify; color: black;'> Variaveis de Entrada</h1>", unsafe_allow_html=True)
        entrada = ['EngLoad','EngRPM','GndSped','BaseCutPrs','BaseCutHght','ChopperHydPrs','ChopperRPM','HydrostatChrgPrs']
        select_entrada = st.selectbox('', entrada, key='EngLoad')
    # # Configuração da coluna direita - Parâmetros de saída do reator
    with col04:
        
        st.markdown("<h4 style='text-align: justify; color: black;'> Variáveis de saída</h1>", unsafe_allow_html=True)
        saida = ['anomalies','notAanomalie','anomalyAcumulate','totalAcumulate']         
        select_saida = st.selectbox('', saida, key="anomalies")

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

    col1, col2 = st.columns(2)
    # pass
    chart_left = col1.empty()
    chart_right = col2.empty()

    # 🔄 Loop otimizado para atualização dos gráficos
    for i in range(0, n - 30, 1):
        # chart_left = st.empty()
        time.sleep(0.05)
        df_tmp = df.iloc[i:i + 30, :]

        ymin_entrada, ymax_entrada = df[select_entrada].min() - 10, df[select_entrada].max() + 10
        ymin_saida, ymax_saida = df[select_saida].min() - 10, df[select_saida].max() + 10

        # 🔄 Atualizar gráficos sem recriar o layout
        chart_left.write(make_chart(df_tmp, select_entrada, ymin_entrada, ymax_entrada))
        chart_right.write(make_chart(df_tmp, select_saida, ymin_saida, ymax_saida))

        time.sleep(0.8)  # ⏳ Reduzindo o tempo de espera para tornar mais fluido

