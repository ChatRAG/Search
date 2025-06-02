from opensearchpy import OpenSearch


def get_client():
    host = 'search-chatrag-opensearch-wz6fxha74dkfc4ojr5kww7tf5e.ap-southeast-2.es.amazonaws.com'
    port = 443
    auth = ('admin', 'Chatrag-2025')

    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
    )

    return client
