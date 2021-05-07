from pymongo import MongoClient


class DATABASE:

    def __init__(self):
        client = MongoClient()
        db = client.KEEPA_DATA
        self.product_col = db.products_data
        # self.product_col.create_index([('title','text')])