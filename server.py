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

    def register_user(self):
        cipher = AES.new(secret_key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(self.password.encode('utf-8'))

        db_password = f"{ciphertext.hex()}:{nonce.hex()}:{tag.hex()}"

        self.cursor.execute('INSERT INTO Users (Login, Password, SecretKey) VALUES (?, ?, ?)', (self.username, db_password, secret_key))
        self.conn.commit()

    def check_login(self, input_password):
        self.cursor.execute('SELECT Password, SecretKey FROM Users WHERE Login = ?', (self.username,))
        result = self.cursor.fetchone()

        if not result:
            return False

        stored_data, secret_key = result
        stored_data = stored_data.split(':')
        if len(stored_data) != 3:
            return False

        try:
            ciphertext = bytes.fromhex(stored_data[0])
            nonce = bytes.fromhex(stored_data[1])
            tag = bytes.fromhex(stored_data[2])

            cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode('utf-8') == input_password
        except:
            return False

    def check_username_exists(self):
        self.cursor.execute('SELECT * FROM Users WHERE Login = ?', (self.username,))
        return self.cursor.fetchone() is not None

    def close_connection(self):
        self.conn.close()