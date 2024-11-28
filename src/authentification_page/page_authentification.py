import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st

def authenticator_page():
    with open('data/authentification/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    # stauth.Hasher.hash_passwords(config['credentials'])

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    if st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')
    return authenticator