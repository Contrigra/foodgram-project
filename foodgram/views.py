from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from api.models import Recipe



def index_view(request):
    #TODO кверисет рецептов, с пагинацией, сортировка от нового к старому, как-то передавать теги и ингредиенты

    recipes = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page':page, 'paginator': paginator})