from decimal import Decimal
from django.db.models import Sum
from finances.models.transaction_model import Transaction
from finances.models.compte_model import Compte


class FinanceCalculator:

    @staticmethod
    def calculer_solde_total(user):
        comptes = Compte.objects.filter(user=user, actif=True)
        total = Decimal('0')
        for compte in comptes:
            total += compte.solde
        return total

    @staticmethod
    def calculer_total_par_type(user, type_transaction, mois, annee):
        result = Transaction.objects.filter(
            user=user,
            type=type_transaction,
            date__month=mois,
            date__year=annee
        ).aggregate(total=Sum('montant'))
        return result['total'] or Decimal('0')

    @staticmethod
    def calculer_epargne_mensuelle(user, mois, annee):
        total_revenus = FinanceCalculator.calculer_total_par_type(
            user, 'revenu', mois, annee
        )
        total_depenses = FinanceCalculator.calculer_total_par_type(
            user, 'depense', mois, annee
        )
        return total_revenus - total_depenses

    @staticmethod
    def calculer_pourcentage_categorie(montant_categorie, total_depenses):
        if total_depenses == 0:
            return Decimal('0')
        pourcentage = (Decimal(str(montant_categorie)) / Decimal(str(total_depenses))) * 100
        return round(pourcentage, 2)

    @staticmethod
    def calculer_depenses_par_categorie(user, mois, annee):
        depenses = Transaction.objects.filter(
            user=user,
            type='depense',
            date__month=mois,
            date__year=annee
        ).values(
            'categorie__id',
            'categorie__nom',
            'categorie__icone',
            'categorie__couleur'
        ).annotate(
            total=Sum('montant')
        ).order_by('-total')

        total_depenses = FinanceCalculator.calculer_total_par_type(
            user, 'depense', mois, annee
        )

        resultats = []
        for depense in depenses:
            pourcentage = FinanceCalculator.calculer_pourcentage_categorie(
                depense['total'], total_depenses
            )
            resultats.append({
                'categorie_id': depense['categorie__id'],
                'categorie_nom': depense['categorie__nom'],
                'categorie_icone': depense['categorie__icone'],
                'categorie_couleur': depense['categorie__couleur'],
                'total': depense['total'],
                'pourcentage': pourcentage,
            })

        return resultats