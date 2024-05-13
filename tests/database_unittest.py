import unittest
import sqlite3
from unittest.mock import MagicMock
from src.database import setup_database, save_email_to_db

class TestYourModule(unittest.TestCase):

    def setUp(self):
        self.DB_FILE = "test_emails.db"
        setup_database(self.DB_FILE)

    def tearDown(self):
        try:
            conn = sqlite3.connect(self.DB_FILE)
            conn.execute("DROP TABLE IF EXISTS emails")
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error while tearing down:", e)

    def test_setup_database(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails'")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

    def test_save_email_to_db(self):
        email_data = {
            'id': '123456',
            'sender': 'test@example.com',
            'subject': 'Test Subject',
            'labels': '["label1", "label2"]',
            'date_received': '2024-05-13'
        }
        save_email_to_db(email_data, self.DB_FILE)
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emails WHERE id=?", (email_data['id'],))
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], email_data['id'])


if __name__ == '__main__':
    unittest.main()
