from django.db import models
from account.models.user_model import User
from finances.models.compte_model import Compte
from finances.models.categorie_model import Categorie


class Transaction(models.Model):

    TYPE_CHOICES = [
        ('depense', 'Dépense'),
        ('revenu', 'Revenu'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    compte = models.ForeignKey(
        Compte,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-date_creation']

    def __str__(self):
        return f"{self.type} - {self.montant} - {self.date}"