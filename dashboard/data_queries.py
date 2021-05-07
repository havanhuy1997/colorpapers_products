from django.conf import settings
from dashboard.data_connect import DATABASE as mongo
from .models import *
import urllib.parse
from datetime import datetime
import json, requests, time
from pprint import pprint

class KEEPA_QUERIES:

    def __init__(self):
        self.DATA_KEY = settings.KEEPA_KEY
        self.PER_PAGE_LIMIT = settings.PER_PAGE_RECORD_LIMIT
        self.TARGET_MARKET = settings.DOMAIN_MARKET
        self.URL_PREFIX = settings.KEEPA_API_PREFIX
        self.PRODUCTS_COUNT = 0
        self.EXECUTION_OBJ = None
        self.PAGE_NO_ACTIVE = 0
        self.PRODUCT_SIZE_LIMIT = None
        self.TOKEN_LEFT = None
        self.MONGOOBJ = mongo()
    
    def loadDataDict(self, catag_id, catag_type, page):
        default_dict = {
            "sort":[["current_SALES","asc"]],
            "productType":[0,1],
            "page":page,
            "perPage":self.PER_PAGE_LIMIT
        }
        if catag_type is True:
            default_dict.update({"rootCategory": int(catag_id)})
        else:
            default_dict.update({"categories_include":[str(catag_id)]})
        return default_dict
    
    def executeNode(self, execution_object):
        self.EXECUTION_OBJ = execution_object
        node_id = execution_object.node_id
        node_type = execution_object.node_type
        if node_type =='root':
            catag_type = True
        else:
            catag_type = False
        initialRowDict = self.loadDataDict(node_id, catag_type, self.PAGE_NO_ACTIVE)
        self.fetchData(initialRowDict)

    def fetchData(self, search_dict):
        encoded_data = urllib.parse.quote_plus(str(json.dumps(search_dict)))
        url = self.URL_PREFIX.format(self.DATA_KEY, self.TARGET_MARKET, encoded_data)
        con = requests.get(url)
        data = json.loads(con.content)
        asin_list = data['asinList']
        self.TOKEN_LEFT = data['tokensLeft']
        self.PRODUCT_SIZE_LIMIT = data['totalResults']
        self.iterateAsinProducts(asin_list)
        
    

    def iterateAsinProducts(self, asinList):
        for asin in asinList:
            if int(self.MONGOOBJ.product_col.find({'asin': asin}).count()) > 0:
                continue
            url = settings.KEEPA_API+"/product?key={}&domain={}&asin={}".format(self.DATA_KEY, self.TARGET_MARKET, asin)
            con = requests.get(url)
            response = json.loads(con.content)
            product = response['products']
            if len(product) > 0:
                product_json_object = product[0]
                product_json_object.update({
                    "execution_id": int(self.EXECUTION_OBJ.id),
                    "execution_node_id": self.EXECUTION_OBJ.node_id,
                    "date_created": datetime.now()
                })
                self.MONGOOBJ.product_col.insert_one(product_json_object)
                self.EXECUTION_OBJ.updated_at = datetime.now()
                self.EXECUTION_OBJ.save()

            time.sleep(1)

        


