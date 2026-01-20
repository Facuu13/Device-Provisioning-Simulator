import sqlite3

DB_PATH = 'devices.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH) # Conectar a la base de datos
    conn.row_factory = sqlite3.Row # Para obtener filas como diccionarios
    return conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY,
            state TEXT,
            created_at INTEGER,
            provisioned_at INTEGER,
            provision_token TEXT,
            activated_at INTEGER,
            fw_version TEXT
        )
    ''')
    conn.commit()
    conn.close()

