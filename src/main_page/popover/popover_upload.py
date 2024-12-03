import streamlit as st
from src.main_page.popover.ceapc.ceapc_upload import ceapc_treatment


def popover_uploader():
    col1, col2 = st.columns(2)
    with col1:
        with st.popover('🗂 Déposer les nouveaux fichiers', use_container_width=True):
            file_type = st.selectbox('Type de Fichier', ['CEAPC', 'CIC', 'DigiPharmacie'])
            st.session_state.uploaded_file = st.file_uploader('Déposer le fichier', accept_multiple_files=False)
            if st.session_state.uploaded_file is not None:
                if file_type=='CEAPC':
                    ceapc_treatment(st.session_state.uploaded_file)
