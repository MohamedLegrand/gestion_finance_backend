from django.db import models
from account.models.user_model import User


class Categorie(models.Model):

    TYPE_CHOICES = [
        ('depense', 'Dépense'),
        ('revenu', 'Revenu'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icone = models.CharField(max_length=10, blank=True, null=True)
    couleur = models.CharField(max_length=7, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'nom', 'type']
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.type})"