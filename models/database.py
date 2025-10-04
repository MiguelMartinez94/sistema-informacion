# ===============================
# models/database.py - CONEXIÓN DB (AJUSTADO A NUEVO ESQUEMA)
# ===============================

import mysql.connector
from flask import current_app, g

def get_db():
    """Obtiene conexión a la base de datos MySQL"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB'],
                autocommit=True,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            print("✓ Conexión MySQL establecida")
        except mysql.connector.Error as err:
            print(f"Error conectando a MySQL: {err}")
            raise
    return g.db

def close_db(e=None):
    """Cierra conexión a la base de datos"""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()
        print("✓ Conexión MySQL cerrada")

def init_db(app):
    """Inicializa la base de datos MySQL"""
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        create_tables(db)
        print("✓ Base de datos MySQL inicializada")

def create_tables(db):
    """Crear tablas en MySQL según el esquema del usuario."""
    cursor = db.cursor()
    try:
        # 1. Tabla 'Mapas'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Mapas (
                id_mapa INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # 2. Tabla 'Contenidos'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Contenidos (
                id_contenido INT AUTO_INCREMENT PRIMARY KEY,
                color VARCHAR(7) DEFAULT '#FFFFFF',
                detalle TEXT,
                imagen VARCHAR(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # 3. Tabla 'Municipios' (Catálogo y relación)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Municipios (
                id_municipio VARCHAR(50) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                id_mapa INT NOT NULL,
                id_contenido INT,
                PRIMARY KEY (id_mapa, id_municipio),
                FOREIGN KEY (id_mapa) REFERENCES Mapas(id_mapa) ON DELETE CASCADE,
                FOREIGN KEY (id_contenido) REFERENCES Contenidos(id_contenido) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        print("✓ Tablas (Mapas, Contenidos, Municipios) verificadas/creadas.")
        
    except mysql.connector.Error as err:
        print(f"Error creando tablas: {err}")
        raise
    finally:
        cursor.close()

def test_connection():
    # ... (esta función puede permanecer igual)
    pass