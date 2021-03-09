from django import template

register = template.Library()

@register.filter()
def add_id(url, type_id):
    url_line = str(type_id)
    if url is None:
        return url_line
    return url + url_line


@register.filter()
def string_view(type_id):
    return str(type_id)
