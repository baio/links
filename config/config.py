__author__ = 'baio'
import os

def _dev_config():
    return {
        "MONGO_URI" : "mongodb://adm:123@ds039447.mongolab.com:39447/links",
        "ES_URI" : "http://localhost:9200/"
    }

def _product_config():
    return {
        "MONGO_URI" : os.environ['MONGO_URI'],
        "ES_URI" : os.environ['ES_URI']
    }

config = _product_config() if os.getenv("ENV", None) == 'production' else _dev_config()
