import os
from opensearchpy import OpenSearch

OPEN_SEARCH_PASSWORD = os.getenv("OPEN_SEARCH_PASSWORD")


def get_client():
    host = 'search-chatrag-opensearch-wz6fxha74dkfc4ojr5kww7tf5e.ap-southeast-2.es.amazonaws.com'
    port = 443
    auth = ('admin', OPEN_SEARCH_PASSWORD)

    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
    )

    return client
