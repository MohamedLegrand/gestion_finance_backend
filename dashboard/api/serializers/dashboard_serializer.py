from rest_framework import serializers
from finances.api.serializers.compte_serializer import CompteSerializer
from finances.api.serializers.transaction_serializer import TransactionListSerializer
from finances.api.serializers.budget_serializer import BudgetSerializer


class BilanMensuelSerializer(serializers.Serializer):
    mois = serializers.IntegerField()
    annee = serializers.IntegerField()
    total_revenus = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_depenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    epargne = serializers.DecimalField(max_digits=12, decimal_places=2)


class DepenseCategorieSerializer(serializers.Serializer):
    categorie_id = serializers.IntegerField()
    categorie_nom = serializers.CharField()
    categorie_icone = serializers.CharField(allow_null=True)
    categorie_couleur = serializers.CharField(allow_null=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    pourcentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class AlerteBudgetSerializer(serializers.Serializer):
    type = serializers.CharField()
    message = serializers.CharField()


class EtatBudgetSerializer(serializers.Serializer):
    budget_id = serializers.IntegerField()
    categorie = serializers.CharField()
    mois = serializers.IntegerField()
    annee = serializers.IntegerField()
    montant_limite = serializers.DecimalField(max_digits=12, decimal_places=2)
    montant_depense = serializers.DecimalField(max_digits=12, decimal_places=2)
    montant_restant = serializers.DecimalField(max_digits=12, decimal_places=2)
    pourcentage_utilise = serializers.DecimalField(max_digits=5, decimal_places=2)
    alertes = AlerteBudgetSerializer(many=True)


class DashboardSerializer(serializers.Serializer):
    utilisateur = serializers.CharField()
    date_aujourdhui = serializers.DateField()
    mois_en_cours = serializers.IntegerField()
    annee_en_cours = serializers.IntegerField()
    solde_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    comptes = CompteSerializer(many=True)
    bilan_mensuel = BilanMensuelSerializer()
    dernieres_transactions = TransactionListSerializer(many=True)
    depenses_par_categorie = DepenseCategorieSerializer(many=True)
    etat_budgets = EtatBudgetSerializer(many=True)