import streamlit as st
import pandas as pd
import os
import shutil
from comum import arquivozip, extrair_arquivos, listar_arquivos

def show_predict_page2():
    st.markdown("<h1 style='text-align: center; color: black;'>Predição estática do modelo autoencoder</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>Por arquivos</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Modelos com 7 e 8 variáveis</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(gap='large', spec=[1,1])

    with col1:
        modelo = arquivozip()

        if modelo is not None:
            temp = "temp"
            caminho_extraido = "arquivosExtraidos"

            if os.path.exists(temp):
                shutil.rmtree(temp)  
            os.makedirs(temp, exist_ok=True)

            if os.path.exists(caminho_extraido):
                shutil.rmtree(caminho_extraido)  
            os.makedirs(caminho_extraido, exist_ok=True)

            pastaZip = os.path.join(temp, modelo.name)
            with open(pastaZip, "wb") as f:
                f.write(modelo.getvalue())

            extrair_arquivos(pastaZip, extrair=caminho_extraido)

            csvLista = listar_arquivos(caminho_extraido)
            csv_files = [f for f in csvLista if f.endswith(".csv")]

            if not csv_files:
                # st.error("Nenhum arquivo CSV encontrado no ZIP!")
                return
            
            caminhoArquivo = csv_files[0]

    with col2:
        try:
            dFrame = pd.read_csv(caminhoArquivo, sep=';')
            # st.success(f"Arquivo carregado: {csv_files[0]}")
        except Exception as e:
            # st.error(f"Erro ao carregar o CSV: {e}")
            return

        if "dateDir" not in dFrame.columns:
            # st.error("A coluna 'dateDir' não foi encontrada no CSV!")
            return

        dFrame["dateDir"] = pd.to_datetime(dFrame["dateDir"], errors='coerce')
        dFrame["Data"] = dFrame["dateDir"].dt.strftime("%Y-%m-%d")
        dFrame["Hora"] = dFrame["dateDir"].dt.strftime("%H:%M:%S")

        datas_unicas = sorted(dFrame["Data"].dropna().unique().tolist())

        if not datas_unicas:
            # st.warning("Nenhuma data válida encontrada no CSV.")
            return

        data_selecionada = st.selectbox("Selecione a data", datas_unicas)
        horarios_disponiveis = dFrame[dFrame["Data"] == data_selecionada]["Hora"].unique().tolist()
        horario_selecionado = st.selectbox("Selecione o horário", sorted(horarios_disponiveis))

        # Remover hífen de data_selecionada
        data_selecionada = data_selecionada.replace("-", "")

        # Remover dois pontos e zeros de horario_selecionado
        horario_selecionado = horario_selecionado.replace(":", "").replace("00", "")

        # Concatenar data_selecionada e horario_selecionado
        data_horario_selecionado = f"{data_selecionada}_{horario_selecionado}"


    col3, col4 = st.columns(gap='large', spec=[1,1])        

    with col3:
        st.image("CNHI_variaveis_tabela.png")

    with col4:
        imagensList = listar_arquivos(caminho_extraido)
        jpeg_files = [img for img in imagensList if img.lower().endswith((".jpg", ".jpeg"))]
        
        if len(jpeg_files) == 0:
            st.warning("Nenhuma imagem encontrada na pasta extraída.")
            return
        
        imagem_correspondente = next((img for img in jpeg_files if data_horario_selecionado in img), None)

        if imagem_correspondente:
            st.image(imagem_correspondente, caption=f"Imagem para {data_horario_selecionado}", use_container_width=True)
        else:
            st.warning(f"Nenhuma imagem correspondente encontrada para {data_horario_selecionado}.")
    
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
