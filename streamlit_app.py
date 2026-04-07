# -----------------------------------------------------------------------------
# Declare some useful functions.
#import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
import math
import datetime
from pathlib import Path

import os
os.system("pip install -r requirements.txt")
import plotly.express as px
#from streamlit_player import st_player
import geopandas as gpd
#from ipyleaflet import Map, Marker
#from streamlit_folium import folium_static
#import pydeck as pdk
#import folium
#import streamlit_pannellum
#from streamlit_pannellum import streamlit_pannellum
#import dash_pannellum

#import openchord as ocd

#import dash
#from dash import html
#import dash_pannellum

#from plotly.subplots import make_subplots
#from plotly_calplot import calplot
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
    df_d = pd.read_csv(DATA_FILENAME, sep=';', encoding='utf-8')
    #df_d['value'] = df_d['value'].str.replace(",", ".", regex=False)  # replace decimal comma with dot
    df_d['value'] = df_d['value'].astype(float)

    return df_d
df_depenses = get_data_depenses()

# Filter année
#min_value_debit = df_wellness['Année'].min()
#max_value_debit = df_wellness['Année'].max()

#from_year, to_year = st.sidebar.slider(
#    'Années',
#    min_value=max_value_debit,
#    value=[min_value_debit, max_value_debit],max_value=max_value_debit)

# Filter année
year2 = df_wellness['Année'].unique()
if not len(year2):
    st.warning("Selectionner au moins une année")

selected_year = st.sidebar.multiselect('Quelle année vous interesse ?', year2, 
                                       default=[2011, 2021])

# Filter pays
country = df_wellness['Pays'].unique()
if not len(country):
    st.warning("Selectionner au moins un Pays")

selected_country = st.sidebar.multiselect('Quel pays souhaitez-vous analyser ?', country,
                                          default=['France', 'Allemagne'])
       #'Pays-Bas', 'Portugal', 'Luxembourg', 'Belgique',
       #'Autriche', 'Irlande', 'Finlande', 'Espagne', 'Lituanie',
       #'Italie', 'Lettonie', 'Estonie', 'République slovaque', 'Grèce'],

#st.title('Split steps of the story')
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([ "Dépenses","Dépenses Habitat","Mesurer le bien être","Bien-être Habitat","_","Froid"])

with tab0:
    st.header('Dépenses', divider='gray')
    st.caption("Dépenses :euro:")
    
    import plotly.express as px
    filtered_df_depenses = df_depenses[(df_depenses['Pays'].isin(selected_country)) & (df_depenses['Année'].isin(selected_year))]
    df3 = filtered_df_depenses.sort_values(by=['Année','variable','Pays'], ascending=[True,False,False]).query("Année==2021 & value>0") 


    fig3 = px.treemap(filtered_df_depenses ,
                    path=["Année",'Pays','variable'], 
                    values='value',color='variable', 
                    color_discrete_map={'(?)':'lightgrey', 'Protection<br>sociale':'gold', 'Santé':'#a1ddd2',
                                        'Services<br>publics':'','Education':'', 'Affaires<br>économiques':'',
                                        'Ordre<br>public<br>et<br>sécurité':'','Défense':'','Habitat':'darkblue',
                                        'Sports,<br>culture<br>et<br>religions':'',"Protection<br>de<br>l'environnement":'green' }
                    #color_continuous_scale="Viridis",
                    )

    fig3.data[0].textinfo = 'label+text+percent parent' #+value' #value'+percent entry
    #fig3.update_traces(root_color="lightgrey")
    fig3.update_traces(textfont=dict(size=20),marker=dict(cornerradius=5))
    fig3.update_layout(margin = dict(t=30, l=5, r=5, b=5))
    #fig3.show()
    st.plotly_chart(fig3, use_container_width=True)

    st.button("L'année est les catégories sont triées de la gauche vers la droite, de la plus grande valeur à la plus petite.")

    
    #filtered_df_depenses_show=filtered_df_depenses
    #filtered_df_depenses_show['variable'] = filtered_df_depenses_show['variable'].str.replace('<br>',' ')
    #st.dataframe(
    #    filtered_df_depenses_show,
    #    use_container_width=True,
    #    #column_config={"code_crue": st.column_config.TextColumn("code_crue")},
    #)

