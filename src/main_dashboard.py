import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from prelevements import preprocess_prelevements

jour_prelevement = 1


def main_dashboard():
    echeancier = make_echeancier()
    echeancier = add_salaire_to_echeancier(echeancier)
    echeancier = add_factures_to_echeancier(echeancier)
    echeancier = add_prelevements_to_echeancier(echeancier)
    echeancier_cum = group_echeancier_per_depense(echeancier)
    build_cumulative_graph(echeancier_cum)


def make_echeancier():
    start_date = datetime.today()
    date_range = [start_date + timedelta(days=x) for x in range(100)]
    echeancier = pd.DataFrame(date_range, columns=['Date'])
    echeancier['Date'] = echeancier['Date'].dt.date
    return echeancier

def add_salaire_to_echeancier(echeancier):
    st.session_state.salaires['salaire_total'] = - abs(st.session_state.salaires['Salaire net'] + st.session_state.salaires['Urssaf'])
    salaires_net_total = st.session_state.salaires['Salaire net'].sum()
    urssaf_total = st.session_state.salaires['Urssaf'].sum()
    salaires_total = st.session_state.salaires['salaire_total'].sum()
    echeancier['salaires_net'] = echeancier['Date'].apply(lambda x: salaires_net_total if x.day == jour_prelevement else None)
    echeancier['Urssaf'] = echeancier['Date'].apply(lambda x: urssaf_total if x.day == jour_prelevement else None)
    echeancier['salaire_total'] = echeancier['Date'].apply(lambda x: salaires_total if x.day == jour_prelevement else None)
    return echeancier

def add_factures_to_echeancier(echeancier):
    st.session_state.factures['montant_facture'] = - abs(st.session_state.factures['montant_facture'].apply(
        lambda x: float(str(x).replace(',', '.').replace('€', '').replace(' ', ''))))
    st.session_state.factures['Date'] = pd.to_datetime(pd.to_datetime(st.session_state.factures['Date']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.factures['Echéance'] = pd.to_datetime(pd.to_datetime(st.session_state.factures['Echéance']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.factures['Date de paiement'] = pd.to_datetime(
        pd.to_datetime(st.session_state.factures['Date de paiement']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.factures['Date paiement attendue'] = st.session_state.factures['Echéance'].apply(lambda x: x - timedelta(days=3))
    factures_not_payed = st.session_state.factures[st.session_state.factures['Payé'] == 'non']
    echeancier = echeancier.merge(factures_not_payed[['Date paiement attendue', 'montant_facture']],
                                  left_on='Date', right_on='Date paiement attendue', how='left')
    echeancier = echeancier.drop('Date paiement attendue', axis=1)
    return echeancier

def add_prelevements_to_echeancier(echeancier):
    preprocess_prelevements()
    st.session_state.prelevements['Date paiement attendue'] = st.session_state.prelevements['Echéance'].apply(lambda x: x - timedelta(days=3))
    prelevements_not_payed = st.session_state.prelevements[st.session_state.prelevements['Payé'] == 'non']
    echeancier = echeancier.merge(prelevements_not_payed[['Date paiement attendue', 'montant_prelevement']],
                                  left_on='Date', right_on='Date paiement attendue', how='left')
    echeancier = echeancier.drop('Date paiement attendue', axis=1)
    return echeancier

def group_echeancier_per_depense(echeancier):
    echeancier_g = echeancier.groupby('Date').sum().reset_index()
    echeancier_cum = echeancier_g.set_index('Date').cumsum()
    echeancier_cum_min = echeancier_cum.drop(['salaires_net', 'Urssaf'], axis=1)
    return echeancier_cum_min

def build_cumulative_graph(echeancier_cum):
    st.header("Main Dashboard")

    fig = px.area(
        echeancier_cum,
        x=echeancier_cum.index,  # Assumant que l'index est la colonne des dates
        y=["salaire_total", "montant_prelevement", "montant_facture"],
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