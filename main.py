
import streamlit as st
from streamlit_option_menu import option_menu
import about, dataProfile, home, realtimedemo, staticpredictionForDay,staticpredictionForFiles, howto, scatterplot
from comum import config

config()

class Multiapp:
    
    def __int__(self):
        self.apps = []
    def add_app(self,title,function):
        self.app.append({
            "title"     : title,
            "function"  : function
        })

    def run() :

        app = option_menu(None, 
                        ['Home','Data Profile','scatterplot',
                        #  'How to',
                         'Real-Time Optimization','Static Prediction Day','Static Prediction Files',
                        #  'about'
                        ], 
            icons=['house-fill','bi-buildings-fill','database','question-diamond-fill','pc-display-horizontal','display','display','person-circle'], 
            menu_icon="cast", default_index=0, orientation="horizontal")
    
        
        if app == "Home":
            home.app()
        if app == "scatterplot":
            scatterplot.app()  
        if app == "Data Profile":
            dataProfile.app()    
        if app == "Real-Time Optimization":
            realtimedemo.app()
        if app == "How to":
            howto.app()         
        if app == 'Static Prediction Day':
            staticpredictionForDay.show_predict_page1()
        if app == 'Static Prediction Files':
            staticpredictionForFiles.show_predict_page2()    
        if app == 'about':
            about.app()    
             
    run()