with tab1:
    st.header('Dépenses', divider='gray')
    st.caption("Dépenses : dans le temps ")
    import plotly.express as px
    #.query("Année==2003 |Année==2013 | Année==2023")
    fig0 = px.line(filtered_df_depenses,x="Année", y="value", color="variable", #barmode = 'group', cumulative = False, 
        facet_col="Pays", facet_col_wrap=4, #height=1000, title="df_depenses" #'group','overlay', 'relative' facet_col="variable", facet_col_wrap=2 .update_traces( marker={"color": "red"}, name='Pays', showlegend=True #name="red",
        color_discrete_map={ '(?)':'lightgrey','Protection<br>sociale':'gold', 'Santé':'#a1ddd2',
                            'Services<br>publics':'lightgrey','Education':'lightgrey', 'Affaires<br>économiques':'lightgrey',
                            'Ordre<br>public<br>et<br>sécurité':'lightgrey','Défense':'lightgrey','Habitat':'darkblue',
                            'Sports,<br>culture<br>et<br>religions':'lightgrey',"Protection<br>de<br>l'environnement":'green' }
    )
    st.plotly_chart(fig0) #, use_container_width=True)

    st.info('Info message')


with tab2:
    st.header('Bien-être', divider='gray')
    st.caption("Bien-être par échelle :smile: ")

    # Insert a chat message container.
    with st.chat_message("user"):
        st.write("Hello 👋")
        #Scatter doubler les graphiques
        import plotly.express as px
        #fig = px.line(df_depenses_euro[df_depenses_euro['Dépense'].str.contains("ogement")].query("Montant>0 "), x="Année", y="Montant", color="Dépense",#size="Valeur_Mesurée", & Dépense=='Accessibilité financière du logement'
        #            hover_data=["Opération","Cde_Dépense","Dépense"], #size="Valeur_Mesurée", 
        #                #animation_frame="Année",facet_row ="Cde_Mesure",color_continuous_scale='RdBu',
        #                facet_col ="Opération", facet_col_wrap=2,height=800,
        #                title="Dépense'", #facet_row ="Unité", height=700
        #                ) #,  height=700) #width=800, facet_row="Pays",facet_col="Mesure", 
        #fig.show()
        #fig.show(autorange= 'True')
        #fig.update_xaxes(rangeslider_visible=True )
        st.line_chart(np.random.randn(30, 3))

        # Display a chat input widget.
        st.chat_input("Say something") 

    st.radio('Selectionner', options=[1,2,3,4,5])


