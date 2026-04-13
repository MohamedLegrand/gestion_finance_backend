from decimal import Decimal
from django.db import transaction
from finances.models.compte_model import Compte


class CompteService:

    @staticmethod
    def get_comptes_user(user):
        return Compte.objects.filter(user=user, actif=True)

    @staticmethod
    def get_compte_by_id(user, compte_id):
        try:
            return Compte.objects.get(id=compte_id, user=user, actif=True)
        except Compte.DoesNotExist:
            return None

    @staticmethod
    def creer_compte(user, nom, type, solde_initial, devise='XAF'):
        compte = Compte.objects.create(
            user=user,
            nom=nom,
            type=type,
            solde=Decimal(str(solde_initial)),
            devise=devise
        )
        return compte

    @staticmethod
    def modifier_compte(compte, **kwargs):
        for key, value in kwargs.items():
            setattr(compte, key, value)
        compte.save()
        return compte

    @staticmethod
    def desactiver_compte(compte):
        compte.actif = False
        compte.save()
        return compte

    @staticmethod
    def crediter_compte(compte, montant):
        with transaction.atomic():
            compte.refresh_from_db()
            compte.solde += Decimal(str(montant))
            compte.save()
        return compte

    @staticmethod
    def debiter_compte(compte, montant):
        with transaction.atomic():
            compte.refresh_from_db()
            if compte.solde < Decimal(str(montant)):
                raise ValueError(
                    f"Solde insuffisant. Solde actuel : {compte.solde} {compte.devise}"
                )
            compte.solde -= Decimal(str(montant))
            compte.save()
        return compte

    @staticmethod
    def get_solde_total(user):
        comptes = Compte.objects.filter(user=user, actif=True)
        total = Decimal('0')
        for compte in comptes:
            total += compte.solde
        return total