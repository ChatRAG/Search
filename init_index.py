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

embedding_index_body = {
    "settings": {
        "index.knn": True
    },
    "mappings": {
        "properties": {
            "chunk_id": {"type": "keyword"},
            "file_key": {"type": "keyword"},
            "title": {"type": "text"},
            "content": {"type": "text"},
            "offset": {"type": "integer"},
            "embedding": {
                "type": "knn_vector",
                "dimension": 1024
            }
        }
    }
}

word_search_index_body = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "edge_ngram_tokenizer": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 25,
                    "token_chars": ["letter", "digit"]
                }
            },
            "analyzer": {
                "edge_ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "edge_ngram_tokenizer"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "chunk_id": {"type": "keyword"},
            "file_key": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "edge_ngram_analyzer"
            },
            "content": {"type": "text"},
            "offset": {"type": "integer"}
        }
    }
}

# Create embedding_index
if not client.indices.exists(index="embedding_index"):
    response = client.indices.create(index="embedding_index", body=embedding_index_body)
    print("Created embedding_index:", json.dumps(response, indent=2))
else:
    print("embedding_index already exists.")

# Create word_search_index
if not client.indices.exists(index="word_search_index"):
    response = client.indices.create(index="word_search_index", body=word_search_index_body)
    print("Created word_search_index:", json.dumps(response, indent=2))
else:
    print("word_search_index already exists.")
