from django.db import models
from account.models.user_model import User


class Compte(models.Model):

    TYPE_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('bancaire', 'Bancaire'),
        ('cash', 'Cash'),
        ('autre', 'Autre'),
    ]

    DEVISE_CHOICES = [
        ('XAF', 'Franc CFA'),
        ('USD', 'Dollar américain'),
        ('EUR', 'Euro'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comptes'
    )
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    solde = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='XAF')
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'nom']
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom} - {self.solde} {self.devise}"