import cohere
import os

API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(API_KEY)


def rerank(query, docs, model="rerank-v3.5", top_n=3, score_threshold=0.1):
    response = co.rerank(
        model=model,
        query=query,
        documents=[doc['content'] for doc in docs],
        top_n=top_n,
    )

    # Filter documents with relevance score > 0.1 and extract document text
    filtered_results = [
        docs[item.index] for item in response.results if item.relevance_score > score_threshold
    ]

    # Return the top n documents as a list of strings
    return filtered_results[:top_n]

