import streamlit as st
import pandas as pd
import os
import shutil
from comum import arquivozip, extrair_arquivos,listar_arquivos

def show_predict_page1():
    st.markdown("<h1 style='text-align: center; color: black;'>Predição estática do modelo autoencoder</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Diários</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Modelos com 7 e 8 variáveis</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(gap='large', spec=[1,1])

    with col1:
        modelo = arquivozip()

        if modelo is not None:
            # 🛠 Apagar e recriar diretórios para evitar arquivos antigos
            temp = "temp"
            caminho_extraido = "arquivosExtraidos"

            if os.path.exists(temp):
                shutil.rmtree(temp)  
            os.makedirs(temp, exist_ok=True)

            if os.path.exists(caminho_extraido):
                shutil.rmtree(caminho_extraido)  
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



    with col2:
                # 🛠 Verificar se o CSV pode ser carregado
        try:
            dFrame = pd.read_csv(caminhoArquivo, sep=';')
            # st.success(f"Arquivo carregado: {csv_files[0]}")
        except Exception as e:
            # st.error(f"Erro ao carregar o CSV: {e}")
            return
        # 🛠 Verificar se a coluna "dateDir" existe antes de continuar
        if "dateDir" not in dFrame.columns:
            # st.error("A coluna 'dateDir' não foi encontrada no CSV!")
            return

        # Corrigir formato da coluna "dateDir"
        dFrame["dateDir"] = pd.to_datetime(dFrame["dateDir"], errors='coerce').dt.strftime("%Y-%m-%d")
        datas_unicas = dFrame["dateDir"].dropna().unique().tolist()

        if not datas_unicas:
            # st.warning("Nenhuma data válida encontrada no CSV.")
            return

        # Selectbox para escolher a data
        data_selecionada = st.selectbox("Selecione a data", datas_unicas)

    col3, col4 = st.columns(gap='large', spec=[1,1])        

    with col3:
        st.image("CNHI_variaveis_numeros.png")

    with col4:
        imagensList =listar_arquivos(caminho_extraido)

        jpeg_files = [img for img in imagensList if img.lower().endswith((".jpg", ".jpeg"))]
        

        if len (jpeg_files) == 0:
            # st.warning("Nenhuma imagem encontrada na pasta extraída.")
            return
        # Ajuste para encontrar a imagem correta com base na data selecionada
        imagem_correspondente = next(( img for img in jpeg_files if data_selecionada in img), None)
        

        if imagem_correspondente:
            st.image(imagem_correspondente, caption=f"Imagem para {data_selecionada}", use_container_width=True)
        else:
            st.warning(f"Nenhuma imagem correspondente encontrada para {data_selecionada}.")
    col5, col6 = st.columns(gap='large', spec=[1,1])        


    with col5:
        statisticsImg = [img for img in jpeg_files if "statistics" in img.lower()]
        statisticsImg1 = statisticsImg[0]
        if len(statisticsImg) > 1:
            statisticsImg2 = statisticsImg[1]
        st.image(statisticsImg1)
        
    with col6:
        if statisticsImg2 is not None:
            st.image(statisticsImg2)

