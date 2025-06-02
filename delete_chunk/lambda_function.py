import json
import common.client as c

client = c.get_client()


def handler(event, context):
    try:
        file_key = event.get("file_key")

        if not file_key:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required field: file_key"})
            }

        # Delete matching docs from both indexes
        for index_name in ["word_search_index", "embedding_index"]:
            client.delete_by_query(
                index=index_name,
                body={
                    "query": {
                        "term": {
                            "file_key": file_key
                        }
                    }
                }
            )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"All chunks with file_key='{file_key}' deleted from both indexes."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }