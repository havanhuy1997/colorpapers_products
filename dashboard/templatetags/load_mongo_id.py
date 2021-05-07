from django import template

register = template.Library()

@register.filter(name='private')
def private(value):
    return str(value['_id'])

@register.filter(name='export_slug_key')
def export_slug_key(value):
    keys_list = list(value.GET.keys())
    if "node_key" in keys_list:
        return '1'
    elif "q" in keys_list:
        return '2'
    else:
        return '0'

@register.filter(name='export_slug_value')
def export_slug_value(value):
    keys_list = list(value.GET.keys())
    if "node_key" in keys_list:
        return value.GET['node_key']
    elif "q" in keys_list:
        return value.GET['q']
    else:
        return ''