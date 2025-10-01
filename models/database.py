# ===============================
# models/database.py - CONEXIÓN DB (SOLO MySQL)
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
    if db is not None:
        if db.is_connected():
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
    """Crear tablas en MySQL"""
    cursor = db.cursor()
    
    try:
        # Tabla de mapas/indicadores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mapas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla de municipios con su configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS municipios_configuracion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mapa_id INT NOT NULL,
                municipio_id VARCHAR(50) NOT NULL,
                color VARCHAR(7) DEFAULT '#FFFFFF',
                informacion TEXT,
                imagen_url VARCHAR(255),
                FOREIGN KEY (mapa_id) REFERENCES mapas (id) ON DELETE CASCADE,
                UNIQUE KEY unique_mapa_municipio (mapa_id, municipio_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla de tablas personalizadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tablas_datos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mapa_id INT NOT NULL,
                filas INT NOT NULL,
                columnas INT NOT NULL,
                datos_json LONGTEXT,
                FOREIGN KEY (mapa_id) REFERENCES mapas (id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # Tabla de municipios base (catálogo)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS municipios (
                id VARCHAR(50) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                region VARCHAR(50)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        print("✓ Tablas creadas exitosamente")
        
        # Insertar municipios base
        municipios_base = [
            ('landaDeMatamoros', 'Landa de Matamoros', 'Sierra'),
            ('arroyoSeco', 'Arroyo Seco', 'Sierra'),
            ('sanJoaquin', 'San Joaquín', 'Sierra'),
            ('cadereytaDeMontes', 'Cadereyta de Montes', 'Semidesierto'),
            ('ezequielMontes', 'Ezequiel Montes', 'Centro'),
            ('colon', 'Colón', 'Centro'),
            ('tequisquiapan', 'Tequisquiapan', 'Centro'),
            ('huimilpan', 'Huimilpan', 'Centro'),
            ('amealcoDeBonfil', 'Amealco de Bonfil', 'Sur'),
            ('sanJuanDelRio', 'San Juan del Río', 'Sur'),
            ('pedroEscobedo', 'Pedro Escobedo', 'Centro'),
            ('corregidora', 'Corregidora', 'Centro'),
            ('queretaro', 'Querétaro', 'Centro'),
            ('elMarques', 'El Marqués', 'Centro'),
            ('toliman', 'Tolimán', 'Semidesierto'),
            ('penamiller', 'Peñamiller', 'Semidesierto'),
            ('pinalDeAmoles', 'Pinal de Amoles', 'Sierra'),
            ('jalpanDeSerra', 'Jalpan de Serra', 'Sierra')
        ]
        
        # Insertar municipios uno por uno para mejor control
        for municipio in municipios_base:
            cursor.execute('''
                INSERT IGNORE INTO municipios (id, nombre, region) 
                VALUES (%s, %s, %s)
            ''', municipio)
        
        print(f"✓ {len(municipios_base)} municipios insertados")
        
    except mysql.connector.Error as err:
        print(f"Error creando tablas: {err}")
        raise
    finally:
        cursor.close()

def test_connection():
    """Función para probar la conexión MySQL"""
    try:
        from app import app  # Ajusta según tu estructura
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            cursor.close()
            print(f"✓ Conexión exitosa. MySQL versión: {version[0]}")
            return True
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        return False