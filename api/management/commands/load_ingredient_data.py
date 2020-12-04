from django.core.management.base import BaseCommand, CommandError
from api.models import Ingredient
import csv

class Command(BaseCommand):
    help = 'load ingredient fixtures'

    def handle(self, *args, **options):
        with open('api/management/commands/ingredients.csv') as fixture:
            reader = csv.reader(fixture)
            for row in reader:
                title, measure = row
                Ingredient.objects.get_or_create(title=title, measure=measure)