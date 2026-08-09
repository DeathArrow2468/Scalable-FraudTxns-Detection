import psycopg2
import boto3
from config import DB_PASSWORD as pwd
password = pwd

conn = None
try:
    conn = psycopg2.connect(
        host='database-2.cfauguumuok7.ap-south-1.rds.amazonaws.com',
        port=5432,
        database='postgres',
        user='postgres',
        password=password,
        sslmode='verify-full',
    sslrootcert=r'C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\secrets\global-bundle.pem'
    )
    cur = conn.cursor()
    cur.execute('SELECT version();')
    print(cur.fetchone()[0])
    cur.close()
except Exception as e:
    print(f"Database error: {e}")
    raise
finally:
    if conn:
        conn.close()