# La classification des dépenses
| Thème | Exemples |
|:--|:--|
|  1-Services publiques|  Exécutif, législatif, impôts, recherche, gestion de la dette, ...|
|  2-Défense|  Défense civile et militaire, aide internationale, ... |
| 3-Ordre public et sécurité | Police, pompiers, justice, prisons, ... |
| 4-Affaires économiques |  Agriculture, énergie, constructions, industries, transport, communication, ...|
|  5-Protection de l'environnement|  Gestion des ordures, épuration de l'eau, pollutions, protection des espèces, ...|
| 6-Habitat|  Développement, voiries, eau, éclairages, ...|
| 7-Santé|  Matériels, médicaments, hôpitaux, recherche, ...|
| 8-Sports, culture et religions| Sports, services public de diffusion, culture, ...  |
| 9-Education | Ecoles, collèges, lycées, universités, services, ...|
| 10-Protection sociale | Maladie, vieillesse, famille, chômage, exclusion, ... |

[Sources](https://www.oecd.org/fr/publications/panorama-des-administrations-publiques-2025_758a7905-fr/full-report/classification-of-the-functions-of-government-cofog_16aa2337.html)

Sauf indication contraire, les montants monétaires sont les milliard d'euros.

Cette classification a le mérite de permettre la comparaison mais présente certains défauts qui peuvent entacher les interprétations : 
 - Ambiguïté de finalité : certaines dépenses contribuent à plusieurs finalités mais ne sont comptabilisées que dans une
 - Ne fait pas de distinction entre le fonctionnement et l'investissement
 - Soumise à l'arbitraire de l'interprétation de chaque pays

# Les facettes du bien être
Bien qu'il soit impossible de chiffrer le bonheur, il est néanmoins possible d'approcher la réalité par un ensemble de critères subjectifs (note entre 0 et 10) et des moyennes nationales (revenu médian, pourcentage de foyer équipé d'internet, ...). Une liste de 60 critères quantitatifs organisés en domaines :  [Source](https://www.oecd.org/fr/data/tools/well-being-data-monitor.html)


| Domaine | Exemples |
|:--|:--|
| Logement | - Ménages vivant dans des logements surpeuplés <br> - Accessibilité financière du logement |
| Savoirs et compétences | - Adultes ayant de faibles compétences en calcul <br> - Compétences des élèves en compréhension de l’écrit|
| Revenu et patrimoine | - Patrimoine net médian <br> - Salaire brut annuel moyen |
| Bien-être subjectif | - Sentiment de solitude <br>  - Satisfaction à l’égard de la vie |
| Liens sociaux | - Satisfaction à l’égard des relations personnelles inférieure à 5 <br>  - Manque de soutien social |
| Qualité environnementale | - Accès à des espaces verts <br> - Exposition à la pollution de l’air |
| Engagement civique | - Participation électorale <br> - Ne pas avoir son mot à dire concernant l’action des pouvoirs publics |
| Equilibre travail-vie | - Quintile supérieur de la satisfaction à l’égard de l’emploi du temps <br> - Satisfaction au travail |
| Santé | - Espérance de vie à la naissance <br> - Etat de santé perçu comme bon |
| Sécurité | - Sentiment d’insécurité la nuit <br> - Homicides |

 Disponibles par pays et par années entre 2004 et 2025

# La population (nombre et répartition)
Afin d'analyser ces données il est nécessaire de disposer de contexte. C'est le rôle de deux fichiers :
 - population 
 - pyramide_age
   
par pays x année de 2002 à 2024

# Contexte supplémentaire
Pour ne pas limiter les appétits 3 autres variables ont été ajoutées
 - pib (Produit Intérieur Brut)
 - impots 
 - dette
   
par pays x années de 2002 à 2024
   
# Fichiers additionnels pour cartographie
Pour aider à la présentation des résultats sous forme de cartes, est mis à disposition une carte au format geojson:
 - carte.geojson
   
Rappel du règlement : il est interdit de rajouter des données hormis des fonds de carte.

# Fichiers et formats
Chacun de ces répertoires contient les fichiers suivants
 - depenses_euro
 - depenses_france
 - bien_etre
---   
 - population
 - pyramide_age
---
 - pib
 - dette
 - impots
