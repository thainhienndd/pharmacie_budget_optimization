import streamlit as st
import time
from src.utils import add_new_df_line, make_graph_cumul
from src.main_dashboard import make_echeancier
from src.main_dashboard import add_salaire_to_echeancier
from src.input_parameters import salaires_path

def display_salaires():
    colf, cols = st.columns(2)
    with colf:
        st.header('Salaires')
        with st.container(border=True):
            st.session_state.salaires = st.data_editor(st.session_state.salaires, num_rows="dynamic", hide_index=True)
        col1, col2, _ = st.columns(3)
        with col1:
            if st.button('Save modifications'):
                with st.spinner():
                    time.sleep(1.5)
                    st.session_state.salaires.to_excel(salaires_path, index=False)
                    st.caption('Les salaires sont à jour !')
        with col2:
            add_salaire_module()
    with cols:
        display_graph_depense_salaire()


def add_salaire_module():
    with st.popover("Ajouter Salaire", icon="💶"):
        nom = st.text_input(label='Nom du nouvel employé ?')
        salaire_net = st.number_input(label="Montaire du salaire net (en €)")
        urssaf = st.number_input(label="Montant de l'URSSAF (en €)")
        added_salaire = {'Nom': [nom],
                         'Salaire net': [salaire_net],
                         'Urssaf': [urssaf]}
        if st.button('Add New Salaire'):
            with st.spinner():
                time.sleep(1.5)
                st.session_state.salaires = add_new_df_line(st.session_state.salaires, added_salaire)
                st.session_state.salaires.to_excel(salaires_path, index=False)
                st.caption('New line added !')


def display_graph_depense_salaire():
    echeancier = make_echeancier()
    echeancier = add_salaire_to_echeancier(echeancier)
    echeancier_g = echeancier.groupby('Date').sum().reset_index()
    echeancier_cum = echeancier_g.set_index('Date').cumsum()
    echeancier_cum = echeancier_cum.drop('salaire_total', axis=1)
    echeancier_cum['salaires_net'] = - abs(echeancier_cum['salaires_net'])
    echeancier_cum['Urssaf'] = - abs(echeancier_cum['Urssaf'])
    make_graph_cumul(echeancier_cum, 'Evolution Dépenses Salaires', ["salaires_net", "Urssaf"])
