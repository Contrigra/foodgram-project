from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from api.models import Shoplist, Favourites

User = get_user_model()


def create_shoplist(sender, instance, created, **kwargs):
    if created:
        Shoplist.objects.create(user=instance)


def create_favourites(sender, instance, created, **kwargs):
    if created:
        Favourites.objects.create(user=instance)


post_save.connect(create_shoplist, sender=User)
post_save.connect(create_favourites, sender=User)
