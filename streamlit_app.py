import streamlit as st
from streamlit_option_menu import option_menu
from src.init_streamlit import initialize_streamlit
from src.main_page.main_dashboard import main_dashboard_page
from src.credit_page.page_credit import page_credit
from src.authentification_page.page_authentification import authenticator_page
from src.debit_page.page_debit import page_debit

st.set_page_config(layout='wide')

hide_decoration_bar_style = '''
    <style>
        header {visibility:hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-right: 10rem;
            }
        </style>
""", unsafe_allow_html=True)

authenticator = authenticator_page()
if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')
    initialize_streamlit()

    with st.sidebar:
        selected_main = option_menu(None, ["Home", 'Crédit', 'Débit'],
            icons=['house', 'bank', 'bank2'], menu_icon="cast", default_index=0)

        if selected_main == 'Paramètres':
            selected_main = option_menu('Parameters', ['Salaires', 'Factures', 'Prélèvements'])


    if selected_main == 'Home':
        main_dashboard_page()

    if selected_main == 'Crédit':
        page_credit()

    if selected_main == 'Débit':
        page_debit()

    st.markdown(
        """<hr>
        <p style="text-align: left; font-size: medium;">
        <b>SIREN:</b> XXX
        </p>
        """, unsafe_allow_html=True
    )
