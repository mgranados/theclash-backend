import os
import requests
from dotenv import load_dotenv
import sqlite3
import time
from calendar import timegm

load_dotenv()

base_url = "https://sandbox.belvo.com"
user_secret = os.getenv('PROVIDER_ID')
user_pass = os.getenv('PROVIDER_PASS')

conn = sqlite3.connect(os.getenv('LOCAL_DB'))
cur = conn.cursor()

payload = {
    "link": "956e42d8-0680-4fe4-a2ed-6703a624d0ec",
    "date_from": "2022-02-01",
    "date_to": "2022-04-04"
}

r = requests.post(base_url + "/api/transactions/", data=payload, auth=(user_secret, user_pass))

transactions_json = r.json()
for transaction in transactions_json:
    print(transaction['id'])
    utc_time = time.strptime(transaction['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_created_at = timegm(utc_time)
    cur.execute("""
        INSERT INTO transactions (
            id,
            account_id,
            account_link,
            created_at,
            currency, 
            description, 
            amount_in_cents, 
            status, 
            category,
            merchant_name,
            merchant_website
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            transaction['id'], 
            transaction['account']['id'], 
            transaction['account']['link'],
            epoch_created_at,
            transaction['currency'], 
            transaction['description'], 
            int(transaction['amount'] * 100), 
            transaction['status'], 
            transaction['category'], 
            transaction['merchant']['name'], 
            transaction['merchant']['website']
 
        )
    )

conn.commit()
conn.close()