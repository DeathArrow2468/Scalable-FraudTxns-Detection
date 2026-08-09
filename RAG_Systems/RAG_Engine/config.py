import os

DB_HOST = DB_HOST = 'database-2.cfauguumuok7.ap-south-1.rds.amazonaws.com'
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "fraud_txns_rag"

AWS_REGION = "ap-south-1"

RETRIEVER_1_TABLE = "retriever_1_chunks"
RETRIEVER_2_TABLE = "retriever_2_chunks"
RETRIEVER_3_TABLE = "retriever_3_chunks"

TOP_K_RESEARCH = 3
TOP_K_GUIDELINES = 3