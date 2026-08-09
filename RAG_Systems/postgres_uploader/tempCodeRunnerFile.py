collection = load_json(next(Path(EMBEDDINGS_FOLDER).rglob("*.json")))

    # print(type(collection["chunks"][0]["embedding"]))

    # print(len(collection["chunks"][0]["embedding"]))

    # print(collection["chunks"][0]["embedding"][:5])