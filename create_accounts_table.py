from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

conn = sqlite3.connect(os.getenv('LOCAL_DB'))
cur = conn.cursor()
cur.execute('CREATE TABLE accounts (id VARCHAR, link VARCHAR, institution_name VARCHAR, category VARCHAR, number VARCHAR, balance_current_cents INTEGER, name VARCHAR, created_at INTEGER, public_identification_name VARCHAR, public_identification_value VARCHAR)')
conn.commit()
conn.close()