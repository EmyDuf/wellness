# -----------------------------------------------------------------------------
# Declare some useful functions.
import altair as alt
import streamlit as st
import pandas as pd
import math
import datetime
from pathlib import Path

import os
os.system("pip install -r requirements.txt")
import plotly.express as px
from streamlit_player import st_player
import geopandas as gpd
#from ipyleaflet import Map, Marker
#from streamlit_folium import folium_static
import pydeck as pdk
#import folium
import streamlit_pannellum
from streamlit_pannellum import streamlit_pannellum
#import dash_pannellum

#import dash
#from dash import html
#import dash_pannellum

from plotly.subplots import make_subplots
from plotly_calplot import calplot
#libxmp #ipyleaflet #pyproj #json #folium
#import json
import geopandas as gpd
#import pyproj
#lxml
#libxmp2 #lxml #python-xmp-toolkit #libxmp
#streamlit_pannellum

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(layout="wide",    page_title='Wellness : fr',
    page_icon=':smile:',initial_sidebar_state='collapsed',) # This is an emoji shortcode. Could be a URL too.)
#@m = folium.Map(location=[43.59966,1.44043,], zoom_start=11, tiles='OpenStreetMap')
#folium_static(m)

# Primary accent for interactive elements
primaryColor = '#d33682'
# Background color for the main content area
backgroundColor = '#002b36'
# Background color for sidebar and most interactive widgets
secondaryBackgroundColor = '#586e75'
# Color used for almost all text
textColor = '#fafafa'
# Font family for all text in the app, except code blocks
# Accepted values (serif | sans serif | monospace) 
# Default: "sans serif"
font = "sans serif"

# -----------------------------------------------------------------------------
#@st.cache_data
def get_data_wellness():
    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/csv_long/bien_etre.csv'
    df = pd.read_csv(DATA_DIR, sep=';', encoding='utf-8')
    df['Valeur_Mesurée'] = df['Valeur_Mesurée'].str.replace(",", ".", regex=False)  # replace decimal comma with dot
    df['Valeur_Mesurée'] = df['Valeur_Mesurée'].astype(float)

    return df
df_wellness = get_data_wellness()

# Filter pays
country = df_wellness['Pays'].unique()
if not len(pays):
    st.warning("Selectionner au moins un Pays")

selected_country = st.sidebar.multiselect('Quel  souhaitez-vous regarder ?', country,  
['France', 'Allemagne'])
