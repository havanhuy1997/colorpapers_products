from pymongo import MongoClient


client = MongoClient()
db = client.KEEPA_DATA
product_col = db.products_data