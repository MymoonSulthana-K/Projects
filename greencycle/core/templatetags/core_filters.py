# greencycle/core/templatetags/core_filters.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def sub(value, arg):
    """
    Subtracts the arg from the value.
    Usage: {{ value|sub:arg }}
    Handles Decimal types correctly.
    """
    try:
        return Decimal(value) - Decimal(arg)
    except (ValueError, TypeError):
        return '' # Or raise an error, or return 0, depending on desired behavior