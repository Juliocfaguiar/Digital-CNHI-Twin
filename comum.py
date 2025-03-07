import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly as plt
import zipfile
from PIL import Image
import re
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def config():
    st.set_page_config(page_title="Digital-Twin",layout="wide")
    st.set_option('server.maxUploadSize', 500)

# columns =  ['BaseCutRPM','ChopperRPM','EngRPM','EngLoad','ChopperHydPrs','BaseCutHght','BaseCutPrs','BHF','GndSpd','HydrostatChrgPrs','A2000_ChopperHydOilPrsHi']
columns =  ['DateTime [-]','BaseCutRPM','ChopperRPM','EngRPM','EngLoad','ChopperHydPrs','BaseCutHght','BaseCutPrs','BHF','GndSpd','HydrostatChrgPrs','A2000_ChopperHydOilPrsHi']

def lerArquivo():
    arquivo = st.file_uploader("Escolha um arquivo CSV",type=['csv'])
    df = pd.DataFrame()
    if arquivo:
        print(f'Arquivo lido ={arquivo.name} : {arquivo.type}')
        df = pd.read_csv(arquivo,sep =";")
        
        renameColumns(df)
        df = df[columns]
        st.session_state['df'] = df
    
    else:
        st.error('Arquivo ainda não foi importado')
    return df
        
def renameColumns(df):
    df.rename(columns={"Time [s]": "Time"}, inplace= True)
    df.rename(columns={"PB_Ucm2_Status_84::BHF_On_Off": "BHF"}, inplace= True)
    df.rename(columns={"Hydstat_Charge_Press": "HydrostatChrgPrs"}, inplace= True)
    df.rename(columns={"Absolute Time [sec]" : "Time"}, inplace= True)
    df.rename(columns={"Chopper_Rpm" : "ChopperRPM"}, inplace= True)
    df.rename(columns={"Chopper_Hydr_Press" : "ChopperHydPrs"}, inplace= True)
    df.rename(columns={"BHF_On_Off": "BHF"}, inplace= True)
    df.rename(columns={"BaseCutter_Rpm": "BaseCutRPM"}, inplace= True)
    df.rename(columns={"basecutter_height": "BaseCutHght"}, inplace= True)
    df.rename(columns={"Basecutter_pressure": "BaseCutPrs"}, inplace= True)
    df.rename(columns={"Ground_Speed": "GndSpd"}, inplace= True)
    df.rename(columns={"Engine_Rpm": "EngRPM"}, inplace= True)
    # df.rename(columns={"y_position": "Js_1YAxPositn"}, inplace= True)
    # df.rename(columns={"x_position": "Js_1XAxPositn"}, inplace= True)
    df.rename(columns={"Eng_Load": "EngLoad"}, inplace= True)
    df.rename(columns={"A2000_Chopper_Hydr_Oil_Press_High": "A2000_ChopperHydOilPrsHi"}, inplace= True)
    # df.rename(columns={"Chopper_Pct_Setp": "ChopperPctSetp"}, inplace= True)
    # df.rename(columns={"Hydstat_Charge_Press": "HydrostatChrgPrs"}, inplace= True)


def renameVar(df):
    df.rename(columns={"imptEngLoad": "EngLoad"}, inplace= True)
    df.rename(columns={"imptEngRPM": "EngRPM"}, inplace= True)
    df.rename(columns={"imptGndSpd": "GndSped"}, inplace= True)
    df.rename(columns={"imptBaseCutPrs" : "BaseCutPrs"}, inplace= True)
    df.rename(columns={"imptBaseCutHght" : "BaseCutHght"}, inplace= True)    
    df.rename(columns={"imptChopperHydPrs" : "ChopperHydPrs"}, inplace= True)
    df.rename(columns={"imptChopperRPM" : "ChopperRPM"}, inplace= True)
    df.rename(columns={"imptHydrostatChrgPrs": "HydrostatChrgPrs"}, inplace= True)


