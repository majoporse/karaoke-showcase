import os

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "lyrics")
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "changeme")
es_client = None


def init_elasticsearch():
    global es_client
    es_client = Elasticsearch(
        [ELASTICSEARCH_URL], basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    )
    return es_client


def get_es_client():
    global es_client
    if es_client is None:
        es_client = init_elasticsearch()
    return es_client


def get_elasticsearch_index():
    return ELASTICSEARCH_INDEX
