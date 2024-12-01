import streamlit as st
from src.main_page.popover.ceapc.ceapc_utils import get_new_credit_debit
import time
import pandas as pd
from src.input_parameters import *

def ceapc_credit_processing(ceapc_new, ceapc_credit):
    new_credits, new_credits_with_categ = get_new_credit_debit(ceapc_credit, ceapc_new)
    col1, col2, _, _ = st.columns(4)
    with col1:
        if st.button('Valider', key='validate_credit'):
            with st.spinner():
                time.sleep(1)
                new_credits_m = new_credits.drop(['Unnamed: 6', 'Débit'], axis=1)
                new_credits_m.insert(0, 'Banque', 'CEAPC')
                new_credits_m = new_credits_m.merge(new_credits_with_categ[['Libellé', 'Catégorie']], how='left', on='Libellé')
                ceapc_credit_new = pd.concat([new_credits_m, ceapc_credit])
                unnamed_list = [name for name in ceapc_credit_new.columns if 'Unnamed' in name]
                if len(unnamed_list) > 0:
                    ceapc_credit_new = ceapc_credit_new.drop(unnamed_list, axis = 1)
                st.session_state['operation_type'] = 'Débit'
                st.caption('Nouveaux Créditeurs identifiés !')
                with col2:
                    if st.button('Passer au débit', key='pass_to_debit'):
                        print('')
                save_ceapc_credit(ceapc_credit_new)
                return ceapc_credit_new


def save_ceapc_credit(ceapc_credit_new):
    st.session_state.ceapc_current_credit = ceapc_credit_new
    st.session_state.ceapc_current_credit['Date'] = pd.to_datetime(st.session_state.ceapc_current_credit['Date'])
    st.session_state.ceapc_current_credit.to_csv(ceapc_credit_path, sep=';', index=False)
    st.session_state.ceapc_current_credit = pd.read_csv(ceapc_credit_path, sep=';')