def dropna(df):
    colunas_dropna = [
        'BaseCutRPM','ChopperRPM','EngRPM','EngLoad','ChopperHydPrs','BaseCutHght','BaseCutPrs','BHF','GndSpd',
                      'floating_roller_io_pos_mv','HydrostatChrgPrs','A2000_ChopperHydOilPrsHi']
    
    # Verificar se todas as colunas especificadas existem no DataFrame
    colunas_existentes = [col for col in colunas_dropna if col in df.columns]
    
    # Remover linhas com NaNs nas colunas especificadas
    if colunas_existentes:
        df.dropna(subset=colunas_existentes, inplace=True)


def arquivozip():
    arquivo = st.file_uploader("Escolha um arquivo ZIP",type=['zip','rar'])
    if arquivo:
        print(f'Arquivo lido ={arquivo.name} : {arquivo.type}')
    else:
        st.error('Arquivo ainda não foi importado')
    return arquivo

# Função para extrair imagens do ZIP
def extrair_arquivos(pastaZip, extrair="arquivosExtraidos"):
    if not os.path.exists(extrair):
        os.makedirs(extrair)
        
    with zipfile.ZipFile(pastaZip, 'r') as zip_ref:
        zip_ref.extractall(extrair)
    
    return [f for f in os.listdir(extrair) if f.endswith((".csv", ".jpg", ".jpeg"))]

def listar_arquivos(diretorio):
    lista_arquivos = []
    
    # Percorre o diretório e subdiretórios
    for dirpath, _, filenames in os.walk(diretorio):
        for file in filenames:
            caminho_completo = os.path.join(dirpath, file)
            lista_arquivos.append(caminho_completo)  # Adiciona o caminho completo do arquivo
    
    return lista_arquivos



# §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§ #


def showAllColumns(df, xColumnName, columnChoose, someColors, plt):
    contador = 0
    plt.figure(figsize=(20,10))
    fig, ax = plt.subplots()
    for coly in columnChoose:
        xValues, yValues = selConName(xColumnName,coly,df)
        ax.plot(xValues, yValues,color=someColors[contador], label=coly)
        contador += 1
    st.pyplot(fig)
    print(columnChoose)

def columnsNames():
    columns =  [
        'BaseCutRPM',
        'ChopperRPM','EngRPM','EngLoad','ChopperHydPrs','BaseCutHght','BaseCutPrs','BHF',
        'GndSpd','floating_roller_io_pos_mv','HydrostatChrgPrs','A2000_ChopperHydOilPrsHi']

    return columns

def selConName(colx, coly, df):
    df_filter = df.loc[:, [colx, coly]]
    df_filter.dropna(inplace = True)
    return df_filter[colx], df_filter[coly]



def getUnidadeLabels():
    unidadesDict = {}
    for name in columnsNames() :
        unidadesDict[name] = ''
        unidadesDict['ChopperHydPrs'] = '\n(bar)'
        unidadesDict['ChopperRPM'] = '\n(rpm)'
        unidadesDict['BaseCutPrs'] = '\n(bar)'
        unidadesDict['BaseCutRPM'] = '\n(rpm)'
        unidadesDict['GndSpd'] = '\n(km/h)'
        unidadesDict['EngRPM'] = '\n(rpm)'
        unidadesDict['EngLoad'] = '\n(%)'
        unidadesDict['BaseCutHght'] = '\n(%)'
        unidadesDict['ChopperPctSetp'] = '\n(%)'
        unidadesDict['HydrostatChrgPrs'] = '\n(bar)'
        unidadesDict['A2000_ChopperHydOilPrsHi'] = '\n(bin)'
        unidadesDict['BHF'] = '\n(bin)'
        unidadesDict['Js_1YAxPositn'] = '\n(?)'
        unidadesDict['Js_1XAxPositn'] = '\n(?)'


    return unidadesDict


