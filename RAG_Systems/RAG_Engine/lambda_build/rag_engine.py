from config import *
from search import SearchEngine
from utils.titan_embedder import TitanEmbedder

class RAGEngine:
    def __init__(self):
        self.embedder = TitanEmbedder()
        self.search_engine = SearchEngine()

    def retrieve(self, query):
        embedding = self.embedder.embed(query)

        research = self.search_engine.vector_search(
            RETRIEVER_1_TABLE, embedding, TOP_K_RESEARCH
        )

        guideline = self.search_engine.vector_search(
            RETRIEVER_3_TABLE, embedding, TOP_K_GUIDELINES
        )

        return research, guideline

    def close(self):
        self.search_engine.close()


if __name__ == "__main__":
    engine = RAGEngine()
    research, guidelines = engine.retrieve(
        "Account takeover fraud using mule accounts"
    )

    print("\n========== Research ==========\n")

    for result in research:

        print(f"Score : {result.score:.4f}")

        print(result.metadata)

        print(result.text[:200])

        print("-" * 80)

    print("\n========== Guidelines ==========\n")

    for result in guidelines:

        print(f"Score : {result.score:.4f}")

        print(result.metadata)

        print(result.text[:200])

        print("-" * 80)

    engine.close()
