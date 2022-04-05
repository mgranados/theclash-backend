from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

conn = sqlite3.connect(os.getenv('LOCAL_DB'))
cur = conn.cursor()
cur.execute(""" CREATE TABLE transactions (
        id VARCHAR,
        account_id VARCHAR,
        account_link VARCHAR,
        created_at INTEGER,
        currency VARCHAR, 
        description VARCHAR, 
        amount_in_cents INTEGER, 
        status VARCHAR, 
        category VARCHAR,
        merchant_name VARCHAR,
        merchant_website VARCHAR
    )""")
conn.commit()
conn.close()