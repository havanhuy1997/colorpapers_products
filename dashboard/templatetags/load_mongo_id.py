from django import template

register = template.Library()

@register.filter(name='private')
def private(value):
    return str(value['_id'])
