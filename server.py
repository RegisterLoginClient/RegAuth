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