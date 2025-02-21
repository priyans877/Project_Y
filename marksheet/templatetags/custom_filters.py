from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the given value by the argument"""
    return value * arg

@register.filter
def index(sequence, position):
    """Returns the element at the given index in a list."""
    try:
        return sequence[int(position)]
    except (IndexError, ValueError, TypeError):
        return None
