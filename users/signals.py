from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Shoplist, Favorites
from .models import User


@receiver(post_save, sender=User)
def create_shoplist(sender, instance, created, **kwargs):
    """A signal to create User's shoplist after User creation"""
    if created:
        Shoplist.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_favourites(sender, instance, created, **kwargs):
    """A signal to create User's favourite list after User creation"""
    if created:
        Favorites.objects.create(user=instance)
