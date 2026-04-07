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

st.sidebar.title('Le bien-être')
st.sidebar.image('./img/7_v2.svg')

# Filter année
year2 = df_wellness['Année'].unique()
if not len(year2):
    st.warning("Selectionner au moins une année")

selected_year = st.sidebar.multiselect('Quelle année vous interesse ?', year2, 
                                       default=[2023])

# Filter pays
country = df_wellness['Pays'].unique()
if not len(country):
    st.warning("Selectionner au moins un Pays")

selected_country = st.sidebar.multiselect('Quel pays souhaitez-vous analyser ?', country,
                                          default=['France', 'Italie'])
       #'Pays-Bas', 'Portugal', 'Luxembourg', 'Belgique',
       #'Autriche', 'Irlande', 'Finlande', 'Espagne', 'Lituanie',
       #'Italie', 'Lettonie', 'Estonie', 'République slovaque', 'Grèce'],

#st.title('Split steps of the story')
tab0, tab1, tab2 = st.tabs([ "Dépenses","Bien-être","Habitat"])

#__________________________
#__________________________
with tab0:
    tabq, tabr = st.tabs([ "Question","Réponse"])
    with tabq:
        st.header("Glissez-vous dans la peau de l'expert comptable de votre pays", divider='gray')
        st.caption("La répartition des deniers publics implique une lourde responsabilité et des priorisations difficiles. Essayez de faire varier les 4 catégories suivantes en restant sous la barre des 100% de l'enveloppe. Attention à la dette... :euro:")
    
        col0, col1, col2 = st.columns([1,1,3])
        with col0:
            st.write("Faites varier le pourcentage des dépenses allouées pour :")
            num_habitat = st.slider("L'Habitat ?", value=15, min_value=1, max_value=61, step=1, format="%d%%")
            num_sante = st.slider("La Santé", value=15, min_value=1, max_value=61, step=1, format="%d%%")
            num_protection_env = st.slider("La Protection de l'environnement", value=15, min_value=1, max_value=61, step=1, format="%d%%")
            num_protection_sociale = st.slider("La Protection sociale", value=15, min_value=1, max_value=61, step=1, format="%d%%")
            num_autre = st.slider("Autre", value=39, min_value=38, max_value=40, step=1, format="%d%%")
        
        with col1:
            #Limit to 100%
            max = 100
            #100 - num_habitat - num_sante - num_protection_env - num_protection_sociale
            sum_pct = num_habitat + num_sante + num_protection_env + num_protection_sociale + num_autre
            st.markdown("<br> <br> <br>", unsafe_allow_html=True)
            st.write("Pourcentage :", sum_pct, "%") 
            if sum_pct >100:
                st.error("Attention, vous êtes trop dépensier. Vous devez réduire les dépenses en dessous de 100 %...")

        with col2:
            list_x = [num_habitat, num_sante, num_protection_env, num_protection_sociale, num_autre]
            names = ['Habitat', 'Santé', "Protection de l'environnement", "Protection sociale", "Autre"]

            df_t = pd.DataFrame({'Pourcentage': list_x,'Dépense': names,})
            fig_t = px.treemap(df_t, path=["Dépense"], values="Pourcentage",color="Dépense", 
                            color_discrete_map={'Autre':'lightgrey', 'Protection sociale':'gold', 'Santé':'#a1ddd2',
                                                'Habitat':'darkblue',
                                                "Protection de l'environnement":'green' },
                            hover_data = ['Dépense', 'Pourcentage']
                            #color_continuous_scale="Viridis",
                            )

            fig_t.data[0].textinfo = 'label+text+percent parent' #+value' #value'+percent entry
            #fig3.update_traces(root_color="lightgrey")
            fig_t.update_traces(textfont=dict(size=20),marker=dict(cornerradius=5))
            fig_t.update_layout(margin = dict(t=30, l=5, r=5, b=5))
            st.plotly_chart(fig_t, use_container_width=True)
        
            #fig_p = px.pie(values=list_x, names=names,color =names , color_discrete_map={'Autre':'lightgrey', 'Protection sociale':'gold', 'Santé':'#a1ddd2',
            #                                    'Habitat':'darkblue',
            #                                    "Protection de l'environnement":'green' })
            #fig_p.update_traces(textposition='inside', textinfo='label+percent') #value
            #st.plotly_chart(fig_p)

    #__________________________
    with tabr:
        st.header("Comparer les dépenses avec celles des états européens de [l'OCDE](https://fr.wikipedia.org/wiki/Organisation_de_coop%C3%A9ration_et_de_d%C3%A9veloppement_%C3%A9conomiques)", divider='gray')
        st.caption("Dépenses :euro:")
        col0, col1 = st.columns([1,3])
        with col0:
            st.markdown("<br> <br> <br>", unsafe_allow_html=True)
            st.markdown("**Pas facile comme exercice... Un rappel des choix que tu as fait :**")
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("Habitat : ", num_habitat, "%")
            st.write("Santé : ", num_sante, "%")
            st.write("Protection de l'environnement : ", num_protection_env , "%")
            st.write("Protection sociale : ", num_protection_sociale , "%")
            st.write("Autre : ", num_autre, "%")
            st.markdown("<br> <br>", unsafe_allow_html=True)        
            st.write("⇦ Dans le bandeau de gauche tu as la possibilité d'ajouter des années ou des pays.")

        with col1:
            import plotly.express as px
            filtered_df_depenses = df_depenses[(df_depenses['Pays'].isin(selected_country))]
            filtered_df_depenses_annees = filtered_df_depenses[(df_depenses['Année'].isin(selected_year))]
            df3 = filtered_df_depenses.sort_values(by=['Année','variable','Pays'], ascending=[True,False,False]).query("Année==2021 & value>0") 


            fig3 = px.treemap(filtered_df_depenses_annees ,
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
            st.write("En passant la souris sur le graphique, le détail des 'Autres' dépenses s'affiche : 'Services publics', 'Education', etc.")

        #st.info("Chaque réaffectation du budget prends du temps pour en mesurer les impacts.")

        #filtered_df_depenses_show=filtered_df_depenses_annees
        #filtered_df_depenses_show['variable'] = filtered_df_depenses_show['variable'].str.replace('<br>',' ')
        #st.dataframe(
        #    filtered_df_depenses_show,
        #    use_container_width=True,
        #    #column_config={"code_crue": st.column_config.TextColumn("code_crue")},
        #)

        #__________________________
        st.header('Dépenses dans le temps', divider='gray')
        st.caption("Le budget est requestionné tous les an")
        import plotly.express as px
        #.query("Année==2003 |Année==2013 | Année==2023")

        fig0 = px.line(filtered_df_depenses,x="Année", y="value", color="variable", #barmode = 'group', cumulative = False, 
                                facet_col="Pays", facet_col_wrap=4, #height=1000, title="df_depenses" #'group','overlay', 'relative' facet_col="variable", facet_col_wrap=2 .update_traces( marker={"color": "red"}, name='Pays', showlegend=True #name="red",
                                color_discrete_map={ '(?)':'lightgrey','Protection<br>sociale':'gold', 'Santé':'#a1ddd2',
                                    'Services<br>publics':'lightgrey','Education':'lightgrey', 'Affaires<br>économiques':'lightgrey',
                                    'Ordre<br>public<br>et<br>sécurité':'lightgrey','Défense':'lightgrey','Habitat':'darkblue',
                                    'Sports,<br>culture<br>et<br>religions':'lightgrey',"Protection<br>de<br>l'environnement":'green' },
                                #hover_name='variable', 
                                #hover_data=["value", "Unité","Pays"]
        )
        fig0.update_layout(xaxis_title="", yaxis_title="Pourcentage du budget")
        st.plotly_chart(fig0) #, use_container_width=True)
        st.info("Le budget pour l'Habitat en Italie est passé de 1% en 2020 à 8% en 2023. Le budget Français de l'Habitat est assez constant avec environ 2 % depuis 20 ans.")

        #st.info("Chaque réaffectation du budget prends du temps pour en mesurer les impacts. En Italie un choix budgetaire fort a été porté sur l'Habitat.")


    #with tab2:
    #    st.header('Bien-être', divider='gray')
    #    st.caption("Bien-être par échelle :smile: ")

    #    # Insert a chat message container.
    #    with st.chat_message("user"):
    #        st.write("Hello 👋")
    #        #Scatter doubler les graphiques
    #        import plotly.express as px
    #        #fig = px.line(df_depenses_euro[df_depenses_euro['Dépense'].str.contains("ogement")].query("Montant>0 "), x="Année", y="Montant", color="Dépense",#size="Valeur_Mesurée", & Dépense=='Accessibilité financière du logement'
    #        #            hover_data=["Opération","Cde_Dépense","Dépense"], #size="Valeur_Mesurée", 
    #        #                #animation_frame="Année",facet_row ="Cde_Mesure",color_continuous_scale='RdBu',
    #        #                facet_col ="Opération", facet_col_wrap=2,height=800,
    #        #                title="Dépense'", #facet_row ="Unité", height=700
    #        #                ) #,  height=700) #width=800, facet_row="Pays",facet_col="Mesure", 
    #        #fig.show()
    #        #fig.show(autorange= 'True')
    #        #fig.update_xaxes(rangeslider_visible=True )
    #        st.line_chart(np.random.randn(30, 3))

    #        # Display a chat input widget.
    #        st.chat_input("Say something") 

    #    #st.radio('Selectionner', options=[1,2,3,4,5])
    #    st.slider('Slide me', min_value=0, max_value=10)

#__________________________
#__________________________
with tab1:
    tabq2, tabr2 = st.tabs([ "Question","Réponse"])
    #__________________________
    with tabq2:
        st.header("Bien-être dans l'habitat", divider='gray')
        st.caption("Question Habitat :smile: :house_with_garden: ")
        st.text("Les états européens de l'OCDE consacrent entre 1 et 8 % pour l'Habitat. Et toi, que représente tes dépenses pour le logement ?")
        
        col0, col1 = st.columns([2,2])
        with col0:
            num_habitat_perso = st.slider("Que représente ton budget dédié à l'Habitat ?", value=2, min_value=0, max_value=100, step=1, format="%d%%")
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("N'oublies pas toutes les dépenses associées : **loyers** y compris les services divers, l'approvisionnement en **eau**, **l'électricité**, le gaz et autres combustibles, ainsi que les dépenses liées au mobilier, équipements ménagers, biens et services pour l’entretien courant de la maison, dépenses de réparation du logement, remboursements...")

        with col1:
            num_autre_perso = 100 - num_habitat_perso
            list_x = [num_habitat_perso, num_autre_perso]
            names = ['Habitat', "Autre"]
            fig_p_perso = px.pie(values=list_x, names=names,color =names , color_discrete_map={'Autre':'lightgrey', 
                                            'Habitat':'darkblue', })
            fig_p_perso.update_traces(textposition='inside', textinfo='label+percent') #value
            st.plotly_chart(fig_p_perso)
    
    #__________________________
    with tabr2:
        st.header("Bien-être dans l'habitat", divider='gray')
        st.caption("Comment mesurer le bien être au sein du logment ? :smile: :house_with_garden: ")

        st.write("La classification [COFOG](https://en.wikipedia.org/wiki/Classification_of_the_Functions_of_Government) regarde le pourcentage dédié à l'Habitat comme critère de bien-être. Au dessus de 40 %, la surcharge financière lié au coût du logement est décrite comme impactant le bien être. Cela concerne 11 % des Français en 2022.")

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
        df2 = filtered_df_wellness.sort_values(by=['Pays','Année'], ascending=[False,False]).query("Domaine =='Logement' & Mesure !='Accessibilité financière du logement' & Année==2022") #.head(1) #| Année==2021")
        df2 = df2.sort_values(by=['Mesure'], key=lambda x: x.map(custom_order))

        col0, col1 = st.columns([1,4])
        with col0:
            st.markdown("<br> <br> <br>", unsafe_allow_html=True)
            st.image('./img/6.svg')  
        with col1:
            fig1 = px.line(
                df2,
                x="Mesure", #size= 'Valeur_Mesurée', #size_max=25,
                y="Valeur_Mesurée", color="Pays",height=500,width=800,
                hover_name="Pays", #size_max=20,
                hover_data=["Valeur_Mesurée", "Unité"] #"Domaine", "Mesure",
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
                        sizex=1,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                        sizey=1,#maxi * 0.2, #row["Valeur_Mesurée"]/5, #np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.2 + maxi * 0.05,
                        sizing="contain", opacity=0.8, layer="above"
                    )
                )

            #fig.update_layout(plot_bgcolor="#ffffff") #height=600, width=1000, yaxis_range=[-5e3, 55e3], 
            #Graphique en 2022
            fig1.update_layout(xaxis_title="",yaxis_title="Pourcentage en 2022") #xaxis_title=xaxis_title,
            fig1.update_traces(mode="markers+lines")
            st.plotly_chart(fig1)

        #st.button("Unité de mesure : Pourcentage du revenu disponible brut ajusté restant du ménage, après déduction des loyers et de l'entretien du logement")
        
        col0, col2, col3, col4 = st.columns([1,1,1,1])
        #col1.write('**Accessibilité financière du logement**')
        col2.write('**Surcharge financière lié au coût du logement**')
        col3.write('**Incapacité à maintenir le logement à bonne température**')
        col4.write('**Taux de surpeuplement**')
        # Three columns with different widths
        #col1, col2, col3, col4 = st.columns([4,1,1])
        # col1 is wider

        #col1.write("*Pourcentage du revenu disponible brut restant, après déduction des loyers et de l'entretien du logement.*")
        col2.write("*Pourcentage de la population consacrant plus de 40 % de leur revenu aux frais de logement.*")
        col3.write("*Pourcentage de ménages déclarant qu'ils n'ont pas les moyens de chauffer adéquatement leur logement.*")
        col4.write("*Pourcentage de ménages vivant dans des logements surpeuplés.*")

            
        # Using 'with' notation:
        with col0:
            st.write("")
        #with col1:
        #    st.write("L’accessibilité financière du logement fait référence au pourcentage du revenu disponible brut ajusté du ménage qui reste disponible pour le ménage après déduction des coûts de logement. Les coûts de logement comprennent le loyer (y compris les loyers imputés pour les logements détenus par leurs propriétaires occupants) et l'entretien (dépenses de réparation du logement, y compris les services divers, l'approvisionnement en eau, l'électricité, le gaz et autres combustibles, ainsi que les dépenses liées au mobilier, à l'ameublement, équipements ménagers et biens et services pour l’entretien courant de la maison).")
        #    #Les données proviennent de la base de données des comptes nationaux de l'OCDE et concernent à la fois les ménages et les institutions sans but lucratif au service des ménages. Les pays utilisant actuellement la version COICOP 2018 des dépenses de consommation finale annuelle des ménages comprennent l'Autriche, la Belgique, la Bulgarie, la République tchèque, le Danemark, l'Estonie, la France, l'Allemagne, la Hongrie, l'Irlande, l'Italie, la Corée, la Lettonie, la Lituanie, les Pays-Bas, le Portugal, la Slovénie et l'Espagne et la Suède.
        with col2:
            st.write("Consacrer plus de 40 % de ses revenus aux coûts de logement. Les coûts de logement incluent les loyers réels.")
            #Aucune donnée sur les remboursements du principal hypothécaire n’est disponible pour le Danemark. Pour le Chili, le Mexique, la Corée et les États-Unis, le revenu brut est utilisé plutôt que le revenu disponible. Les données sont tirées de la base de données de l'OCDE sur le logement abordable, qui provient des données d'enquêtes auprès des ménages.
        with col3:
            st.write("Ne pas avoir les moyens de maintenir le logement suffisamment au chaud dans le logement (précarité énergétique).")
            #Les données proviennent d'estimations fournies par les offices statistiques nationaux par le biais des Statistiques de l'Union européenne sur les revenus et les conditions de vie, une enquête représentative au niveau national avec de grands échantillons (d'environ 4 000 individus dans les plus petits États membres à environ 16 000 dans le plus grand) couvrant tous les membres des ménages privés âgés de 16 ans ou plus et disponible pour les pays de l'UE, ainsi que pour la Norvège et la Suisse.
        with col4:
            st.write("Espace de vie non respecté selon l'âge et la composition du ménage : si moins d'une pièce disponible pour chaque couple du ménage, chaque personne seule âgée de 18 ans ou plus, ... ")
            #Les données proviennent de la base de données de l'OCDE sur le logement abordable, qui utilise les données d'enquêtes auprès des ménages. Au Chili, au Mexique, au Danemark, aux Pays-Bas et aux États-Unis, aucune donnée n’est disponible concernant les locataires subventionnés.
        
        #placeholder = st.empty() # Create a placeholder
        #if st.button("Unité de mesure : Pourcentage du revenu disponible brut ajusté restant du ménage, après déduction des loyers et de l'entretien du logement"):
        #    placeholder.empty() # Clear the placeholder
        #else:
        #    placeholder.write("Accessibilité financière du logement") # Display content


        #with tab3:
        #    st.header('Température du logement', divider='gray')
        #    st.caption("Incapacité à maintenir le logement à bonne température ")
        #    #Scatter doubler les graphiques .query("Valeur_Mesurée>0")
        #    import plotly.express as px
            
        #    filtered_df_wellness = df_wellness[(df_wellness['Pays'].isin(selected_country))]
        #    fig_w = px.scatter(filtered_df_wellness[filtered_df_wellness['Domaine'].str.contains("ogement")].sort_values(by=['Année','Valeur_Mesurée','Pays'], ascending=[True,False,False]), #.query("Année>2011 & Année<=2022"), 
        #                    y="Valeur_Mesurée", x="Pays", size="Valeur_Mesurée", color="Cde_Mesure", hover_data=["Cde_Mesure","Unité"], #size="Valeur_Mesurée", 
        #                    animation_frame="Année",
        #                    size_max=20, title="Bien être",  #facet_row ="Unité", height=700
        #                    ) #,  height=700) #width=800, facet_row="Pays",facet_col="Mesure", 
        #    st.plotly_chart(fig_w)
            #fig.show(autorange= 'True')
            #fig.update_xaxes(rangeslider_visible=True )

