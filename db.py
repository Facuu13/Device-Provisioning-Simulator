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

def insert_device(device: dict):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO devices (device_id, state, created_at, provisioned_at, provision_token, activated_at, fw_version)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        device['device_id'],
        device['state'],
        device['created_at'],
        device['provisioned_at'],
        device['provision_token'],
        device['activated_at'],
        device['fw_version']
    ))
    conn.commit()
    conn.close()

def list_devices():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    rows = cursor.fetchall() # Obtener todas las filas
    devices = [dict(row) for row in rows] # Convertir filas a diccionarios
    conn.close()
    return devices

def get_device(device_id: str):
    conn = get_conn() # Conectar a la base de datos
    cursor = conn.cursor() # Crear un cursor
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,)) # Ejecutar consulta
    row = cursor.fetchone() # Obtener una fila
    conn.close() # Cerrar la conexión
    return dict(row) if row else None # Devolver la fila como diccionario o None si no existe

def update_device(device_id: str, fields: dict):
    conn = get_conn()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(device_id)
    
    cursor.execute(f'''
        UPDATE devices
        SET {set_clause}
        WHERE device_id = ?
    ''', values)
    
    conn.commit()
    conn.close()