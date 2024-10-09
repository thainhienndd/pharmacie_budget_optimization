import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd


def add_new_df_line(df, dict_new_line):
    new_line = pd.DataFrame(data=dict_new_line)
    updated_df = pd.concat([df, new_line])
    return updated_df

def preprocess_prelevements():
    st.session_state.prelevements['montant_prelevement'] = - abs(st.session_state.prelevements['montant_prelevement'].apply(
        lambda x: float(str(x).replace(',', '.').replace('€', '').replace(' ', ''))))
    st.session_state.prelevements['Date'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Date']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.prelevements['Echéance'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Echéance']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.prelevements['Date de paiement'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Date de paiement']).dt.strftime('%Y-%m-%d')).dt.date

def make_graph_cumul_2(echeancier_cum, title, y_columns):
    st.header(title)
    with st.container():
        # Créer une figure vide pour les aires empilées
        fig = go.Figure()

        # Définir des couleurs pour les positifs (vert) et négatifs (rouge) avec des dégradés
        positive_colors = [
            "rgba(255,255,224,0.6)",  # Vert foncé
            "rgba(102,194,165,0.6)",  # Vert moyen
            "rgba(255,255,224,0.6)"  # Vert clair
        ]

        # Couleurs rouges adoucies
        negative_colors = [
            "rgba(255,99,71,0.6)",  # Tomate (Tomato), plus doux
            "rgba(255,160,122,0.6)",  # Light Salmon
            "rgba(255,99,71,0.6)"  # Tomate (Tomato) (utilisé deux fois)
        ]

        # Ajouter chaque série en tant qu'aire empilée avec des couleurs dynamiques
        for idx, y in enumerate(y_columns):
            values = echeancier_cum[y]
            # Sélectionner la couleur en fonction de la valeur
            fillcolor = positive_colors[idx % len(positive_colors)] if values.max() > 0 else negative_colors[
                idx % len(negative_colors)]

            fig.add_trace(go.Scatter(
                x=echeancier_cum.index,
                y=values,
                mode='lines',
                stackgroup='one',  # Stack les aires pour un graphique empilé
                line=dict(width=2.5, color="rgba(0, 0, 0, 0.5)"),  # Augmenter l'épaisseur du trait
                fill='tozeroy',
                fillcolor=fillcolor,
                hoverinfo='x+y+z',  # Masquer les informations sur cette trace au survol
                name=y,
            ))

        # Calculer la somme cumulée des dépenses
        somme_cumulee = echeancier_cum[y_columns].sum(axis=1)

        # Ajouter une trace pour la somme cumulée totale pour l'afficher au survol
        fig.add_trace(go.Scatter(
            x=echeancier_cum.index,
            y=somme_cumulee,
            mode='lines',
            line=dict(width=4, color='rgba(0, 102, 204, 1)'),  # Couleur bleu vif pour la somme cumulée
            hovertemplate='%{x}<br>%{y:.0f} €',
            name='Trésorerie globale'
        ))

        # Trouver la première date où la somme devient négative
        date_passe_negatif = somme_cumulee[somme_cumulee < 0].index.min()

        # Ajouter un marqueur si la somme passe en négatif à une date donnée
        if date_passe_negatif == date_passe_negatif:
            somme_a_date = somme_cumulee.loc[date_passe_negatif]

            # Ajouter un point entouré à la date où la somme devient négative
            fig.add_trace(go.Scatter(
                x=[date_passe_negatif],
                y=[somme_a_date],
                mode='markers+text',
                marker=dict(size=15, color='blue', symbol='circle-open'),
                text=[f'{date_passe_negatif.strftime("%Y-%m-%d")}'],
                textposition="top right",
                textfont=dict(size=13, weight='bold', color='blue'),
                name='Passage en négatif'
            ))

        # Mise en forme de la figure
        fig.update_layout(
            title="Évolution des Dépenses",
            xaxis_title="Date",
            yaxis_title="Montants cumulés",
            template="plotly_dark",
            hovermode="x unified",
            margin=dict(l=40, r=40, t=40, b=40),
            legend_title_text="Sources de flux financiers"
        )

        # Intégrer le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)
