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
