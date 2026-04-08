from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models.user_model import User
from account.models.profile import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)