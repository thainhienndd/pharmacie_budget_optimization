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