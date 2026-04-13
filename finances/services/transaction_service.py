from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from finances.models.transaction_model import Transaction
from finances.services.compte_service import CompteService


class TransactionService:

    @staticmethod
    def get_transactions_user(user, filters=None):
        queryset = Transaction.objects.filter(user=user)

        if filters:
            if filters.get('compte_id'):
                queryset = queryset.filter(compte_id=filters['compte_id'])

            if filters.get('categorie_id'):
                queryset = queryset.filter(categorie_id=filters['categorie_id'])

            if filters.get('type'):
                queryset = queryset.filter(type=filters['type'])

            if filters.get('mois'):
                queryset = queryset.filter(date__month=filters['mois'])

            if filters.get('annee'):
                queryset = queryset.filter(date__year=filters['annee'])

        return queryset

    @staticmethod
    def get_transaction_by_id(user, transaction_id):
        try:
            return Transaction.objects.get(id=transaction_id, user=user)
        except Transaction.DoesNotExist:
            return None

    @staticmethod
    def creer_transaction(user, compte, categorie, montant, type, description, date):
        with transaction.atomic():
            montant = Decimal(str(montant))

            if type == 'depense':
                CompteService.debiter_compte(compte, montant)
            elif type == 'revenu':
                CompteService.crediter_compte(compte, montant)

            nouvelle_transaction = Transaction.objects.create(
                user=user,
                compte=compte,
                categorie=categorie,
                montant=montant,
                type=type,
                description=description,
                date=date
            )

        return nouvelle_transaction

    @staticmethod
    def modifier_transaction(user, transaction_obj, **kwargs):
        with transaction.atomic():

            # Annuler l'effet de l'ancienne transaction
            if transaction_obj.type == 'depense':
                CompteService.crediter_compte(transaction_obj.compte, transaction_obj.montant)
            elif transaction_obj.type == 'revenu':
                CompteService.debiter_compte(transaction_obj.compte, transaction_obj.montant)

            # Appliquer les nouvelles valeurs
            for key, value in kwargs.items():
                setattr(transaction_obj, key, value)

            # Appliquer le nouvel effet sur le compte
            nouveau_montant = Decimal(str(transaction_obj.montant))
            if transaction_obj.type == 'depense':
                CompteService.debiter_compte(transaction_obj.compte, nouveau_montant)
            elif transaction_obj.type == 'revenu':
                CompteService.crediter_compte(transaction_obj.compte, nouveau_montant)

            transaction_obj.save()

        return transaction_obj

    @staticmethod
    def supprimer_transaction(transaction_obj):
        with transaction.atomic():

            # Annuler l'effet de la transaction sur le compte
            if transaction_obj.type == 'depense':
                CompteService.crediter_compte(transaction_obj.compte, transaction_obj.montant)
            elif transaction_obj.type == 'revenu':
                CompteService.debiter_compte(transaction_obj.compte, transaction_obj.montant)

            transaction_obj.delete()

    @staticmethod
    def get_total_depenses(user, mois, annee):
        result = Transaction.objects.filter(
            user=user,
            type='depense',
            date__month=mois,
            date__year=annee
        ).aggregate(total=Sum('montant'))
        return result['total'] or Decimal('0')

    @staticmethod
    def get_total_revenus(user, mois, annee):
        result = Transaction.objects.filter(
            user=user,
            type='revenu',
            date__month=mois,
            date__year=annee
        ).aggregate(total=Sum('montant'))
        return result['total'] or Decimal('0')

    @staticmethod
    def get_depenses_par_categorie(user, mois, annee):
        return Transaction.objects.filter(
            user=user,
            type='depense',
            date__month=mois,
            date__year=annee
        ).values(
            'categorie__nom',
            'categorie__icone',
            'categorie__couleur'
        ).annotate(
            total=Sum('montant')
        ).order_by('-total')

    @staticmethod
    def get_bilan_mensuel(user, mois, annee):
        total_depenses = TransactionService.get_total_depenses(user, mois, annee)
        total_revenus = TransactionService.get_total_revenus(user, mois, annee)
        epargne = total_revenus - total_depenses

        return {
            'mois': mois,
            'annee': annee,
            'total_revenus': total_revenus,
            'total_depenses': total_depenses,
            'epargne': epargne,
        }