from django.db import models
from account.models.user_model import User
from finances.models.categorie_model import Categorie


class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    montant_limite = models.DecimalField(max_digits=12, decimal_places=2)
    mois = models.PositiveIntegerField()
    annee = models.PositiveIntegerField()
    alerte_80 = models.BooleanField(default=False)
    alerte_100 = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'categorie', 'mois', 'annee']
        ordering = ['-annee', '-mois']

    def __str__(self):
        return f"Budget {self.categorie.nom} - {self.mois}/{self.annee} - {self.montant_limite}"