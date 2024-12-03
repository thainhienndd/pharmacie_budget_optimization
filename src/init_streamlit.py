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
    if 'ceapc_current_debit' not in st.session_state:
        st.session_state.ceapc_current_debit = pd.read_csv(ceapc_debit_path, sep=';')
        unnamed_list = [name for name in st.session_state.ceapc_current_credit.columns if 'Unnamed' in name]
        if len(unnamed_list) > 0:
            st.session_state.ceapc_current_debit = st.session_state.ceapc_current_debit.drop(unnamed_list, axis=1)
    if 'credit_cateogrie_list' not in st.session_state:
        st.session_state.credit_categorie_list = pd.read_excel(credit_categorie_path)['credit_categorie']
    if 'debit_fournisseur_list' not in st.session_state:
        st.session_state.debit_fournisseur_list = pd.read_excel(debit_fournisseur_path)['debit_fournisseurs']
    if 'debit_ceapc_validated' not in st.session_state:
        st.session_state.debit_ceapc_validated = 'False'
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'ceapc_completed' not in st.session_state:
        st.session_state.ceapc_completed = False
