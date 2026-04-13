from rest_framework import serializers
from finances.models.budget_model import Budget
from finances.services.budget_service import BudgetService


class BudgetSerializer(serializers.ModelSerializer):

    categorie_nom = serializers.SerializerMethodField()
    montant_depense = serializers.SerializerMethodField()
    montant_restant = serializers.SerializerMethodField()
    pourcentage_utilise = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            'id',
            'categorie',
            'categorie_nom',
            'montant_limite',
            'mois',
            'annee',
            'montant_depense',
            'montant_restant',
            'pourcentage_utilise',
            'alerte_80',
            'alerte_100',
            'date_creation',
            'date_modification',
        ]
        read_only_fields = [
            'id',
            'categorie_nom',
            'montant_depense',
            'montant_restant',
            'pourcentage_utilise',
            'alerte_80',
            'alerte_100',
            'date_creation',
            'date_modification',
        ]

    def get_categorie_nom(self, obj):
        return obj.categorie.nom if obj.categorie else None

    def get_montant_depense(self, obj):
        return BudgetService.get_montant_depense(obj)

    def get_montant_restant(self, obj):
        return BudgetService.get_montant_restant(obj)

    def get_pourcentage_utilise(self, obj):
        return BudgetService.get_pourcentage_utilise(obj)

    def validate_montant_limite(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant limite doit être supérieur à zéro."
            )
        return value

    def validate_mois(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError(
                "Le mois doit être compris entre 1 et 12."
            )
        return value

    def validate_categorie(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(
                "Cette catégorie ne vous appartient pas."
            )
        if value.type != 'depense':
            raise serializers.ValidationError(
                "Un budget ne peut être créé que pour "
                "une catégorie de type dépense."
            )
        return value

    def validate(self, data):
        user = self.context['request'].user
        categorie = data.get('categorie')
        mois = data.get('mois')
        annee = data.get('annee')

        if self.instance is None:
            if Budget.objects.filter(
                user=user,
                categorie=categorie,
                mois=mois,
                annee=annee
            ).exists():
                raise serializers.ValidationError(
                    f"Un budget existe déjà pour la catégorie "
                    f"'{categorie.nom}' en {mois}/{annee}."
                )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Budget.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('categorie', None)
        validated_data.pop('mois', None)
        validated_data.pop('annee', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance