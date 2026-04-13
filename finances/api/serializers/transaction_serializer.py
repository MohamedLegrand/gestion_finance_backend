from rest_framework import serializers
from finances.models.transaction_model import Transaction
from finances.models.compte_model import Compte
from finances.models.categorie_model import Categorie


class TransactionSerializer(serializers.ModelSerializer):

    compte_nom = serializers.SerializerMethodField()
    categorie_nom = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'compte',
            'compte_nom',
            'categorie',
            'categorie_nom',
            'montant',
            'type',
            'description',
            'date',
            'date_creation',
            'date_modification',
        ]
        read_only_fields = [
            'id',
            'compte_nom',
            'categorie_nom',
            'date_creation',
            'date_modification',
        ]

    def get_compte_nom(self, obj):
        return obj.compte.nom if obj.compte else None

    def get_categorie_nom(self, obj):
        return obj.categorie.nom if obj.categorie else None

    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant doit être supérieur à zéro."
            )
        return value

    def validate_type(self, value):
        types_valides = ['depense', 'revenu']
        if value not in types_valides:
            raise serializers.ValidationError(
                f"Type invalide. Types acceptés : {', '.join(types_valides)}"
            )
        return value

    def validate_compte(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(
                "Ce compte ne vous appartient pas."
            )
        if not value.actif:
            raise serializers.ValidationError(
                "Ce compte est désactivé."
            )
        return value

    def validate_categorie(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(
                "Cette catégorie ne vous appartient pas."
            )
        return value

    def validate(self, data):
        type_transaction = data.get('type')
        categorie = data.get('categorie')

        # Vérifier que le type de transaction
        # correspond au type de catégorie
        if categorie and type_transaction:
            if categorie.type != type_transaction:
                raise serializers.ValidationError(
                    f"La catégorie '{categorie.nom}' est de type "
                    f"'{categorie.type}' mais la transaction est "
                    f"de type '{type_transaction}'."
                )

        # Vérifier solde suffisant pour une dépense
        if type_transaction == 'depense':
            compte = data.get('compte')
            montant = data.get('montant')
            if compte and montant:
                if compte.solde < montant:
                    raise serializers.ValidationError(
                        f"Solde insuffisant. "
                        f"Solde disponible : {compte.solde} {compte.devise} / "
                        f"Montant demandé : {montant} {compte.devise}"
                    )

        return data

    def create(self, validated_data):
        from finances.services.transaction_service import TransactionService
        user = self.context['request'].user

        return TransactionService.creer_transaction(
            user=user,
            compte=validated_data['compte'],
            categorie=validated_data.get('categorie'),
            montant=validated_data['montant'],
            type=validated_data['type'],
            description=validated_data.get('description', ''),
            date=validated_data['date'],
        )

    def update(self, instance, validated_data):
        from finances.services.transaction_service import TransactionService

        return TransactionService.modifier_transaction(
            user=self.context['request'].user,
            transaction_obj=instance,
            **validated_data
        )


class TransactionListSerializer(TransactionSerializer):

    class Meta(TransactionSerializer.Meta):
        fields = [
            'id',
            'compte_nom',
            'categorie_nom',
            'montant',
            'type',
            'description',
            'date',
        ]


class TransactionDetailSerializer(TransactionSerializer):

    class Meta(TransactionSerializer.Meta):
        fields = TransactionSerializer.Meta.fields