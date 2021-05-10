from django import template
from dashboard.data_connect import DATABASE as mongo

register = template.Library()


MONGOOBJ = mongo()

@register.filter(name='getDataCount')
def getDataCount(value):
    return MONGOOBJ.product_col.find({'execution_node_id': str(value)}).count()

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