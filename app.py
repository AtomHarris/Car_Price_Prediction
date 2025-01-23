
import streamlit as st
st.set_page_config(
    page_title="Kenya.Luxury.Car.Price.Prediction",
    page_icon=":racing_car:",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/AtomHarris/',
        'Report a bug': 'https://github.com/AtomHarris/',
        'About': "# Kenya Luxury Car Price Prediction!"
    }
)

from  classes import *
from app_pages.home import *
from app_pages.prediction import *
from app_pages.contact_us import display_contact_info, contact_form

# Company Logo
st.sidebar.image('images/logo.webp', use_column_width=True)

# Sidebar Selectbox initialization
selected = st.sidebar.selectbox("Go to", ["Home", "Predictions", "Contact"])

# Class names
#class_names = ['Food Organics', 'Glass', 'Metal', 'Miscellaneous Trash', 'Paper', 'Plastic', 'Textile Trash', 'Vegetation']

# Selecting the Main Home Page
if selected == "Home":
    render_home_page()

# Selecting the About Page
elif selected == "Predictions":
    predict()

#Selecting the Contact Page
elif selected == "Contact":
    display_contact_info()
    contact_form()



