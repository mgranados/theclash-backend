# export FLASK_APP=server
# flask run                                     
from flask import Flask
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = sqlite3.connect(os.getenv('LOCAL_DB'))
cur = conn.cursor()

@app.route("/hello")
def index():
    return "<p>Ayoo page!</p>"

@app.route("/accounts")
def get_accounts():
    accounts = get_all_accounts()
    return {
        "accounts": accounts,
        "count": len(accounts),
        "limit": 1,
        "page": 1
    }

@app.route("/transactions")
def get_transactions():
    transactions = get_all_transactions()
    return {
        "transactions": transactions,
        "count": len(transactions),
        "limit": 1,
        "page": 1
    }

def get_all_accounts():
    conn = sqlite3.connect(os.getenv('LOCAL_DB'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM accounts')
    json_data = []
    for row in cur.fetchall():
        json_dict = {
            'id': row[0], 
            'link': row[1], 
            'institution_name': row[2],
            'category': row[3],
            'number': row[4],
            'balance_current_cents': row[5],
            'name': row[6],
            'created_at': row[7],
            'public_identification_name': row[8],
            'public_identification_value': row[9]
        }
        json_data.append(json_dict)
    conn.close()
    return json_data

def get_all_transactions():
    conn = sqlite3.connect(os.getenv('LOCAL_DB'))
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions')
    json_data = []
    for row in cur.fetchall():
        json_dict = {
            'id': row[0], 
            'account_id': row[1], 
            'account_link': row[2],
            'created_at': row[3],
            'currency': row[4],
            'description': row[5],
            'amount_in_cents': row[6],
            'status': row[7],
            'category': row[8],
            'merchant_name': row[9],
            'merchant_website': row[10]
        }
        json_data.append(json_dict)
    conn.close()
    return json_data