with tab3:
    st.header('Bien-être Habitat', divider='gray')
    st.caption("Bien-être de l'habitat en 2022 :smile: :house_with_garden: ")

    from PIL import Image
    import plotly.express as px

    filtered_df_wellness = df_wellness[(df_wellness['Pays'].isin(selected_country))]
    #& (df_wellness['Année'] <= to_year)
    #& (from_year <= df_wellness['Année'])

    #df = px.data.gapminder().query("year==2007")
    ## Custom sorting dictionary
    custom_order = {'Accessibilité financière du logement': 0, 
                    'Surcharge financière liée au coût du logement': 1, 'Incapacité à maintenir le logement à bonne température': 2, 
                    'Ménages vivant dans des logements surpeuplés': 3, 'Ménages disposant d’un accès internet' : 4}
    ## Sorting the DataFrame using the key argument
    df2 = filtered_df_wellness.sort_values(by=['Pays','Année'], ascending=[False,False]).query("Domaine =='Logement' & Année==2022") #.head(1) #| Année==2021")
    df2 = df2.sort_values(by=['Mesure'], key=lambda x: x.map(custom_order))

    col0, col1 = st.columns([1,4])
    with col0:
        st.write("\n_ \n_")
        st.image('./img/6.svg')  
    with col1:
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
                    sizex=7,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                    sizey=7,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                    sizing="contain", opacity=0.8, layer="above"
                )
            )

        #fig.update_layout(plot_bgcolor="#ffffff") #height=600, width=1000, yaxis_range=[-5e3, 55e3], 
        fig1.update_traces(mode="markers+lines")
        st.plotly_chart(fig1)

    #st.button("Unité de mesure : Pourcentage du revenu disponible brut ajusté restant du ménage, après déduction des loyers et de l'entretien du logement")
    
    col0, col1, col2, col3, col4 = st.columns([1,1,1,1,1])
    col1.write('**Accessibilité financière du logement**')
    col2.write('**Surcharge financière lié au coût du logement**')
    col3.write('**Incapacité à maintenir le logement à bonne température**')
    col4.write('**Taux de surpeuplement**')
    # Three columns with different widths
    #col1, col2, col3, col4 = st.columns([4,1,1])
    # col1 is wider

    col1.write("*Pourcentage du revenu disponible brut ajusté restant du ménage, après déduction des loyers et de l'entretien du logement.*")
    col2.write("*Pourcentage de la population dans la tranche inférieure de 40 % de la répartition des revenus consacrant plus de 40 % de leur revenu disponible aux frais de logement.*")
    col3.write("*Pourcentage de ménages déclarant qu'ils n'ont pas les moyens de chauffer adéquatement leur logement.*")
    col4.write("*Pourcentage de ménages vivant dans des logements surpeuplés.*")

          
    # Using 'with' notation:
    with col0:
        st.write("")
    with col1:
        st.write("L’accessibilité financière du logement fait référence au pourcentage du revenu disponible brut ajusté du ménage qui reste disponible pour le ménage après déduction des coûts de logement. Les coûts de logement comprennent le loyer (y compris les loyers imputés pour les logements détenus par leurs propriétaires occupants) et l'entretien (dépenses de réparation du logement, y compris les services divers, l'approvisionnement en eau, l'électricité, le gaz et autres combustibles, ainsi que les dépenses liées au mobilier, à l'ameublement, équipements ménagers et biens et services pour l’entretien courant de la maison).")
        #Les données proviennent de la base de données des comptes nationaux de l'OCDE et concernent à la fois les ménages et les institutions sans but lucratif au service des ménages. Les pays utilisant actuellement la version COICOP 2018 des dépenses de consommation finale annuelle des ménages comprennent l'Autriche, la Belgique, la Bulgarie, la République tchèque, le Danemark, l'Estonie, la France, l'Allemagne, la Hongrie, l'Irlande, l'Italie, la Corée, la Lettonie, la Lituanie, les Pays-Bas, le Portugal, la Slovénie et l'Espagne et la Suède.
    with col2:
        st.write("La surcharge financière lié au coût du logement est mesurée par le pourcentage de la population situés dans les 40 % inférieurs de la répartition des revenus qui consacrent plus de 40 % de leur revenu disponible aux coûts de logement, ce dernier seuil de 40 % étant basé sur la méthodologie utilisée par Eurostat pour les pays membres de l'UE. Les coûts de logement incluent les loyers réels ainsi que les coûts hypothécaires, englobant le remboursement du capital et les intérêts ; contrairement à la mesure de l’accessibilité financière du logement tirée des comptes nationaux, aucun loyer imputé pour les logements occupés par leur propriétaire n’est inclus. ")
        #Aucune donnée sur les remboursements du principal hypothécaire n’est disponible pour le Danemark. Pour le Chili, le Mexique, la Corée et les États-Unis, le revenu brut est utilisé plutôt que le revenu disponible. Les données sont tirées de la base de données de l'OCDE sur le logement abordable, qui provient des données d'enquêtes auprès des ménages.
    with col3:
        st.write("L’incapacité à maintenir une température adéquate dans le logement (précarité énergétique) fait référence au pourcentage de ménages déclarant ne pas avoir les moyens de maintenir leur logement suffisamment au chaud. Cet indicateur reflète une conséquence de la précarité énergétique, sans toutefois expliquer les causes possibles de l'incapacité à maintenir une température adéquate, qu'elles soient économiques (prix de l'énergie, manque de ressources, …), liées aux caractéristiques du bâtiment (efficacité énergétique, manque d'équipements) ou autres. Les caractéristiques sociales et culturelles des ménages influencent fortement la déclaration d'incapacité à chauffer adéquatement son logement, et le niveau de température adéquate peut varier d'un pays à l'autre. Enfin, les personnes en situation de précarité énergétique peuvent nier se considérer comme étant dans une situation inconfortable et, par conséquent, ne pas le déclarer (également appelé « biais de déni de réalité »). La question est posée à la personne de référence du ménage et les informations sont disponibles uniquement au niveau du ménage.")
        #Les données proviennent d'estimations fournies par les offices statistiques nationaux par le biais des Statistiques de l'Union européenne sur les revenus et les conditions de vie, une enquête représentative au niveau national avec de grands échantillons (d'environ 4 000 individus dans les plus petits États membres à environ 16 000 dans le plus grand) couvrant tous les membres des ménages privés âgés de 16 ans ou plus et disponible pour les pays de l'UE, ainsi que pour la Norvège et la Suisse.
    with col4:
        st.write("Le taux de surpeuplement (le pourcentage de ménages vivant dans des conditions de surpeuplement) adopte la définition convenue par l'UE, qui prend en compte différents besoins en espace de vie selon l'âge et la composition par sexe du ménage. Un ménage est considéré comme vivant dans des conditions de surpeuplement si moins d'une pièce est disponible pour : chaque couple du ménage ; chaque personne seule âgée de 18 ans ou plus ; chaque couple de personnes du même sexe entre 12 et 17 ans ; chaque personne seule entre 12 et 17 ans ne relevant pas de la catégorie précédente ; et chaque paire d'enfants de moins de 12 ans. ")
        #Les données proviennent de la base de données de l'OCDE sur le logement abordable, qui utilise les données d'enquêtes auprès des ménages. Au Chili, au Mexique, au Danemark, aux Pays-Bas et aux États-Unis, aucune donnée n’est disponible concernant les locataires subventionnés.
    
    #placeholder = st.empty() # Create a placeholder
    #if st.button("Unité de mesure : Pourcentage du revenu disponible brut ajusté restant du ménage, après déduction des loyers et de l'entretien du logement"):
    #    placeholder.empty() # Clear the placeholder
    #else:
    #    placeholder.write("Accessibilité financière du logement") # Display content


