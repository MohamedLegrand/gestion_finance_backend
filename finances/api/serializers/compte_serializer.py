from rest_framework import serializers
from finances.models.compte_model import Compte


class CompteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compte
        fields = [
            'id',
            'nom',
            'type',
            'solde',
            'devise',
            'actif',
            'date_creation',
            'date_modification',
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def validate_type(self, value):
        types_valides = ['mobile_money', 'bancaire', 'cash', 'autre']
        if value not in types_valides:
            raise serializers.ValidationError(
                f"Type invalide. Types acceptés : {', '.join(types_valides)}"
            )
        return value

    def validate_devise(self, value):
        devises_valides = ['XAF', 'USD', 'EUR']
        if value not in devises_valides:
            raise serializers.ValidationError(
                f"Devise invalide. Devises acceptées : {', '.join(devises_valides)}"
            )
        return value

    def validate_solde(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Le solde initial ne peut pas être négatif."
            )
        return value

    def validate_nom(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le nom doit contenir au moins 2 caractères."
            )
        return value.strip()

    def validate(self, data):
        user = self.context['request'].user
        nom = data.get('nom')

        # Vérifier unicité lors de la création
        if self.instance is None:
            if Compte.objects.filter(user=user, nom=nom).exists():
                raise serializers.ValidationError(
                    f"Un compte '{nom}' existe déjà."
                )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Compte.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        # Le solde ne peut pas être modifié directement
        # Il est modifié uniquement via les transactions
        validated_data.pop('solde', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CompteDetailSerializer(CompteSerializer):

    solde_total = serializers.SerializerMethodField()

    class Meta(CompteSerializer.Meta):
        fields = CompteSerializer.Meta.fields + ['solde_total']

    def get_solde_total(self, obj):
        return obj.solde