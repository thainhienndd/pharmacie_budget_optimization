import streamlit as st
import pandas as pd


def initialize_streamlit():
    if 'factures' not in st.session_state:
        st.session_state.factures = pd.read_excel('../data/sorties/factures.xlsx')
    if 'salaires' not in st.session_state:
        st.session_state.salaires = pd.read_excel('../data/sorties/salaires.xlsx')
    if 'prelevements' not in st.session_state:
        st.session_state.prelevements = pd.read_excel('../data/sorties/prelevements.xlsx')