import streamlit as st
from utils import add_new_df_line
from datetime import datetime, timedelta
import time
import pandas as pd

def display_facture():
    st.title("Factures")
    preprocess_factures()
    with st.container(border=True):
        st.session_state.factures = st.data_editor(st.session_state.factures, num_rows="dynamic", hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Save modifications'):
            with st.spinner():
                time.sleep(1.5)
                st.session_state.factures.to_excel('../data/sorties/factures.xlsx', index=False)
                st.caption('Les factures sont à jour !')
    with col2:
        add_facture_module()

def add_facture_module():
    with st.popover("Ajouter Une Facture", icon="💶"):
        fournisseur = st.selectbox(label='Est-ce un fournisseur ?', options=['oui', 'non'])
        entite = st.selectbox(label="Quelle est l'entité concernée ?",
                              options=st.session_state.factures['Entité'].unique())
        echeance = st.date_input("Echéance de la facture ?")
        libelle = st.text_input(label="Entrer le libellé")
        is_facture = st.selectbox(label="Y'a t'il une facture ?", options=['oui', 'non'])
        montant = st.number_input(label='Montant de la facture (€) ?')
        added_facture = {'Date': [datetime.today().strftime('%Y-%m-%d')],
                         'Echéance': [echeance.strftime('%Y-%m-%d')],
                         'Fournisseur': [fournisseur],
                         'Entité': [entite],
                         'Libellée': [libelle],
                         'Facture': [is_facture],
                         'montant_facture': [montant],
                         'Payé': ['non'],
                         'Date de paiement': [(echeance - timedelta(days=3)).strftime('%Y-%m-%d')]}
        if st.button('Add New Facture'):
            with st.spinner():
                time.sleep(1.5)
                st.session_state.factures = add_new_df_line(st.session_state.factures, added_facture)
                st.session_state.factures.to_excel('../data/sorties/factures.xlsx', index=False)
                st.caption('New line added !')

def preprocess_factures():
    st.session_state.factures['montant_facture'] = st.session_state.factures['montant_facture'].apply(
        lambda x: float(str(x).replace(',', '.').replace('€', '').replace(' ', '')))
    st.session_state.factures['Date'] = pd.to_datetime(pd.to_datetime(st.session_state.factures['Date']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.factures['Echéance'] = pd.to_datetime(pd.to_datetime(st.session_state.factures['Echéance']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.factures['Date de paiement'] = pd.to_datetime(pd.to_datetime(st.session_state.factures['Date de paiement']).dt.strftime('%Y-%m-%d')).dt.date
