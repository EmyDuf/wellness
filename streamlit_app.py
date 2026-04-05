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
    DATA_FILENAME = Path(__file__).parent/'data/bien_etre.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', encoding='utf-8')
    df['Valeur_Mesurée'] = df['Valeur_Mesurée'].str.replace(",", ".", regex=False)  # replace decimal comma with dot
    df['Valeur_Mesurée'] = df['Valeur_Mesurée'].astype(float)

    return df
df_wellness = get_data_wellness()

def get_data_depenses():
    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/df_depenses.csv'
    df = pd.read_csv(DATA_FILENAME, sep=';', encoding='utf-8')
    #df['Valeur_Mesurée'] = df['Valeur_Mesurée'].str.replace(",", ".", regex=False)  # replace decimal comma with dot
    #df['Valeur_Mesurée'] = df['Valeur_Mesurée'].astype(float)

    return df
df_depenses = get_data_depenses()

# Filter année
#min_value_debit = df_wellness['Année'].min()
#max_value_debit = df_wellness['Année'].max()

#from_year, to_year = st.sidebar.slider(
#    'Années',
#    min_value=max_value_debit,
#    value=[min_value_debit, max_value_debit],max_value=max_value_debit)

# Filter pays
#country = df_wellness['Pays'].unique()
#if not len(country):
#    st.warning("Selectionner au moins un Pays")

selected_country = st.sidebar.multiselect('Quel  souhaitez-vous regarder ?', ['France', 'Allemagne'],
       #'Pays-Bas', 'Portugal', 'Luxembourg', 'Belgique',
       #'Autriche', 'Irlande', 'Finlande', 'Espagne', 'Lituanie',
       #'Italie', 'Lettonie', 'Estonie', 'République slovaque', 'Grèce'],
    default=['France', 'Allemagne'])

#st.title('Split steps of the story')
tab0, tab1 = st.tabs([ "Bien-être", "PIB"])
with tab0:
    st.header('Bien-être', divider='gray')
    st.caption("Bien-être :smile: ")

    from PIL import Image
    import plotly.express as px

    filtered_df_wellness = df_wellness[(df_wellness['Pays'].isin(selected_country))]
    #& (df_wellness['Année'] <= to_year)
    #& (from_year <= df_wellness['Année'])

    #df = px.data.gapminder().query("year==2007")
    ## Custom sorting dictionary
    custom_order = {'Ménages disposant d’un accès internet' : 0,'Accessibilité financière du logement': 1, 
                    'Surcharge financière liée au coût du logement': 2, 'Incapacité à maintenir le logement à bonne température': 3, 'Ménages vivant dans des logements surpeuplés': 4}
    ## Sorting the DataFrame using the key argument
    df2 = filtered_df_wellness.sort_values(by=['Pays','Année'], ascending=[False,False]).query("Domaine =='Logement' & Année==2022") #.head(1) #| Année==2021")
    df2 = df2.sort_values(by=['Mesure'], key=lambda x: x.map(custom_order))

    fig1 = px.line(
        df2,
        x="Mesure", #size= 'Valeur_Mesurée', #size_max=25,
        y="Valeur_Mesurée", color="Pays",height=500,width=800,
        hover_name="Pays", #size_max=20,
        hover_data=["Domaine", "Valeur_Mesurée","Mesure", "Unité"]
    )

    fig1.update_traces(marker_color="rgba(0,0,0,0)")
    fig1.update_traces(line=dict(width=0.5)) #color="Black",


    #maxDim = df2[["Mesure", "Valeur_Mesurée"]].max().idxmax()
    #maxi = df2[maxDim].max()
    for i, row in df2.iterrows():
        country = row['Cde_Pays'] #.replace(" ", "-")
        fig1.add_layout_image(
            dict(source=Image.open(f"flag/{country}.png"),
                xref="x", yref="y",
                xanchor="center", yanchor="middle",
                x=row["Mesure"], y=row["Valeur_Mesurée"],
                sizex=10,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                sizey=10,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                sizing="contain", opacity=0.8, layer="above"
            )
        )

    #fig.update_layout(plot_bgcolor="#ffffff") #height=600, width=1000, yaxis_range=[-5e3, 55e3], 
    fig1.update_traces(mode="markers+lines")
    fig1.show()

    st.plotly_chart(fig1)


with tab1:
    st.header('Dépenses', divider='gray')
    st.caption("Dépenses :money:")

    filtered_df_depenses = df_depenses[(df_depenses['Pays'].isin(selected_country))]

    #filtered_df_depenses['variable'] = filtered_df_depenses['variable'].str.split('_').str[0]
    #filtered_df_depenses['variable'] = filtered_df_depenses['variable'].str.replace(' ','<br>')

    fig2 = px.treemap(filtered_df_depenses.sort_values(by=['Année','variable','Pays'], ascending=[False,False,False]).query("Année==2021 & value>0"), 
                    path=["Année",'Pays','variable'], #"Année==2012 | Année==2022 & 
                    values='value',color='variable', #title='Dépenses', #marker_colorscale = 'Blues'
                    )#labels = "label+value+percent parent+percent entry")

    fig2.data[0].textinfo = 'label+text+percent parent' #+value' #value'+percent entry
    #fig2.update_traces(textfont=dict(size=20),marker=dict(cornerradius=5))
    fig2.update_layout(margin = dict(t=30, l=5, r=5, b=5))
    fig2.show()
    st.plotly_chart(fig2)
    