with tab4:
    st.header('Température du logement', divider='gray')
    st.caption("Incapacité à maintenir le logement à bonne température ")
    #Scatter doubler les graphiques .query("Valeur_Mesurée>0")
    import plotly.express as px
    
    filtered_df_wellness = df_wellness[(df_wellness['Pays'].isin(selected_country))]
    fig_w = px.scatter(filtered_df_wellness[filtered_df_wellness['Domaine'].str.contains("ogement")].sort_values(by=['Année','Valeur_Mesurée','Pays'], ascending=[True,False,False]), #.query("Année>2011 & Année<=2022"), 
                    y="Valeur_Mesurée", x="Pays", size="Valeur_Mesurée", color="Cde_Mesure", hover_data=["Cde_Mesure","Unité"], #size="Valeur_Mesurée", 
                    animation_frame="Année",
                    size_max=20, title="Bien être",  #facet_row ="Unité", height=700
                    ) #,  height=700) #width=800, facet_row="Pays",facet_col="Mesure", 
    st.plotly_chart(fig_w)
    #fig.show(autorange= 'True')
    #fig.update_xaxes(rangeslider_visible=True )

with tab5:
    st.header('Température du logement', divider='gray')
    st.caption("Incapacité à maintenir le logement à bonne température ")
    #st.snow()

     ## Sorting the DataFrame using the key argument
    df_wellness = df_wellness.sort_values(by=['Valeur_Mesurée', 'Pays','Année'], ascending=[False,False,False]).query("Domaine =='Logement' & Année==2023 & Mesure== 'Incapacité à maintenir le logement à bonne température'") #.head(1) #| Année==2021")
    df_wellness = df_wellness.sort_values(by=['Mesure'], key=lambda x: x.map(custom_order))

    figf = px.scatter(
        df_wellness,
        x="Pays", #size= 'Valeur_Mesurée', #size_max=25,
        y="Valeur_Mesurée", color="Pays",height=500,width=800,
        hover_name="Pays", size_max=5,
        hover_data=["Domaine", "Valeur_Mesurée","Mesure", "Unité"]
    )

    figf.update_traces(marker_color="rgba(0,0,0,0)")
    figf.update_traces(line=dict(width=0.5)) #color="Black",


    #maxDim = df2[["Mesure", "Valeur_Mesurée"]].max().idxmax()
    #maxi = df2[maxDim].max()
    for i, row in df_wellness.iterrows():
        country = row['Cde_Pays'] #.replace(" ", "-")
        figf.add_layout_image(
            dict(source=Image.open(f"flag/{country}.png"),
                xref="x", yref="y",
                xanchor="center", yanchor="middle",
                x=row["Pays"], y=row["Valeur_Mesurée"],
                sizex=1,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                sizey=1,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                sizing="contain", opacity=0.8, layer="above"
            )
        )

    #fig.update_layout(plot_bgcolor="#ffffff") #height=600, width=1000, yaxis_range=[-5e3, 55e3], 
    figf.update_traces(mode="markers+lines")
    st.plotly_chart(figf)

