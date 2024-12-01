import mysql.connector
from config import ConfigManager

class DBConnector:
    def __init__(self):
        self.config = ConfigManager.load_config()

    def connect(self):
        try:
            conn = mysql.connector.connect(**self.config['database'])
            return conn
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None

    def insert_data(self, query, data):
        conn = self.connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.executemany(query, data)
            conn.commit()
            conn.close()
