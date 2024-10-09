import pandas as pd
import streamlit as st
import plotly.express as px


def add_new_df_line(df, dict_new_line):
    new_line = pd.DataFrame(data=dict_new_line)
    updated_df = pd.concat([df, new_line])
    return updated_df

def make_graph_cumul(echeancier_cum, title, y_columns):
    st.header(title)
    with st.container(border=True):
        fig = px.area(
            echeancier_cum,
            x=echeancier_cum.index,  # Assumant que l'index est la colonne des dates
            y=y_columns,
            labels={"value": "Montants cumulés", "x": "Date"},
            title="Évolution des Dépenses",
            template="plotly_dark",  # Thème sombre pour une meilleure esthétique
            color_discrete_sequence=px.colors.sequential.Viridis  # Palette de couleurs améliorée
        )

        # Améliorations de mise en forme
        fig.update_layout(
            legend_title_text="Sources de flux financiers",
            xaxis_title="Date",
            yaxis_title="Montants cumulés",
            hovermode="x unified",  # Montrer toutes les valeurs lorsque l'on survole une date
            margin=dict(l=40, r=40, t=40, b=40),
        )

        # Intégrer le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)  # Rendre le graphique responsive

def preprocess_prelevements():
    st.session_state.prelevements['montant_prelevement'] = - abs(st.session_state.prelevements['montant_prelevement'].apply(
        lambda x: float(str(x).replace(',', '.').replace('€', '').replace(' ', ''))))
    st.session_state.prelevements['Date'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Date']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.prelevements['Echéance'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Echéance']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.prelevements['Date de paiement'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Date de paiement']).dt.strftime('%Y-%m-%d')).dt.date
