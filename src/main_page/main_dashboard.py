from src.utils import make_graph_cumul_2
from io import StringIO
from src.input_parameters import *
from src.main_page.graph_treso import *
import time

credit_option_list = ['Caisses et mutuelles', 'CB', 'Espèces', 'Chéques', 'Clients', 'Laboratoires',
                      'A définir ultérieurement']

def get_initial_tresorery():
    return 40000

def popover_uploader():
    col1, col2 = st.columns(2)
    with col1:
        with st.popover('🗂 Déposer les nouveaux fichiers', use_container_width=True):
            file_type = st.selectbox('Type de Fichier', ['CEAPC', 'CIC', 'DigiPharmacie'])
            uploaded_file = st.file_uploader('Déposer le fichier', accept_multiple_files=False)
            if uploaded_file is not None:
                if file_type=='CEAPC':
                    ceapc_new = read_new_ceapc(uploaded_file)
                    if st.session_state['operation_type'] == 'Crédit':
                        ceapc_credit = st.session_state['ceapc_current_credit'].copy()
                        ceapc_credit_processing(ceapc_new, ceapc_credit)
                    elif st.session_state['operation_type'] == 'Débit':
                        ceapc_debit = pd.read_csv(ceapc_debit_path, sep=';')
                        ceapc_debit_processing(ceapc_new, ceapc_debit)

def ceapc_debit_processing(ceapc_new, ceapc_debit):
    new_debits, new_debits_with_categ = get_new_credit_debit(ceapc_debit, ceapc_new, is_credit=False)
    if st.button('Valider', key='validate_debit'):
        with st.spinner():
            new_debits_m = new_debits.drop(['Unnamed: 6', 'Crédit'], axis=1)
            new_debits_m.insert(0, 'Banque', 'CEAPC')
            new_debits_m = new_debits_m.merge(new_debits_with_categ[['Libellé', 'Fournisseur']], how='left', on='Libellé')
            ceapc_credit_new = pd.concat([new_debits_m, ceapc_debit])
            unnamed_list = [name for name in ceapc_credit_new.columns if 'Unnamed' in name]
            if len(unnamed_list) > 0:
                ceapc_credit_new = ceapc_credit_new.drop(unnamed_list, axis = 1)


def ceapc_credit_processing(ceapc_new, ceapc_credit):
    new_credits, new_credits_with_categ = get_new_credit_debit(ceapc_credit, ceapc_new)
    col1, col2, _, _ = st.columns(4)
    with col1:
        if st.button('Valider', key='validate_credit'):
            with st.spinner():
                time.sleep(1)
                new_credits_m = new_credits.drop(['Unnamed: 6', 'Débit'], axis=1)
                new_credits_m.insert(0, 'Banque', 'CEAPC')
                new_credits_m = new_credits_m.merge(new_credits_with_categ[['Libellé', 'Catégorie']], how='left', on='Libellé')
                ceapc_credit_new = pd.concat([new_credits_m, ceapc_credit])
                unnamed_list = [name for name in ceapc_credit_new.columns if 'Unnamed' in name]
                if len(unnamed_list) > 0:
                    ceapc_credit_new = ceapc_credit_new.drop(unnamed_list, axis = 1)
                st.session_state['operation_type'] = 'Débit'
                with col2:
                    if st.button('Passer au débit', key='pass_to_debit'):
                        print('')

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
            options=credit_option_list,
            required=True,
        ),
        operation_type_name: st.column_config.NumberColumn(
            "Montant (€)",
            step=1,
            format="%d€",
        )
    }, hide_index=True)
    return new_credits, new_credits_with_categ


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


def main_dashboard():
    popover_uploader()
    echeancier = make_echeancier()
    echeancier = add_salaire_to_echeancier(echeancier)
    echeancier = add_factures_to_echeancier(echeancier)
    echeancier = add_prelevements_to_echeancier(echeancier)
    echeancier_cum = group_echeancier_per_depense(echeancier)
    initial_tresory = get_initial_tresorery()
    echeancier_cum['Trésorerie'] = initial_tresory
    make_graph_cumul_2(echeancier_cum, "Main Dashboard",['Trésorerie', "Salaires", "Prélèvements", "Factures"])
