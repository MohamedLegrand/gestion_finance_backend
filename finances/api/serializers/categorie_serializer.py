from rest_framework import serializers
from finances.models.categorie_model import Categorie


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = [
            'id',
            'nom',
            'type',
            'icone',
            'couleur',
            'date_creation',
        ]
        read_only_fields = ['id', 'date_creation']

    def validate_type(self, value):
        types_valides = ['depense', 'revenu']
        if value not in types_valides:
            raise serializers.ValidationError(
                f"Type invalide. Types acceptés : {', '.join(types_valides)}"
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
        type = data.get('type')

        # Vérifier unicité lors de la création
        if self.instance is None:
            if Categorie.objects.filter(user=user, nom=nom, type=type).exists():
                raise serializers.ValidationError(
                    f"Une catégorie '{nom}' de type '{type}' existe déjà."
                )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Categorie.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance