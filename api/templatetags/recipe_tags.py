from django import template

register = template.Library()


@register.filter()
def add_id(url, tag_id):
    url_line = str(tag_id)
    if url is None:
        return url_line
    return url + url_line


@register.filter()
def string_view(tag_id):
    return str(tag_id)
