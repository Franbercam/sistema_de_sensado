import sqlite3

from werkzeug.security import generate_password_hash

DATABASE ='C:\\Users\\franb\\Desktop\\Universidad\\TFG\\workspace\\dashboard\\local_db.db'

def get_connection():
    return sqlite3.connect(DATABASE)

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        contraseña TEXT NOT NULL
    )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY, 
            nombre TEXT, 
            maquina TEXT, 
            email TEXT, 
            temperatura REAL, 
            humedad REAL
        ) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts_issued (
            id INTEGER PRIMARY KEY, 
            nombre TEXT, 
            maquina TEXT, 
            email TEXT, 
            temperatura REAL, 
            humedad REAL
        ) ''')
    conn.commit()
    conn.close()

def get_alerts_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts')
    data = cursor.fetchall()
    conn.close()
    return data

def get_alerts_issued_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts_issued')
    data = cursor.fetchall()
    conn.close()
    return data

def add_alert_db(nombre, maquina, email, temperatura, humedad):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO alerts (nombre, maquina, email, temperatura, humedad) VALUES (?, ?, ?, ?, ?)', (nombre, maquina, email, temperatura, humedad))
    conn.commit()
    conn.close()


def get_users_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()
    return data

def get_users_name_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM users')
    data = cursor.fetchall()
    conn.close()
    return data

def add_user_db(nombre, contraseña):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    pass_hash = generate_password_hash(contraseña)
    cursor.execute('INSERT INTO users (nombre, contraseña) VALUES (?, ?)', (nombre, pass_hash,))
    conn.commit()
    conn.close()

def delete_user_db(nombre):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE nombre = ?', (nombre,))
    conn.commit()
    conn.close()