with tab2:
    tabq3, tabr3 = st.tabs([ "Question","Réponse"])
    #__________________________
    with tabq3:
        st.header('Mesurer le Bien-être à grande échelle', divider='gray')
        st.caption("Question Habitat :smile: :house_with_garden: ")
        st.text("Question")

    with tabr3:
        st.header('Température du logement', divider='gray')
        st.caption("Incapacité à maintenir le logement à bonne température ")
        
        col0, col1 = st.columns([1,5])
        with col0:
            st.markdown("<br> <br>", unsafe_allow_html=True)
            st.info("Alors que le critère considère uniquement le maintien du logement au chaud, le top 4 comprend 3 pays au climat méditerranéen chaud : Grèce, Portugal, Espagne.")

            ## Sorting the DataFrame using the key argument
            df_wellness = df_wellness.sort_values(by=['Valeur_Mesurée', 'Pays','Année'], ascending=[False,False,False]).query("Domaine =='Logement' & Année==2022 & Mesure== 'Incapacité à maintenir le logement à bonne température'") #.head(1) #| Année==2021")
            df_wellness = df_wellness.sort_values(by=['Mesure'], key=lambda x: x.map(custom_order))
        with col1:
            figf = px.scatter(
                df_wellness,
                x="Pays", #size= 'Valeur_Mesurée', #size_max=25,
                y="Valeur_Mesurée", color="Pays",height=500,width=800,
                size_max=5,
                #hover_name="Pays",
                #hover_data=["Valeur_Mesurée"]
            )
            figf.update_layout(yaxis_title="Pourcentage en 2022") #xaxis_title=xaxis_title,
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

        st.markdown("Cet indicateur reflète une conséquence de la **précarité énergétique**, sans toutefois expliquer les causes possibles de l'incapacité à maintenir une température adéquate, qu'elles soient **économiques** *(prix de l'énergie, manque de ressources...)*, liées aux **caractéristiques du bâtiment** (efficacité énergétique, manque d'équipements) ou autres. Les caractéristiques **sociales** et **culturelles** des ménages influencent fortement la déclaration d'incapacité à chauffer adéquatement son logement, et le **niveau de température adéquate peut varier d'un pays à l'autre**.")

        st.info("Attention le biais de déni de réalité implique que des personnes en situation réelle de précarité énergétique peuvent nier cette situation d'inconfort.")
