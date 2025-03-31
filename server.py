import socket
import jsonpickle
import pyodbc
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

secret_key = get_random_bytes(16)

class User:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Test;Trusted_Connection=yes')
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

    def generate_and_store_secret_key(self):
        self.cursor.execute('UPDATE Users SET SecretKey = ? WHERE Login = ?', (secret_key, self.username))
        self.conn.commit()
        return secret_key

    def get_secret_key(self):
        self.cursor.execute('SELECT SecretKey FROM Users WHERE Login = ?', (self.username,))
        result = self.cursor.fetchone()
        return result[0] if result else None