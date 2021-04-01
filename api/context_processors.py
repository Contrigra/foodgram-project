from django.core.paginator import Paginator

from api.models import TimeTag, Recipe
from foodgram.utils import get_filter_tags, get_tag_status, get_url_with_tags


def filtering(request):
    # TODO if no tags received, all tags should be switched on
    received_tags = get_filter_tags(request)
    url_tags_line = get_url_with_tags(request)

    if received_tags is None:
        recipes = Recipe.objects.all()
    else:
        recipes = Recipe.objects.filter(
            tag__id__in=received_tags).distinct()

    no_tags = get_tag_status(recipes)

    url_tags_line = get_url_with_tags(request)
    all_tags = TimeTag.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return {'request': request, 'page': page, 'recipes': recipes, 'paginator': paginator,
            'tags': all_tags,
            'received_tags': received_tags, 'url_tags_line': url_tags_line,
            'no_tags': no_tags}