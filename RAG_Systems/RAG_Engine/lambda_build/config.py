import os

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")

RETRIEVER_1_TABLE = "retriever_1_chunks"
RETRIEVER_2_TABLE = "retriever_2_chunks"
RETRIEVER_3_TABLE = "retriever_3_chunks"

TOP_K_RESEARCH = 3
TOP_K_GUIDELINES = 3