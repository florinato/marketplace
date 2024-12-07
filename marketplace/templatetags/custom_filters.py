
from django import template

register = template.Library()

@register.filter
def render_stars(value):
    try:
        value = int(round(float(value)))
        return '⭐' * value
    except (ValueError, TypeError):
        return ''

