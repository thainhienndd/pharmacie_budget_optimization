from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import time
from src.input_parameters import *
from datetime import datetime


def page_debit():
    display_monthly_debit()


    modify_categories_parameters()
    st.subheader('Filtres')

    filtered_ceapc_debit = show_filtered_debit_sum()
    show_filtered_dataframe(filtered_ceapc_debit)


def display_monthly_debit():
    st.title('Débit')
    # return formated_number_m_credit_, month, year


def show_filtered_dataframe(filtered_ceapc_credit):
    st.data_editor(filtered_ceapc_credit, hide_index=True,
                   column_config={
                       'Fournisseur': st.column_config.SelectboxColumn(
                           'Fournisseur',
                           width="medium",
                           options=st.session_state.debit_fournisseur_list.to_list(),
                           required=True,
                       ),
                       'Débit': st.column_config.NumberColumn(
                           "Montant (€)",
                           step=1,
                           format="%d€",
                       ),
                       'Date': st.column_config.DateColumn("Date",
                                                           format="DD/MM/YYYY",
                                                           step=1)
                   }
                   )


def modify_categories_parameters():
    _, _, _, _, _, _, _, col8 = st.columns(8)
    with col8:
        with (st.popover('Fournisseur', icon='⚙️')):
            st.session_state.debit_fournisseur_list = st.data_editor(st.session_state.debit_fournisseur_list,
                                                                    hide_index=True, num_rows='dynamic')
            if st.button('Valider', key='validate_new_fourni'):
                with st.spinner():
                    time.sleep(1)
                    st.session_state.debit_fournisseur_list.to_excel(debit_fournisseur_path)
                    st.caption('Fournisseurs mises à jour !')


def show_filtered_debit_sum():
    filtered_ceapc_debit = filter_dataframe(st.session_state['ceapc_current_debit'])

    filtered_total_credit = int(filtered_ceapc_debit['Débit'].sum())
    formated_number_total_debit = '{:,}'.format(filtered_total_credit).replace(',', ' ')
    st.write(f"Total des débits sur les critères de recherches : **{formated_number_total_debit}**€")
    return filtered_ceapc_debit



def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container(border=True)
    with modification_container:
        to_filter_columns = st.multiselect("Filtrer les résultats par rapport à", df.columns, default=['Date', 'Débit'])
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Valeur du {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    format="%d€",
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Dates",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    st.subheader('Tableau des débits')

    return df
