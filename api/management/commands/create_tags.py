from django.core.management.base import BaseCommand

from api.models import TimeTag


class Command(BaseCommand):
    help = 'Create tags which are used for recipe creation'

    def handle(self, *args, **options):
        TimeTag.objects.get_or_create(name='breakfast', slug='breakfast',
                                      colour='orange', ru_local='Завтрак')
        TimeTag.objects.get_or_create(name='lunch', slug='lunch',
                                      colour='green', ru_local='Обед')
        TimeTag.objects.get_or_create(name='dinner', slug='dinner',
                                      colour='purple', ru_local='Ужин')


