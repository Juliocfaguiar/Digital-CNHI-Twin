import streamlit as st
from streamlit_option_menu import option_menu
import about, dataProfile, home, realtimedemo, staticpredictionForDay, staticpredictionForFiles, howto, scatterplot
from comum import config

config()
st.set_option('server.maxUploadSize', 1000)  # Aumentar o tamanho máximo de upload para 1000 MB

class Multiapp:
    
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        app = option_menu(None, 
                          ['Home', 'Data Profile', 'scatterplot',
                           'Real-Time Optimization', 'Static Prediction Day', 'Static Prediction Files'],
                          icons=['house-fill', 'bi-buildings-fill', 'database', 'question-diamond-fill', 'pc-display-horizontal', 'display', 'display', 'person-circle'], 
                          menu_icon="cast", default_index=0, orientation="horizontal")
        
        if app == "Home":
            home.app()
        elif app == "scatterplot":
            scatterplot.app()  
        elif app == "Data Profile":
            dataProfile.app()    
        elif app == "Real-Time Optimization":
            realtimedemo.app()
        elif app == "How to":
            howto.app()         
        elif app == 'Static Prediction Day':
            staticpredictionForDay.show_predict_page1()
        elif app == 'Static Prediction Files':
            staticpredictionForFiles.show_predict_page2()    
        elif app == 'about':
            about.app()    
             
app = Multiapp()
app.run()
