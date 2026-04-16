from datetime import date
from finances.services.compte_service import CompteService
from finances.services.transaction_service import TransactionService
from finances.services.budget_service import BudgetService
from finances.utils.calculators import FinanceCalculator


class DashboardService:

    @staticmethod
    def get_dashboard_data(user):
        aujourd_hui = date.today()
        mois = aujourd_hui.month
        annee = aujourd_hui.year

        # Solde total de tous les comptes
        solde_total = CompteService.get_solde_total(user)

        # Liste de tous les comptes actifs
        comptes = CompteService.get_comptes_user(user)

        # Bilan du mois en cours
        bilan = TransactionService.get_bilan_mensuel(user, mois, annee)

        # 5 dernières transactions
        dernieres_transactions = TransactionService.get_transactions_user(
            user,
            filters={'annee': annee, 'mois': mois}
        )[:5]

        # Dépenses par catégorie du mois
        depenses_par_categorie = FinanceCalculator.calculer_depenses_par_categorie(
            user, mois, annee
        )

        # État de tous les budgets du mois
        etat_budgets = BudgetService.get_etat_tous_budgets(user, mois, annee)

        return {
            'utilisateur': user.username,
            'date_aujourdhui': aujourd_hui,
            'mois_en_cours': mois,
            'annee_en_cours': annee,
            'solde_total': solde_total,
            'comptes': comptes,
            'bilan_mensuel': bilan,
            'dernieres_transactions': dernieres_transactions,
            'depenses_par_categorie': depenses_par_categorie,
            'etat_budgets': etat_budgets,
        }