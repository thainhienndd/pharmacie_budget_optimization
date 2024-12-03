is_local = False

if is_local:
    prefix_path = 'data/'
else:
    prefix_path = 'data/' #'thainhienndd/pharmacie_budget_optimization/master/data/'

factures_path = prefix_path + 'sorties/factures.xlsx'
salaires_path = prefix_path + 'sorties/salaires.xlsx'
prelevements_path = prefix_path + 'sorties/prelevements.xlsx'

ceapc_credit_path = 'data/banques/CEAPC/CEAPC_current_credit.csv'
ceapc_debit_path = 'data/banques/CEAPC/CEAPC_current_debit.csv'

credit_categorie_path = 'data/parameters_lists/liste_categorie.xlsx'
debit_fournisseur_path = 'data/parameters_lists/liste_fournisseurs.xlsx'