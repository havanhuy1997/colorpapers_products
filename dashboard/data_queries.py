from django.conf import settings
from colorpapers_product.dashboard import data_connect as mongo
from colorpapers_product.dashboard.models import *
class KEEPA_QUERIES:

    def __init__(self):
        self.DATA_KEY = settings.KEEPA_KEY
        self.PER_PAGE_LIMIT = settings.PER_PAGE_RECORD_LIMIT
        self.TARGET_MARKET = settings.DOMAIN_MARKET
        self.URL_PREFIX = settings.KEEPA_API_PREFIX
        self.PRODUCTS_COUNT = 0
    
    def loadDataDict(self, catag_id, catag_type, page):
        default_dict = {
            "sort":[["current_SALES","asc"]],
            "productType":[0,1],
            "page":page,
            "perPage":self.PER_PAGE_LIMIT
        }
        if catag_type is True:
            default_dict.update({"rootCategory": catag_id})
        else:
            default_dict.update({"categories_include":[str(catag_id)]})
        return default_dict
    
    def executeNode(self, execution_id):
        object_row = processExecutions.objects.get(id=int(execution_id))
        




