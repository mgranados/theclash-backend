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
    "token": "1234ab"
}
r = requests.post(base_url + "/api/accounts/", data=payload, auth=(user_secret, user_pass))

accounts_json = r.json()
for acc in accounts_json:
    print(acc['id'])
    # INSERT
    utc_time = time.strptime(acc['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_created_at = timegm(utc_time)
    cur.execute("""
        INSERT INTO accounts (
            id, 
            link, 
            institution_name, 
            category, 
            number, 
            balance_current_cents, 
            name, 
            created_at, 
            public_identification_name, 
            public_identification_value
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            acc['id'], 
            acc['link'], 
            acc['institution']['name'],
            acc['category'],
            acc['number'],
            acc['balance']['current'] * 100,
            acc['name'],
            epoch_created_at,
            acc['public_identification_name'],
            acc['public_identification_value']
        )
    )

conn.commit()
conn.close()