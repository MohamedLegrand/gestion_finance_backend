from decimal import Decimal
from django.db.models import Sum
from finances.models.budget_model import Budget
from finances.models.transaction_model import Transaction


class BudgetService:

    @staticmethod
    def get_budgets_user(user, mois=None, annee=None):
        queryset = Budget.objects.filter(user=user)

        if mois:
            queryset = queryset.filter(mois=mois)

        if annee:
            queryset = queryset.filter(annee=annee)

        return queryset

    @staticmethod
    def get_budget_by_id(user, budget_id):
        try:
            return Budget.objects.get(id=budget_id, user=user)
        except Budget.DoesNotExist:
            return None

    @staticmethod
    def creer_budget(user, categorie, montant_limite, mois, annee):

        # Vérifier qu'un budget n'existe pas déjà
        # pour cette catégorie ce mois-ci
        budget_existant = Budget.objects.filter(
            user=user,
            categorie=categorie,
            mois=mois,
            annee=annee
        ).exists()

        if budget_existant:
            raise ValueError(
                f"Un budget existe déjà pour la catégorie "
                f"{categorie.nom} en {mois}/{annee}."
            )

        # Vérifier que la catégorie est bien une dépense
        if categorie.type != 'depense':
            raise ValueError(
                "Un budget ne peut être créé que pour "
                "une catégorie de type dépense."
            )

        budget = Budget.objects.create(
            user=user,
            categorie=categorie,
            montant_limite=Decimal(str(montant_limite)),
            mois=mois,
            annee=annee
        )

        return budget

    @staticmethod
    def modifier_budget(budget, montant_limite):
        budget.montant_limite = Decimal(str(montant_limite))
        budget.save()
        return budget

    @staticmethod
    def supprimer_budget(budget):
        budget.delete()

    @staticmethod
    def get_montant_depense(budget):
        result = Transaction.objects.filter(
            user=budget.user,
            categorie=budget.categorie,
            type='depense',
            date__month=budget.mois,
            date__year=budget.annee
        ).aggregate(total=Sum('montant'))

        return result['total'] or Decimal('0')

    @staticmethod
    def get_montant_restant(budget):
        montant_depense = BudgetService.get_montant_depense(budget)
        restant = budget.montant_limite - montant_depense
        return max(restant, Decimal('0'))

    @staticmethod
    def get_pourcentage_utilise(budget):
        montant_depense = BudgetService.get_montant_depense(budget)
        if budget.montant_limite == 0:
            return Decimal('0')
        pourcentage = (montant_depense / budget.montant_limite) * 100
        return round(pourcentage, 2)

    @staticmethod
    def verifier_alertes(budget):
        alertes = []
        pourcentage = BudgetService.get_pourcentage_utilise(budget)

        # Vérifier seuil 80%
        if pourcentage >= 80 and not budget.alerte_80:
            budget.alerte_80 = True
            budget.save()
            alertes.append({
                'type': 'warning',
                'message': f"Attention ! Tu as utilisé {pourcentage}% "
                           f"de ton budget {budget.categorie.nom} "
                           f"pour {budget.mois}/{budget.annee}."
            })

        # Vérifier seuil 100%
        if pourcentage >= 100 and not budget.alerte_100:
            budget.alerte_100 = True
            budget.save()
            alertes.append({
                'type': 'danger',
                'message': f"Budget {budget.categorie.nom} dépassé ! "
                           f"Tu as dépensé {pourcentage}% de ton budget "
                           f"pour {budget.mois}/{budget.annee}."
            })

        return alertes

    @staticmethod
    def get_etat_budget(budget):
        montant_depense = BudgetService.get_montant_depense(budget)
        montant_restant = BudgetService.get_montant_restant(budget)
        pourcentage = BudgetService.get_pourcentage_utilise(budget)
        alertes = BudgetService.verifier_alertes(budget)

        return {
            'budget_id': budget.id,
            'categorie': budget.categorie.nom,
            'mois': budget.mois,
            'annee': budget.annee,
            'montant_limite': budget.montant_limite,
            'montant_depense': montant_depense,
            'montant_restant': montant_restant,
            'pourcentage_utilise': pourcentage,
            'alertes': alertes,
        }

    @staticmethod
    def get_etat_tous_budgets(user, mois, annee):
        budgets = BudgetService.get_budgets_user(user, mois, annee)
        return [BudgetService.get_etat_budget(budget) for budget in budgets]