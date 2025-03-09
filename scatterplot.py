import streamlit as st
import pandas as pd
from comum import  carregar_arquivo ,criar_graficos



def app():
    df = carregar_arquivo()  # Certifique-se de que o arquivo foi carregado antes de chamar a função
    
    
    if df is not None:
        # Verificar se a coluna 'BaseCutRPM' contém apenas valores escalares
        if 'BaseCutRPM' in df.columns:
            df = df[df['BaseCutRPM'].apply(lambda x: pd.api.types.is_scalar(x))]
        
        criar_graficos(df)
        
    print(df)
        


        
    