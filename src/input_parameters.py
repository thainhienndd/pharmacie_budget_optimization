is_local = False

if is_local:
    prefix_path = '../data/'
else:
    prefix_path = '/mount/src/pharmacie_budget_optimization/data/'

factures_path = prefix_path + 'sorties/factures.xlsx'
salaires_path = prefix_path + 'sorties/salaires.xlsx'
prelevements_path = prefix_path + 'sorties/prelevements.xlsx'