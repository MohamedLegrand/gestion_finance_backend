from rest_framework import serializers
from finances.models.transfert_model import Transfert


class TransfertSerializer(serializers.ModelSerializer):

    compte_source_nom = serializers.SerializerMethodField()
    compte_destination_nom = serializers.SerializerMethodField()

    class Meta:
        model = Transfert
        fields = [
            'id',
            'compte_source',
            'compte_source_nom',
            'compte_destination',
            'compte_destination_nom',
            'montant',
            'description',
            'date',
            'date_creation',
            'date_modification',
        ]
        read_only_fields = [
            'id',
            'compte_source_nom',
            'compte_destination_nom',
            'date_creation',
            'date_modification',
        ]

    def get_compte_source_nom(self, obj):
        return obj.compte_source.nom if obj.compte_source else None

    def get_compte_destination_nom(self, obj):
        return obj.compte_destination.nom if obj.compte_destination else None

    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant doit être supérieur à zéro."
            )
        return value

    def validate_compte_source(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(
                "Ce compte ne vous appartient pas."
            )
        if not value.actif:
            raise serializers.ValidationError(
                "Le compte source est désactivé."
            )
        return value

    def validate_compte_destination(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(
                "Ce compte ne vous appartient pas."
            )
        if not value.actif:
            raise serializers.ValidationError(
                "Le compte destination est désactivé."
            )
        return value

    def validate(self, data):
        compte_source = data.get('compte_source')
        compte_destination = data.get('compte_destination')
        montant = data.get('montant')

        # Vérifier que les deux comptes sont différents
        if compte_source and compte_destination:
            if compte_source.id == compte_destination.id:
                raise serializers.ValidationError(
                    "Le compte source et le compte destination "
                    "ne peuvent pas être identiques."
                )

        # Vérifier solde suffisant
        if compte_source and montant:
            if compte_source.solde < montant:
                raise serializers.ValidationError(
                    f"Solde insuffisant. "
                    f"Solde disponible : {compte_source.solde} {compte_source.devise} / "
                    f"Montant demandé : {montant} {compte_source.devise}"
                )

        return data

    def create(self, validated_data):
        from finances.services.transfert_service import TransfertService
        user = self.context['request'].user

        return TransfertService.creer_transfert(
            user=user,
            compte_source=validated_data['compte_source'],
            compte_destination=validated_data['compte_destination'],
            montant=validated_data['montant'],
            description=validated_data.get('description', ''),
            date=validated_data['date'],
        )