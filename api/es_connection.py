import requests
from elasticsearch import Elasticsearch

from config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT


class Searcher:

    def __init__(self):
        self.conn = Elasticsearch(
            f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"
        )

    def add_data(self):
        response = requests.get("https://jsonplaceholder.typicode.com/comments")
        data = response.json()

        self.conn.indices.create(index="comments", ignore=400)
        for _ in range(2000):
            for entry in data:
                document = {
                    "_index": "comments",
                    "_source": entry
                }
                yield document

    def search_by_field(self, field_name: str, value: str):
        query = {
            "query": {
                "match": {
                    field_name: value
                }
            }
        }

        try:
            return self.conn.search(index="comments", body=query)
        except IndexError:
            pass


def get_searcher():
    return Searcher()


if __name__ == "__main__":
    from elasticsearch.helpers import bulk

    searcher = Searcher()
    success, failed = bulk(searcher.conn, searcher.add_data())
