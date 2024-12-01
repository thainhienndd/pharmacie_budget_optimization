import streamlit as st
from src.input_parameters import *
import pandas as pd
from src.main_page.popover.ceapc.ceapc_utils import read_new_ceapc
from src.main_page.popover.ceapc.ceapc_debit import ceapc_debit_processing
from src.main_page.popover.ceapc.ceapc_credit import ceapc_credit_processing


def ceapc_treatment(uploaded_file):
    ceapc_new = read_new_ceapc(uploaded_file)
    if st.session_state['operation_type'] == 'Crédit':
        ceapc_credit = st.session_state['ceapc_current_credit'].copy()
        ceapc_credit_processing(ceapc_new, ceapc_credit)
    elif st.session_state['operation_type'] == 'Débit':
        ceapc_debit = pd.read_csv(ceapc_debit_path, sep=';')
        ceapc_debit_processing(ceapc_new, ceapc_debit)




