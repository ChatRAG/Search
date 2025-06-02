import json
import common.embed as e
import common.client as c

client = c.get_client()
top_k = 5


def handler(event, context):
    try:
        query_text = event.get("query")

        if not query_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required field: query"})
            }

        # Perform text-based fuzzy search
        text_result = client.search(
            index="word_search_index",
            body={
                "size": top_k,
                "query": {
                    "multi_match": {
                        "query": query_text,
                        "fields": ["title", "content"],
                        "fuzziness": "AUTO"
                    }
                }
            }
        )

        text_hits = text_result["hits"]["hits"]
        text_docs = [hit["_source"] for hit in text_hits]

        # Track seen chunk_ids to prevent duplicates
        seen_ids = set(doc.get("chunk_id") for doc in text_docs if "chunk_id" in doc)

        # Perform vector-based knn search
        embedding = e.embed_text(query_text)
        vector_result = client.search(
            index="embedding_index",
            body={
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": embedding,
                            "k": top_k
                        }
                    }
                }
            }
        )

        vector_hits = vector_result["hits"]["hits"]
        vector_docs = []
        for hit in vector_hits:
            doc = hit["_source"]
            cid = doc.get("chunk_id")
            if cid not in seen_ids:
                vector_docs.append(doc)
                seen_ids.add(cid)

        combined_docs = text_docs + vector_docs

        return {
            "statusCode": 200,
            "body": json.dumps({
                "results": combined_docs
            })
        }

    except Exception as ex:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(ex)})
        }
