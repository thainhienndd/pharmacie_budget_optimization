from io import StringIO
import pandas as pd
import streamlit as st


def read_new_ceapc(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("latin-1"))
    ceapc_new = pd.read_csv(stringio, skiprows=4, sep=';', skipfooter=1,
                            engine='python')
    ceapc_new['Date'] = pd.to_datetime(ceapc_new['Date'])
    ceapc_new['Crédit'] = ceapc_new['Crédit'].apply(
        lambda x: float(str(x).replace('+', '').replace(',', '.')))
    ceapc_new['Débit'] = ceapc_new['Débit'].apply(
        lambda x: float(str(x).replace('+', '').replace(',', '.')))
    ceapc_new['Crédit'] = ceapc_new['Crédit'].apply(lambda x: round(x, 0))
    ceapc_new['Débit'] = ceapc_new['Débit'].apply(lambda x: round(x, 0))
    return ceapc_new

def get_new_credit_debit(ceapc, ceapc_new, is_credit=True):
    if is_credit:
        operation_type_name = 'Crédit'
        colname_operation = 'Catégorie'
    else:
        operation_type_name = 'Débit'
        colname_operation = 'Fournisseur'

    new_credits = ceapc_new[
        (~ceapc_new['Numéro d\'opération'].isin(ceapc['Numéro d\'opération'].unique())) &
        (ceapc_new[operation_type_name].notna())]

    new_credits_g = new_credits.groupby(['Libellé']).agg(
        {operation_type_name: sum, "Numéro d'opération": 'nunique'}).reset_index().sort_values(by=operation_type_name,
                                                                                    ascending=not is_credit)
    new_credits_g = new_credits_g.rename({"Numéro d'opération": "Nombre d'opérations"}, axis=1)
    new_credits_g[colname_operation] = ''
    st.title('Nouveaux ' + operation_type_name + 'eurs identifiés')
    new_credits_with_categ = st.data_editor(new_credits_g, column_config={
        colname_operation: st.column_config.SelectboxColumn(
            colname_operation,
            width="medium",
            options=st.session_state.credit_categorie_list.to_list(),
            required=True,
        ),
        operation_type_name: st.column_config.NumberColumn(
            "Montant (€)",
            step=1,
            format="%d€",
        )
    }, hide_index=True)
    return new_credits, new_credits_with_categ
