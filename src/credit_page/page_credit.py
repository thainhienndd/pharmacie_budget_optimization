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
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns, default=['Date', 'Crédit'])
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
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
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

    return df

def page_credit():
    _, _, _, _, _, _, _, col8 = st.columns(8)

    with col8:
        with (st.popover('Catégories', icon='⚙️')):
            st.session_state.credit_categorie_list = st.data_editor(st.session_state.credit_categorie_list, hide_index=True, num_rows='dynamic')
            if st.button('Valider', key='validate_new_categ'):
                with st.spinner():
                    time.sleep(1)
                    st.session_state.credit_categorie_list.to_excel(credit_categorie_path)
                    st.caption('Catégories mises à jour !')

    st.data_editor(filter_dataframe(st.session_state['ceapc_current_credit']), hide_index=True,
                   column_config={
                       'Catégorie': st.column_config.SelectboxColumn(
                           'Catégorie',
                           width="medium",
                           options=st.session_state.credit_categorie_list.to_list(),
                           required=True,
                       ),
                       'Crédit': st.column_config.NumberColumn(
                           "Montant (€)",
                           step=1,
                           format="%d€",
                       ),
                       'Date':st.column_config.DateColumn("Date",
                                                          format="DD/MM/YYYY",
                                                          step=1)
                   }
                   )