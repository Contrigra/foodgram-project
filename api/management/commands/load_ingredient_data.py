import csv

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    help = 'load ingredient fixtures'

    def handle(self, *args, **options):
        with open('api/management/commands/ingredients.csv',
                  encoding='utf-8') as fixture:
            reader = csv.reader(fixture)
            for row in reader:
                name, units = row
                Ingredient.objects.get_or_create(name=name,
                                                 units=units)
