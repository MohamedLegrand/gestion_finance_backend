from django.db import models
from account.models.user_model import User
from finances.models.compte_model import Compte


class Transfert(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transferts'
    )
    compte_source = models.ForeignKey(
        Compte,
        on_delete=models.CASCADE,
        related_name='transferts_source'
    )
    compte_destination = models.ForeignKey(
        Compte,
        on_delete=models.CASCADE,
        related_name='transferts_destination'
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-date_creation']

    def __str__(self):
        return f"Transfert {self.montant} de {self.compte_source} vers {self.compte_destination}"