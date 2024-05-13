
import json
from src.logger_util import logging
import sqlite3
from src.gmail_api import get_gmail_service,list_messages,get_message
from src.models import Email

def setup_database(DB_FILE="emails.db"):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                            id TEXT PRIMARY KEY,
                            sender TEXT,
                            subject TEXT,
                            labels TEXT,
                            date_received TEXT)''')
        conn.commit()
        conn.close()
    except Exception:
        logging.exception("exception occured",exc_info=True)
def save_email_to_db(email_data,DB_FILE):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("INSERT OR REPLACE INTO emails (id, sender, subject, labels, date_received) VALUES (?, ?, ?, ?, ?)",
                    (email_data['id'], email_data['sender'], email_data['subject'], email_data['labels'], email_data['date_received']))
        conn.commit()
        conn.close()
        logging.info("emails saved to DB")
    except Exception:
        logging.exception("exception occured",exc_info=True)

def extract_email_data(message):
    try:
        payload = message['payload']
        headers = payload.get('headers', [])

        sender = None
        subject = None
        received_date = None
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            elif header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'Date':
                received_date = header['value']

        return {
            'sender': sender,
            'subject': subject,
            'receivedDate': received_date,
        }
    except Exception:
        logging.exception("exception occured",exc_info=True)
        
def get_emails(DB_FILE='emails.db'):
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, sender, subject, labels, date_received FROM emails")
        emails = cursor.fetchall()
        conn.close()
        emails=[Email(**dict(email)) for email in emails]
    except Exception:
        logging.exception("exception occured",exc_info=True)
    return emails
def fetch_and_store_emails(service,DB_FILE='emails.db'):
    try:
        messages=list_messages(service)
        messages=[ get_message(service,msg) for msg in messages ]
        for msg in messages:
            email_msg=extract_email_data(msg)
            email_data = {
                'id': msg['id'],
                'sender': email_msg['sender'],
                'subject': email_msg['subject'],
                'labels': json.dumps(msg['labelIds']),
                'date_received': email_msg['receivedDate']
            }
            save_email_to_db(email_data,'emails.db')
    except Exception:
        logging.exception("exception occured",exc_info=True)