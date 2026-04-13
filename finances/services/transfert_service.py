from decimal import Decimal
from django.db import transaction
from finances.models.transfert_model import Transfert
from finances.services.compte_service import CompteService


class TransfertService:

    @staticmethod
    def get_transferts_user(user, filters=None):
        queryset = Transfert.objects.filter(user=user)

        if filters:
            if filters.get('compte_source_id'):
                queryset = queryset.filter(
                    compte_source_id=filters['compte_source_id']
                )

            if filters.get('compte_destination_id'):
                queryset = queryset.filter(
                    compte_destination_id=filters['compte_destination_id']
                )

            if filters.get('mois'):
                queryset = queryset.filter(date__month=filters['mois'])

            if filters.get('annee'):
                queryset = queryset.filter(date__year=filters['annee'])

        return queryset

    @staticmethod
    def get_transfert_by_id(user, transfert_id):
        try:
            return Transfert.objects.get(id=transfert_id, user=user)
        except Transfert.DoesNotExist:
            return None

    @staticmethod
    def creer_transfert(user, compte_source, compte_destination, montant, description, date):
        with transaction.atomic():

            # Verification 1 : compte source != compte destination
            if compte_source.id == compte_destination.id:
                raise ValueError(
                    "Le compte source et le compte destination ne peuvent pas être identiques."
                )

            # Verification 2 : les deux comptes appartiennent au même user
            if compte_source.user != user or compte_destination.user != user:
                raise ValueError(
                    "Les comptes ne vous appartiennent pas."
                )

            # Verification 3 : compte source est actif
            if not compte_source.actif:
                raise ValueError(
                    "Le compte source est désactivé."
                )

            # Verification 4 : compte destination est actif
            if not compte_destination.actif:
                raise ValueError(
                    "Le compte destination est désactivé."
                )

            montant = Decimal(str(montant))

            # Debiter le compte source (vérifie solde suffisant)
            CompteService.debiter_compte(compte_source, montant)

            # Crediter le compte destination
            CompteService.crediter_compte(compte_destination, montant)

            # Enregistrer le transfert
            nouveau_transfert = Transfert.objects.create(
                user=user,
                compte_source=compte_source,
                compte_destination=compte_destination,
                montant=montant,
                description=description,
                date=date
            )

        return nouveau_transfert

    @staticmethod
    def annuler_transfert(transfert_obj):
        with transaction.atomic():

            # Reverser l'argent au compte source
            CompteService.crediter_compte(
                transfert_obj.compte_source,
                transfert_obj.montant
            )

            # Retirer l'argent du compte destination
            CompteService.debiter_compte(
                transfert_obj.compte_destination,
                transfert_obj.montant
            )

            transfert_obj.delete()