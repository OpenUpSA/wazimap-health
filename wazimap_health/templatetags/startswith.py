from django import template

register = template.Library()


@register.filter(name='startswith')
def startswith(value, geo_level):
    """
    we need to check if a geography is a point or not.
    """
    return value.startswith(geo_level)
