import streamlit as st
import pandas as pd
from input_parameters import *

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

def initialize_streamlit():
    if 'factures' not in st.session_state:
        st.session_state.factures = pd.read_excel(factures_path)
    if 'salaires' not in st.session_state:
        st.session_state.salaires = pd.read_excel(salaires_path)
    if 'prelevements' not in st.session_state:
        st.session_state.prelevements = pd.read_excel(prelevements_path)