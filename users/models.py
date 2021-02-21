from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from django.conf import settings
from api.models import Shoplist, Favourites

User = get_user_model()


def create_shoplist(sender, instance, created, **kwargs):
    """A signal to create User's shoplist after User creation"""
    if created:
        Shoplist.objects.create(user=instance)


def create_favourites(sender, instance, created, **kwargs):
    """A signal to create User's shoplist after User creation"""
    if created:
        Favourites.objects.create(user=instance)


post_save.connect(create_shoplist, sender=settings.AUTH_USER_MODEL)
post_save.connect(create_favourites, sender=settings.AUTH_USER_MODEL)
