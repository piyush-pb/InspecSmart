import streamlit as st
from streamlit_option_menu import option_menu
from home import home_operation
from document_analysis import document_analysis_operation
from img_desc import new_college
from score_calc import nirf_score_calc
from facility import facility

st.set_page_config(page_title="Hackoholics", page_icon=":guardsman:", layout="centered", initial_sidebar_state="expanded")

with st.sidebar:
    selected = option_menu("Main Menu", ["Predicted Facilities", 'Facility Inspection', 'Document Analysis','Image Desc', "Score Calculator"], 
        icons=['house', 'gear', 'book', 'pen'], menu_icon="cast", default_index=1,
        styles={ 
                "nav-link-selected": {
                    "background-color": "#000000", 
                    "font-size": "16px",
                },
            })

if selected == "Predicted Facilities":
    home_operation()
elif selected == "Document Analysis":
    document_analysis_operation()
elif selected == "Facility Inspection":
    facility()
elif selected == "Image Desc":
    new_college()
elif selected == "Score Calculator":
    nirf_score_calc()