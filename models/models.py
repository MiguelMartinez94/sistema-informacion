# ===============================
# models/models.py - MODELOS
# ===============================

from models.database import get_db
import json
from datetime import datetime

class Mapa:
    def __init__(self, id=None, nombre=None, descripcion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = None
        self.fecha_modificacion = None
    
    @staticmethod
    def crear(nombre, descripcion=None):
        """Crear un nuevo mapa"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('''
                INSERT INTO mapas (nombre, descripcion) 
                VALUES (?, ?)
            ''', (nombre, descripcion))
            mapa_id = cursor.lastrowid
        else:  # MySQL
            cursor.execute('''
                INSERT INTO mapas (nombre, descripcion) 
                VALUES (%s, %s)
            ''', (nombre, descripcion))
            mapa_id = cursor.lastrowid
        
        db.commit()
        return mapa_id
    
    @staticmethod
    def obtener_todos():
        """Obtener todos los mapas"""
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM mapas ORDER BY fecha_creacion DESC')
        
        if hasattr(db, 'row_factory'):  # SQLite
            return [dict(row) for row in cursor.fetchall()]
        else:  # MySQL
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_por_id(mapa_id):
        """Obtener mapa por ID"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('SELECT * FROM mapas WHERE id = ?', (mapa_id,))
        else:  # MySQL
            cursor.execute('SELECT * FROM mapas WHERE id = %s', (mapa_id,))
        
        result = cursor.fetchone()
        if result:
            if hasattr(db, 'row_factory'):  # SQLite
                return dict(result)
            else:  # MySQL
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
        return None
    
    @staticmethod
    def eliminar(mapa_id):
        """Eliminar mapa"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('DELETE FROM mapas WHERE id = ?', (mapa_id,))
        else:  # MySQL
            cursor.execute('DELETE FROM mapas WHERE id = %s', (mapa_id,))
        
        db.commit()
        return cursor.rowcount > 0

class MunicipioConfiguracion:
    def __init__(self, mapa_id, municipio_id, color='#FFFFFF', informacion=None, imagen_url=None):
        self.mapa_id = mapa_id
        self.municipio_id = municipio_id
        self.color = color
        self.informacion = informacion
        self.imagen_url = imagen_url
    
    def guardar(self):
        """Guardar configuración de municipio"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('''
                INSERT OR REPLACE INTO municipios_configuracion 
                (mapa_id, municipio_id, color, informacion, imagen_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.mapa_id, self.municipio_id, self.color, self.informacion, self.imagen_url))
        else:  # MySQL
            cursor.execute('''
                INSERT INTO municipios_configuracion 
                (mapa_id, municipio_id, color, informacion, imagen_url)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                color = VALUES(color),
                informacion = VALUES(informacion),
                imagen_url = VALUES(imagen_url)
            ''', (self.mapa_id, self.municipio_id, self.color, self.informacion, self.imagen_url))
        
        db.commit()
    
    @staticmethod
    def obtener_por_mapa(mapa_id):
        """Obtener todas las configuraciones de municipios de un mapa"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('''
                SELECT mc.*, m.nombre as municipio_nombre
                FROM municipios_configuracion mc
                JOIN municipios m ON mc.municipio_id = m.id
                WHERE mc.mapa_id = ?
            ''', (mapa_id,))
            return [dict(row) for row in cursor.fetchall()]
        else:  # MySQL
            cursor.execute('''
                SELECT mc.*, m.nombre as municipio_nombre
                FROM municipios_configuracion mc
                JOIN municipios m ON mc.municipio_id = m.id
                WHERE mc.mapa_id = %s
            ''', (mapa_id,))
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    @staticmethod
    def obtener_configuracion(mapa_id, municipio_id):
        """Obtener configuración específica de un municipio"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('''
                SELECT * FROM municipios_configuracion 
                WHERE mapa_id = ? AND municipio_id = ?
            ''', (mapa_id, municipio_id))
            result = cursor.fetchone()
            return dict(result) if result else None
        else:  # MySQL
            cursor.execute('''
                SELECT * FROM municipios_configuracion 
                WHERE mapa_id = %s AND municipio_id = %s
            ''', (mapa_id, municipio_id))
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            return None
    
    @staticmethod
    def eliminar_por_mapa(mapa_id):
        """Elimina todas las configuraciones de un mapa específico."""
        db = get_db()
        cursor = db.cursor()
        
        # Asumiendo MySQL
        cursor.execute('DELETE FROM municipios_configuracion WHERE mapa_id = %s', (mapa_id,))
        
        db.commit()
        return cursor.rowcount

class TablaDatos:
    def __init__(self, mapa_id, filas, columnas, datos=None):
        self.mapa_id = mapa_id
        self.filas = filas
        self.columnas = columnas
        self.datos = datos or []
    
    def guardar(self):
        """Guardar tabla de datos"""
        db = get_db()
        cursor = db.cursor()
        
        datos_json = json.dumps(self.datos)
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('''
                INSERT OR REPLACE INTO tablas_datos 
                (mapa_id, filas, columnas, datos_json)
                VALUES (?, ?, ?, ?)
            ''', (self.mapa_id, self.filas, self.columnas, datos_json))
        else:  # MySQL
            cursor.execute('''
                INSERT INTO tablas_datos 
                (mapa_id, filas, columnas, datos_json)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                filas = VALUES(filas),
                columnas = VALUES(columnas),
                datos_json = VALUES(datos_json)
            ''', (self.mapa_id, self.filas, self.columnas, datos_json))
        
        db.commit()
    
    @staticmethod
    def obtener_por_mapa(mapa_id):
        """Obtener tabla de datos de un mapa"""
        db = get_db()
        cursor = db.cursor()
        
        if hasattr(db, 'row_factory'):  # SQLite
            cursor.execute('SELECT * FROM tablas_datos WHERE mapa_id = ?', (mapa_id,))
            result = cursor.fetchone()
            if result:
                data = dict(result)
                data['datos'] = json.loads(data['datos_json'])
                return data
        else:  # MySQL
            cursor.execute('SELECT * FROM tablas_datos WHERE mapa_id = %s', (mapa_id,))
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                data['datos'] = json.loads(data['datos_json'])
                return data
        return None

class Municipio:
    @staticmethod
    def obtener_todos():
        """Obtener todos los municipios"""
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM municipios ORDER BY nombre')
        
        if hasattr(db, 'row_factory'):  # SQLite
            return [dict(row) for row in cursor.fetchall()]
        else:  # MySQL
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]