import streamlit as st
from utils import add_new_df_line
from datetime import datetime, timedelta
import time
import pandas as pd

def display_prelevement():
    st.title("Prélèvements")
    preprocess_prelevements()
    with st.container(border=True):
        st.session_state.prelevements = st.data_editor(st.session_state.prelevements, num_rows="dynamic", hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Save modifications'):
            with st.spinner():
                time.sleep(1.5)
                st.session_state.prelevements.to_excel('../data/sorties/prelevements.xlsx', index=False)
                st.caption('Les prélèvements sont à jour !')
    with col2:
        add_prelevement_module()

def add_prelevement_module():
    with st.popover("Ajouter Un Prélèvement", icon="💶"):
        fournisseur = st.selectbox(label='Est-ce un fournisseur ?', options=['oui', 'non'])
        entite = st.selectbox(label="Quelle est l'entité concernée ?",
                              options=st.session_state.prelevements['Entité'].unique())
        echeance = st.date_input("Echéance du prélèvement ?")
        libelle = st.text_input(label="Entrer le libellé")
        montant = st.number_input(label='Montant du prélèvement (€) ?')
        added_prelevement = {'Date': [datetime.today().strftime('%Y-%m-%d')],
                         'Echéance': [echeance.strftime('%Y-%m-%d')],
                         'Fournisseur': [fournisseur],
                         'Entité': [entite],
                         'Libellée': [libelle],
                         'montant_prelevement': [montant],
                         'Payé': ['non'],
                         'Date de paiement': [(echeance - timedelta(days=3)).strftime('%Y-%m-%d')]}
        if st.button('Add New prelevement'):
            with st.spinner():
                time.sleep(1.5)
                st.session_state.prelevements = add_new_df_line(st.session_state.prelevements, added_prelevement)
                st.session_state.prelevements.to_excel('../data/sorties/prelevements.xlsx', index=False)
                st.caption('New line added !')

def preprocess_prelevements():
    st.session_state.prelevements['montant_prelevement'] = - abs(st.session_state.prelevements['montant_prelevement'].apply(
        lambda x: float(str(x).replace(',', '.').replace('€', '').replace(' ', ''))))
    st.session_state.prelevements['Date'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Date']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.prelevements['Echéance'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Echéance']).dt.strftime('%Y-%m-%d')).dt.date
    st.session_state.prelevements['Date de paiement'] = pd.to_datetime(pd.to_datetime(st.session_state.prelevements['Date de paiement']).dt.strftime('%Y-%m-%d')).dt.date
