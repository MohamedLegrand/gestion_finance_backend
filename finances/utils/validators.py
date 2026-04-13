from decimal import Decimal
from datetime import date


class FinanceValidator:

    @staticmethod
    def valider_montant(montant):
        try:
            montant = Decimal(str(montant))
        except Exception:
            raise ValueError("Le montant doit être un nombre valide.")

        if montant <= 0:
            raise ValueError("Le montant doit être supérieur à zéro.")

        return montant

    @staticmethod
    def valider_mois(mois):
        try:
            mois = int(mois)
        except Exception:
            raise ValueError("Le mois doit être un nombre entier.")

        if mois < 1 or mois > 12:
            raise ValueError("Le mois doit être compris entre 1 et 12.")

        return mois

    @staticmethod
    def valider_annee(annee):
        try:
            annee = int(annee)
        except Exception:
            raise ValueError("L'année doit être un nombre entier.")

        annee_courante = date.today().year

        if annee < 2000 or annee > annee_courante + 1:
            raise ValueError(
                f"L'année doit être comprise entre 2000 et {annee_courante + 1}."
            )

        return annee

    @staticmethod
    def valider_date(date_value):
        if not isinstance(date_value, date):
            raise ValueError("La date fournie n'est pas valide.")

        return date_value

    @staticmethod
    def valider_solde_suffisant(solde, montant):
        solde = Decimal(str(solde))
        montant = Decimal(str(montant))

        if solde < montant:
            raise ValueError(
                f"Solde insuffisant. "
                f"Solde disponible : {solde} / "
                f"Montant demandé : {montant}"
            )

        return True

    @staticmethod
    def valider_type_transaction(type_transaction):
        types_valides = ['depense', 'revenu']

        if type_transaction not in types_valides:
            raise ValueError(
                f"Type de transaction invalide. "
                f"Types acceptés : {', '.join(types_valides)}"
            )

        return type_transaction

    @staticmethod
    def valider_type_compte(type_compte):
        types_valides = ['mobile_money', 'bancaire', 'cash', 'autre']

        if type_compte not in types_valides:
            raise ValueError(
                f"Type de compte invalide. "
                f"Types acceptés : {', '.join(types_valides)}"
            )

        return type_compte

    @staticmethod
    def valider_type_categorie(type_categorie):
        types_valides = ['depense', 'revenu']

        if type_categorie not in types_valides:
            raise ValueError(
                f"Type de catégorie invalide. "
                f"Types acceptés : {', '.join(types_valides)}"
            )

        return type_categorie