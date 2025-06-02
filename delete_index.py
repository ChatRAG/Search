from opensearchpy import OpenSearch
import json

host = 'search-chatrag-opensearch-wz6fxha74dkfc4ojr5kww7tf5e.ap-southeast-2.es.amazonaws.com'
port = 443
password = input('password: ')
auth = ('admin', password)

client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
)

indexes_to_delete = ["embedding_index", "word_search_index"]

for index in indexes_to_delete:
    if client.indices.exists(index=index):
        response = client.indices.delete(index=index)
        print(f"Deleted {index}: {json.dumps(response, indent=2)}")
    else:
        print(f"{index} does not exist.")
