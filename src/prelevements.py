import streamlit as st
from src.utils import add_new_df_line, preprocess_prelevements, make_graph_cumul_2
from datetime import datetime, timedelta
import time
import pandas as pd
from src.main_dashboard import make_echeancier, add_prelevements_to_echeancier
from src.input_parameters import prelevements_path

def display_prelevement():
    st.title("Prélèvements")
    preprocess_prelevements()
    with st.container(border=True):
        st.session_state.prelevements = st.data_editor(st.session_state.prelevements, num_rows="dynamic", hide_index=True)
    col1, col2, _, _, _, _ = st.columns(6)
    with col1:
        if st.button('Save modifications'):
            with st.spinner():
                time.sleep(1.5)
                st.session_state.prelevements.to_excel(prelevements_path, index=False)
                st.caption('Les prélèvements sont à jour !')
    with col2:
        add_prelevement_module()
    display_graph_depense_prelevement()

def add_prelevement_module():
    with st.popover("Ajouter Prélèvement", icon="💶"):
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
                st.session_state.prelevements.to_excel(prelevements_path, index=False)
                st.caption('New line added !')

def display_graph_depense_prelevement():
    echeancier = make_echeancier()
    echeancier = add_prelevements_to_echeancier(echeancier)
    echeancier_g = echeancier.groupby('Date').sum().reset_index()
    echeancier_cum = echeancier_g.set_index('Date').cumsum()
    make_graph_cumul_2(echeancier_cum, 'Evolution Dépenses Prélèvements', ['montant_prelevement'])
