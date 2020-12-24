from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def create_recipe_view(request):
    return render(request, 'formRecipe.html')