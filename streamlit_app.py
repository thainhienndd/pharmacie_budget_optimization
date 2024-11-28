import streamlit as st
from streamlit_option_menu import option_menu
from src.init_streamlit import initialize_streamlit
from src.main_page.main_dashboard import main_dashboard
from src.credit_page.page_credit import page_credit
from src.salaires import display_salaires
from src.prelevements import display_prelevement
from src.factures import display_facture

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


initialize_streamlit()

with st.sidebar:
    selected_main = option_menu(None, ["Home", 'Crédit'],
        icons=['house', 'bank', 'gear'], menu_icon="cast", default_index=0)

    if selected_main == 'Paramètres':
        selected_main = option_menu('Parameters', ['Salaires', 'Factures', 'Prélèvements'])


if selected_main == 'Home':
    main_dashboard()

if selected_main == 'Crédit':
    page_credit()

# if selected_main == 'Factures':
#     display_facture()
#
# if selected_main == 'Salaires':
#     display_salaires()
#
# if selected_main == 'Prélèvements':
#     display_prelevement()