from django.core.paginator import Paginator

from api.models import TimeTag
from foodgram.settings import OBJECT_PER_PAGE
from foodgram.utils import get_filter_tags, get_url_with_tags, obtain_recipes


def filtering(request):
    """
    A recipe filtering system for index, favorite and profile url
    """
    if request.resolver_match.url_name == 'index' \
            or request.resolver_match.url_name == 'favorites' \
            or request.resolver_match.url_name == 'profile':

        received_tags = get_filter_tags(request)
        url_tags_line = get_url_with_tags(request)

        if received_tags is None:
            received_tags = ['1', '2', '3']

        recipes = obtain_recipes(request, received_tags)

        url_tags_line = get_url_with_tags(request)
        if url_tags_line is None:
            url_tags_line = '123'

        all_tags = TimeTag.objects.all()

        paginator = Paginator(recipes, OBJECT_PER_PAGE)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        return {'request': request, 'page': page, 'recipes': recipes,
                'paginator': paginator,
                'tags': all_tags, 'page_number': page_number,
                'received_tags': received_tags, 'url_tags_line': url_tags_line}

    else:
        return {}
