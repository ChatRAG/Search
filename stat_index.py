from opensearchpy import OpenSearch
import json

host = 'search-chatrag-opensearch-wz6fxha74dkfc4ojr5kww7tf5e.ap-southeast-2.es.amazonaws.com'
port = 443
auth = ('admin', 'Chatrag-2025')

client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
)


def get_index_stats(index_name):
    print(f"\n📊 Stats for index: {index_name}")
    try:
        stats = client.indices.stats(index=index_name)
        count = client.count(index=index_name)["count"]
        print(f"Total docs: {count}")
        print(json.dumps(stats["_all"]["primaries"]["docs"], indent=2))
    except Exception as e:
        print(f"Failed to get stats: {e}")


def sample_documents(index_name, size=5):
    print(f"\n📦 Sample documents from index: {index_name}")
    try:
        result = client.search(
            index=index_name,
            body={
                "query": {"match_all": {}},
                "size": size
            }
        )
        hits = result["hits"]["hits"]
        for i, doc in enumerate(hits):
            print(f"\n--- Document {i + 1} ---")
            print(json.dumps(doc["_source"], indent=2))
    except Exception as e:
        print(f"Failed to retrieve documents: {e}")


for index in ["embedding_index", "word_search_index"]:
    get_index_stats(index)
    sample_documents(index)
