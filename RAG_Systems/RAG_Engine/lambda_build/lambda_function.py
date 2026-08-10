from rag_engine import RAGEngine

def lambda_handler(event, context):
    query = event["query"]
    engine = RAGEngine()

    try:
        research, guidelines = engine.retrieve(query)

        return {
            "statusCode": 200,
            "research": [
                {
                    "score": result.score,
                    "metadata": result.metadata,
                    "text": result.text
                }for result in research
            ],
            "guidelines":[
                {
                    "score": result.score,
                    "metadata": result.metadata,
                    "text": result.text
                }for result in guidelines
            ]
        }

    except Exception:
        print("Error in lambda_function")
        raise

    finally:
        engine.close()