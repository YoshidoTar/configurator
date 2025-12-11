import sqlite3
import hashlib


class Database:
    def __init__(self, db_name="configurations.db"):
        self.db_name = db_name
        self.connect()
        self.init_db()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def init_db(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            configuration TEXT,
            is_approved INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        self.cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("admin", self.hash_password("admin123"), "admin"))

        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, self.hash_password(password))
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, self.hash_password(password))
        )
        return self.cursor.fetchone()

    def save_configuration(self, user_id, configuration):
        try:
            self.cursor.execute(
                "INSERT INTO saved_configurations (user_id, configuration) VALUES (?, ?)",
                (user_id, configuration)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Ошибка БД:", e)
            return False

    def view_saved_configurations(self, user_id):
        self.cursor.execute(
            "SELECT configuration FROM saved_configurations WHERE user_id=?",
            (user_id,)
        )
        return self.cursor.fetchall()

    def view_all_configurations_for_edit(self):
        self.cursor.execute("""
        SELECT saved_configurations.id, users.username, saved_configurations.configuration
        FROM saved_configurations
        JOIN users ON saved_configurations.user_id = users.id
        """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