def tratarLabel (coluna,unidade):
    fim = 10
#    for name in coluna():
    if coluna == 'ChopperHydPrs':
        return 'ChopHPr' + unidade
    if coluna == 'ChopperRPM':
        return 'ChopRPM' + unidade
    if coluna == 'BaseCutPr':
        return 'BaseCPr' + unidade
    if coluna == 'BaseCutHght':
        return 'BaseCutHg' + unidade
    if coluna == 'ChopperPctSetp':
        return 'ChopPct' + unidade
    if coluna == 'BaseCutRPM':
        return 'BaseCRPM' + unidade
    if coluna == 'A2000_ChopperHydOilPrsHi':
        return 'A2000Chop' + unidade
    

    juncao = f'{coluna[0:fim]} {unidade}'
    return juncao 



# Função para carregar o arquivo CSV
def carregar_arquivo():
    arquivo = st.file_uploader("Escolha um arquivo CSV", type=['csv'])

    if arquivo is not None:
        # Evita reprocessamento se o mesmo arquivo já estiver carregado
        if 'arquivo' not in st.session_state or st.session_state['arquivo'] != arquivo:
            st.session_state['arquivo'] = arquivo
            
            # Ler arquivo CSV
            df = pd.read_csv(arquivo, sep=";")
           
            renameColumns(df)
            df.dtypes[df.dtypes == 'int64']
            st.session_state['df'] = df  # Salva no estado da sessão
        return st.session_state['df']

    return None  # Retorna None caso nenhum arquivo seja carregado


def criar_graficos(df):
 #   st.subheader("📊 Visualização de Dados")

    colunas = columnsNames()
    x_coluna = ["Time"]

    colunas_selecionadas = st.multiselect("Selecione as variáveis para análise (eixo Y):", colunas)

    if not colunas_selecionadas:
        st.warning("Selecione pelo menos uma variável para visualizar os gráficos.")
        return

    total_graficos = len(colunas_selecionadas)
    linhas = (total_graficos // 2) + (total_graficos % 2)  # Organiza em 2 colunas
    fig, axs = plt.subplots(nrows=linhas, ncols=2, figsize=(12, 4 * linhas), layout='constrained')

    # Se houver apenas um gráfico, transforma axs em uma lista para evitar erro de indexação
    if total_graficos == 1:
        axs = np.array([[axs]])

    axs = axs.flatten()  # Transforma a matriz em lista para fácil iteração

    for idx, coluna in enumerate(colunas_selecionadas):
        axs[idx].scatter(df[x_coluna], df[coluna], s=1, color="blue", alpha=0.7)
        axs[idx].set_xlabel(x_coluna)
        axs[idx].set_ylabel(coluna)
        # axs[idx].set_title(f"Dispersão de {coluna} vs {x_coluna}")
        axs[idx].grid(True)

    # Esconde gráficos vazios se houver número ímpar de gráficos
    if total_graficos % 2 == 1:
        axs[-1].axis("off")

    st.pyplot(fig)


def convertTypes(df):
    colunas_para_converter = ['EngLoad', 'EngRPM', 'GndSped', 'BaseCutPrs', 
                              'BaseCutHght', 'ChopperHydPrs', 'ChopperRPM', 'HydrostatChrgPrs']

    for col in colunas_para_converter:
        if col in df.columns:
            # 🔹 Convertendo tudo para string para facilitar limpeza
            df[col] = df[col].astype(str).str.replace(',', '.').str.strip()

            # 🔹 Substituir valores inesperados por NaN
            df[col] = df[col].replace(["", " ", "N/A", "erro", "None"], np.nan)

            # 🔹 Converter para número
            df[col] = pd.to_numeric(df[col], errors='coerce')

            # 🔹 Se necessário, substituir NaN por 0 e converter para inteiro
            df[col] = df[col].fillna(0).astype(int)
