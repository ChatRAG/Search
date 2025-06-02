import json
import common.embed as e
import common.client as c

client = c.get_client()


def handler(event, context):
    try:
        required_fields = ["file_key", "offset", "title", "content"]
        for field in required_fields:
            if field not in event:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing required field: {field}"})
                }

        file_key = event["file_key"]
        offset = event["offset"]
        title = event["title"]
        content = event["content"]
        chunk_id = f"{file_key}-{offset}"

        # Build base chunk
        chunk = {
            "chunk_id": chunk_id,
            "file_key": file_key,
            "title": title,
            "content": content,
            "offset": offset
        }

        # Insert into word_search_index
        client.index(index="word_search_index", id=chunk_id, body=chunk)

        # Embed and insert into embedding_index
        embedding = e.embed_text(content)
        chunk["embedding"] = embedding
        client.index(index="embedding_index", id=chunk_id, body=chunk)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Document added to both indexes", "chunk_id": chunk_id})
        }

    except Exception as ex:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(ex)})
        }
