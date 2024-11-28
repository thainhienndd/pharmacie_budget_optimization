import streamlit as st
import pandas as pd
from src.input_parameters import *

def initialize_streamlit():
    if 'factures' not in st.session_state:
        st.session_state.factures = pd.read_excel(factures_path)
    if 'salaires' not in st.session_state:
        st.session_state.salaires = pd.read_excel(salaires_path)
    if 'prelevements' not in st.session_state:
        st.session_state.prelevements = pd.read_excel(prelevements_path)
    if 'operation_type' not in st.session_state:
        st.session_state.operation_type = 'Crédit'
    if 'ceapc_current_credit' not in st.session_state:
        st.session_state.ceapc_current_credit = pd.read_csv(ceapc_credit_path, sep=';')
        unnamed_list = [name for name in st.session_state.ceapc_current_credit.columns if 'Unnamed' in name]
        if len(unnamed_list) > 0:
            st.session_state.ceapc_current_credit = st.session_state.ceapc_current_credit.drop(unnamed_list, axis=1)

