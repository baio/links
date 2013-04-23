__author__ = 'baio'
import os

def _dev_config():
    return {
        "MONGO_URI" : "mongodb://adm:123@ds039447.mongolab.com:39447/links",
        "ES_URI" : "http://ec8a279a8973c6f31c23e87e5c5a2f46-us-east-1.foundcluster.com:9200"
    }

def _product_config():
    return {
        "MONGO_URI" : os.environ['MONGO_URI'],
        "ES_URI" : os.environ['FOUNDELASTICSEARCH_URL']
    }

config = _product_config() if os.getenv("ENV", None) == 'production' else _dev_config()
