import streamlit as st
import pandas as pd
from src.main_page.popover.ceapc.ceapc_utils import get_new_credit_debit

def ceapc_debit_processing(ceapc_new, ceapc_debit):
    new_debits, new_debits_with_categ = get_new_credit_debit(ceapc_debit, ceapc_new, is_credit=False)
    if st.button('Valider', key='validate_debit'):
        st.session_state['ceapc_debit_validated'] = True
        with st.spinner():
            new_debits_m = new_debits.drop(['Unnamed: 6', 'Crédit'], axis=1)
            new_debits_m.insert(0, 'Banque', 'CEAPC')
            new_debits_m = new_debits_m.merge(new_debits_with_categ[['Libellé', 'Fournisseur']], how='left', on='Libellé')
            ceapc_debit_new = pd.concat([new_debits_m, ceapc_debit])
            unnamed_list = [name for name in ceapc_debit_new.columns if 'Unnamed' in name]
            st.caption('Nouveaux Débiteurs identifiés !')
            if len(unnamed_list) > 0:
                ceapc_debit_new = ceapc_debit_new.drop(unnamed_list, axis = 1)
