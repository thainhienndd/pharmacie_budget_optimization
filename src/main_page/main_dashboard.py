from src.old.utils import make_graph_cumul_2
from src.main_page.graph_treso import *
from src.main_page.popover.popover_upload import popover_uploader

def get_initial_tresorery():
    return 40000

def main_dashboard_page():
    popover_uploader()
    echeancier = make_echeancier()
    echeancier = add_salaire_to_echeancier(echeancier)
    echeancier = add_factures_to_echeancier(echeancier)
    echeancier = add_prelevements_to_echeancier(echeancier)
    echeancier_cum = group_echeancier_per_depense(echeancier)
    initial_tresory = get_initial_tresorery()
    echeancier_cum['Trésorerie'] = initial_tresory
    make_graph_cumul_2(echeancier_cum, "Main Dashboard",['Trésorerie', "Salaires", "Prélèvements", "Factures"])
