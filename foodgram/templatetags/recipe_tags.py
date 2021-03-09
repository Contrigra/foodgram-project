from django import template

register = template.Library()

@register.filter()
def add_id(url, tag):
    url_line = str(tag)
    if url is None:
        return url_line
    return url + '&tags=' + url_line
